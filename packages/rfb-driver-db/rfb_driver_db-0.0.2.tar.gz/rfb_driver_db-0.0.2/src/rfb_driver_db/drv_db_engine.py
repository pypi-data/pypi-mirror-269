#!/usr/bin/python3
'''
Execute a SQLAlchemy database on the given database .

Raises:
    err: Error while connecting with DB.
    ConnectionError: Max db connection resets reached. Connection with db may have been lost.
'''
#######################        MANDATORY IMPORTS         #######################
from __future__ import annotations
#######################         GENERIC IMPORTS          #######################
from typing import Any
from datetime import datetime

#######################       THIRD PARTY IMPORTS        #######################
# SQL Alchemy
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
#######################    SYSTEM ABSTRACTION IMPORTS    #######################
from rfb_config_tool import sys_conf_read_config_params
from rfb_logger_tool import Logger, sys_log_logger_get_module_logger
log: Logger = sys_log_logger_get_module_logger(__name__)

#######################          PROJECT IMPORTS         #######################

#######################          MODULE IMPORTS          #######################
from .drv_db_types import DrvDbTypeE

#######################              ENUMS               #######################

######################             CONSTANTS              ######################
from .context import DEFAULT_CRED_FILEPATH

#######################             CLASSES              #######################
class DrvDbSqlEngineC:
    '''
    Classmethod to create a SqlAlchemy engine.
    '''

    __MAX_RESETS = 2

    def __init__(self, db_type : DrvDbTypeE, config_file: str= DEFAULT_CRED_FILEPATH):
        '''
        Create an connector to the MySQL database server

        Args:
            db_type (DrvDbTypeE): type of database to connect to.
            config_file (str): path to the configuration file.
        '''
        params = {}
        # read connection parameters
        self.config_file = config_file
        section='database'
        if db_type == DrvDbTypeE.CACHE_DB:
            section = 'cache_db'
        if db_type == DrvDbTypeE.MASTER_DB:
            section = 'master_db'
        self.section = section
        try:
            params = sys_conf_read_config_params(filename=config_file, section= self.section)

            # create engine
            url = 'mysql+mysqlconnector://' + params['user'] + ':'\
                    + params['password'] + '@' + params['host'] + ':'\
                    + str(params['port']) + '/' + params['database']

            log.debug(f"Creating database engine with url: [{url}]")
            self.engine: Engine = create_engine(url=url, echo=False, future=True)
            self.session : Session = Session(bind=self.engine, future=True)
            self.session.begin()
            self.n_resets = 0
            self.__last_connection = datetime.now()

        except Exception as err:
            log.error(msg="Error on DB Session creation. Please check DB " +\
                      f"credentials and params: {params}")
            log.error(msg=err)
            raise err


    def commit_changes(self, raise_exception : bool = False) -> None:
        '''
        Perform a commit againt the used database. If any error occurs, a
        rollback is performed.

        Args:
            raise_exception (bool, optional): If True, an exception is raised if any error occurs. \
                Defaults to False.

        Raises:
            err: Throw an exception if any error occurs during commit transaction.
        '''
        try:
            self.session.commit()
            self.__last_connection = datetime.now()
        except Exception as err:
            log.critical(err)
            log.critical("Error while commiting change to DB. Performing rollback...")
            self.session.rollback()
            if raise_exception:
                raise err

    def check_connection(self) -> None:
        '''
        Check when has been the last connection with the database and reconnect with it
        '''
        elapsed_time = datetime.now() - self.__last_connection
        if elapsed_time.seconds > 30:
            log.warning((f"Database {self.section} last connection "
                         "was 30s ago, trying to connect again"))
            self.__reset_engine()

    def close_connection(self) -> None:
        '''
        Close the connection with the database.
        '''
        self.commit_changes()
        self.session.close()


    def __reset_engine(self) -> None:
        '''
        Create a new engine and initialize it
        '''
        params: dict[str, Any] = sys_conf_read_config_params(#pylint: disable=unsubscriptable-object
            filename=self.config_file, section=self.section)

        url = 'mysql+mysqlconnector://' + params['user'] + ':'\
            + params['password'] + '@' + params['host'] + ':'\
            + str(params['port']) + '/' + params['database']
        self.engine = create_engine(url, echo=False, future=True)
        self.session = Session(self.engine, future=True)
        self.session.begin()
        self.__last_connection = datetime.now()


    def reset(self) -> None:
        '''
        Resets the connection to the database .

        Raises:
            ConnectionError: Max db connection resets reached. Connection \
                                  with db may have been lost.
        '''
        if self.n_resets <= self.__MAX_RESETS:
            self.__reset_engine()
            self.n_resets += 1
        else:
            raise ConnectionError("Max db connection resets reached. Connection \
                                  with db may have been lost.")


#######################            FUNCTIONS             #######################
