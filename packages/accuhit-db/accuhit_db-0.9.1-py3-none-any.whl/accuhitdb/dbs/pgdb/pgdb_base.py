import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from accuhitdb import DefaultDBConfig

logger = logging.getLogger("config.pg_client")


class PgConfig(DefaultDBConfig):
    """
    Pg db設定檔類別
    """
    __timezone = "Asia/Taipei"
    __schema = None
    __autoUpdate = False

    @property
    def schema(self):
        return self.__schema

    @schema.setter
    def schema(self, value):
        self.__schema = value

    @property
    def autoUpdate(self):
        return self.__autoUpdate

    @autoUpdate.setter
    def autoUpdate(self, value):
        self.__autoUpdate = value


class PgConnectionProvider(object):
    """
    Pg client提供者，簡化創建client instance程序
    """
    def __init__(self, config):
        logger.info("===init PgClient===")
        self.SessionLocal = None
        if not isinstance(config, PgConfig):
            raise Exception("input attribute(config) type must be pgdb_base.PgConfig")
        self.pg_config = config

    def create_engine(self):
        return create_engine(self.pg_config.url,
                             pool_pre_ping=True,
                             pool_size=10,
                             max_overflow=20,
                             connect_args={"options": f"-c search_path={self.pg_config.schema}"})

    def create_client(self, **kwargs):
        Session = sessionmaker(autocommit=False,
                               autoflush=False,
                               bind=self.create_engine(),
                               **kwargs)
        session = Session(**kwargs)
        return session

    def get_session(self):
        session = self.create_client()
        try:
            yield session
        finally:
            session.close()

    def create_table(self):
        if self.pg_config.autoUpdate:
            Base.metadata.create_all(bind=self.create_engine())


Base = declarative_base()
