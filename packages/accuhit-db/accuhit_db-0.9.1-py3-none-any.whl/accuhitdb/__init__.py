# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class DefaultDBConfig(object):
    """
    db設定檔，包含host, user, password等連線資訊
    """
    def __init__(self, dbname, url=None, host=None, username=None, password=None, port=None, replicaset=None):
        self.__url = url
        self.__host = host
        self.__port = port
        self.__dbname = dbname
        self.__username = username
        self.__password = password
        self.__replicaset = replicaset

    @property
    def url(self):
        return self.__url

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def dbname(self):
        return self.__dbname

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password

    @property
    def replicaset(self):
        return self.__replicaset
