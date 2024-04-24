# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import abc
import logging
from collections.abc import MutableMapping
from datetime import datetime

import certifi
import pytz
from bson.objectid import ObjectId
from pymongo import MongoClient

from accuhitdb import DefaultDBConfig

logger = logging.getLogger("config.mongo_client")
default_db_pytz = pytz.timezone("Asia/Taipei")


class MongoConfig(DefaultDBConfig):
    """
    Mongo db設定檔類別
    """
    __timezone = "Asia/Taipei"
    __auth_mode = None
    __auth_source = None

    @property
    def auth_mode(self):
        return self.__auth_mode

    @auth_mode.setter
    def auth_mode(self, value):
        self.__auth_mode = value

    @property
    def auth_source(self):
        return self.__auth_source

    @auth_source.setter
    def auth_source(self, value):
        self.__auth_source = value

    @property
    def timezone(self):
        return self.__timezone

    @timezone.setter
    def timezone(self, value):
        self.__timezone = value


class MongoClientProvider(object):
    """
    Mongo client提供者，簡化創建client instance程序
    """

    def __init__(self, config):
        if not isinstance(config, MongoConfig):
            raise Exception("input attribute(config) type must be mongo_base.MongoConfig")
        self.mongo_config = config
        global default_db_pytz
        default_db_pytz = pytz.timezone(config.timezone)

    def create_client(self, connect=True, **kwargs):
        """
        :param connect: immediately begin connecting to MongoDB in the background. Otherwise connect on the first operation.
        :param kwargs:
        :return:
        """
        auth_source = self.mongo_config.auth_source
        if not auth_source:
            auth_source = self.mongo_config.dbname

        if self.mongo_config.auth_mode:
            client = MongoClient(self.mongo_config.url,
                                 username=self.mongo_config.username,
                                 password=self.mongo_config.password,
                                 replicaset=self.mongo_config.replicaset,
                                 authSource=auth_source,
                                 authMechanism=self.mongo_config.auth_mode,
                                 tlsCAFile=certifi.where(),
                                 connect=connect,
                                 **kwargs
                                 )
        else:
            client = MongoClient(self.mongo_config.url,
                                 replicaset=self.mongo_config.replicaset,
                                 tlsCAFile=certifi.where(),
                                 connect=connect,
                                 **kwargs
                                 )

        logger.debug("create mongo client:{}".format(client))
        return client

    def get_db(self, client):
        return client[self.mongo_config.dbname]

    def get_session(self, client):
        session = client.start_session()
        try:
            with session.start_transaction():
                yield session
        finally:
            session.end_session()


class MongoBaseModel(MutableMapping):
    """
    Mongo entity基礎類別，預設_id, user, time欄位
    """
    _id = None
    crt_user = None
    crt_date = None
    mdy_user = None
    mdy_date = None

    def __init__(self, *args, **kwargs):
        if self._init_default() is not None:
            self.update(self._init_default())  # use the free update to set keys
        self.crt_date = datetime.now(default_db_pytz)
        self.mdy_date = datetime.now(default_db_pytz)
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        super().__setattr__(key, value)

    def __delitem__(self, key):
        super().__delattr__(key)

    def __iter__(self):
        return super().__iter__()

    def __len__(self):
        return super().__len__()

    # @abc.abstractmethod
    def _init_default(self):
        return {}

    def to_dict(self):
        return self.__dict__


class MongoRepository(abc.ABC):
    """
    Mongo client基礎類別，包裝多種資料處理函式
    """

    def __init__(self, db, session):
        self.collection_name = self._get_collection_name()
        self.collection = db[self.collection_name]
        self.session = session

    @abc.abstractmethod
    def _get_collection_name(self):
        pass

    def save_one(self, data):
        if data is None:
            logger.warning("data save to {} is null...".format(self.collection_name))
            return
        self.collection.insert_one(data, session=self.session)
        logger.info("save data to {} success, id is {}".format(self.collection_name, data["_id"]))

    def save(self, data_list):
        if not data_list:
            logger.warning("data save to {} is empty...".format(self.collection_name))
            return
        self.collection.insert_many(data_list, session=self.session)
        logger.info("save list to {} success, action count is {}".format(self.collection_name, len(data_list)))

    def find_by_ids(self, id_list, fields=None, sort=None, limit=-1, offset=-1):
        ids = [ObjectId(id) for id in id_list]
        return self.find({"_id": {"$in": ids}}, fields=fields, sort=sort, limit=limit, offset=offset)

    def find_all(self, fields=None, sort=None, limit=-1, offset=-1):
        return self.find({}, fields=fields, sort=sort, limit=limit, offset=offset)

    def find(self, params, fields=None, sort=None, limit=-1, offset=-1):
        """
        :param params:
        :param fields: 限定查詢結果欄位，型態為dict：key為欄位，value為0(不包含)或1(包含) e.g.{item:1, _id:0}
        :param sort: 排序方式，array of tuple, e.g.[("crt_date", pymongo.DESCENDING)]
        :param limit:
        :param offset:
        :return:
        """
        cursor = self.collection.find(params, fields)
        if sort is not None and len(sort) > 0:
            cursor.sort(sort)
        if offset > -1:
            cursor.skip(offset)
        if limit > -1:
            cursor.limit(limit)
        return list(cursor)

    def count(self, params, fields=None):
        records = list(self.collection.find(params, fields))
        return len(records)

    def delete_by_ids(self, id_list):
        if not id_list:
            logger.info("no data be deleted from {}...".format(self.collection_name))
            return 0
        _ids = [ObjectId(id) for id in id_list]
        return self.delete({"_id": {"$in": _ids}})

    def delete(self, params):
        if not params:
            logger.info("no data de deleted from {}...".format(self.collection_name))
            return 0

        result = self.collection.delete_many(params, session=self.session)
        action = result.deleted_count
        logger.info("deleted data from {} success, action count is {}".format(self.collection_name, action))
        return action

    def update(self, condition, data):
        result = self.collection.update_many(condition, {"$set": data}, session=self.session)
        action = result.modified_count
        logger.info("update {} success, action count is {}".format(self.collection_name, action))

    def save_or_update(self, data):
        result = self.collection.save(data, session=self.session)
        logger.info("update {} success!".format(self.collection_name))
        return result

    def aggregate(self, pipeline, sort=None, limit=-1, offset=-1):
        """

        :param pipeline: 型態為dict
        :param sort: 排序方式，型態為dict：key為欄位，value為降冪或升冪
        :param limit:
        :param offset:
        :return:
        """
        if sort and len(sort) > 0:
            pipeline.append({"$sort": sort})
        if offset > -1:
            pipeline.append({"$skip": offset})
        if limit > -1:
            pipeline.append({"$limit": limit})
        return list(self.collection.aggregate(pipeline))
