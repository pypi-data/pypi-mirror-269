#!/usr/bin/python3
'''
Create a ORM model of the defined database.

This document's base structure is generated automaticly using sqlacodegen extracting data from DB.
Attributes in this script does not follow PEP8 snake_case naming convention.

sqlacodegen mysql+mysqlconnector://user:password@ip:port/db_name --outfile drv_db_dao.py
'''
#######################        MANDATORY IMPORTS         #######################

#######################         GENERIC IMPORTS          #######################

#######################       THIRD PARTY IMPORTS        #######################
from sqlalchemy import Column, Enum
from sqlalchemy.dialects.mysql import MEDIUMINT
from sqlalchemy.orm import declarative_base

#######################    SYSTEM ABSTRACTION IMPORTS    #######################
from rfb_logger_tool import Logger, sys_log_logger_get_module_logger
log: Logger = sys_log_logger_get_module_logger(__name__)

#######################          PROJECT IMPORTS         #######################


#######################          MODULE IMPORTS          #######################
from .drv_db_dao_base import DrvDbBaseExperimentC, DrvDbBaseGenericMeasureC,\
    DrvDbBaseExtendedMeasureC, DrvDbBaseStatusC
from .drv_db_types import DrvDbCyclingModeE

#######################              ENUMS               #######################


#######################             CLASSES              #######################
Base = declarative_base()
metadata = Base.metadata

class DrvDbCacheExperimentC(DrvDbBaseExperimentC, Base): #pylint: disable=too-many-instance-attributes
    '''
    Class method to create a simplified model of database Experiment table.
    '''
    __tablename__: str = 'ExperimentCache'

    CSID = Column(MEDIUMINT(unsigned=True), nullable=False)
    BatID = Column(MEDIUMINT(unsigned=True), nullable=False)
    ProfID = Column(MEDIUMINT(unsigned=True), nullable=False)

class DrvDbCacheGenericMeasureC(DrvDbBaseGenericMeasureC, Base):
    '''
    Class method to create a model of cache database GenericMeasures table.
    '''
    __tablename__ = 'GenericMeasuresCache'

    InstrID = Column(MEDIUMINT(unsigned=True), nullable=False)
    PowerMode = Column(Enum(*DrvDbCyclingModeE.get_all_values()), nullable= False)

class DrvDbCacheExtendedMeasureC(DrvDbBaseExtendedMeasureC, Base):
    '''
    Class method to create a model of cache database ExtendedMeasures table.
    '''
    __tablename__ = 'ExtendedMeasuresCache'

    UsedMeasID = Column(MEDIUMINT(unsigned=True), primary_key=True, nullable=False)

class DrvDbCacheStatusC(DrvDbBaseStatusC, Base):
    '''
    Class method to create a base model of database Status table.
    '''
    __tablename__ = 'StatusCache'

    DevID = Column(MEDIUMINT(unsigned=True), nullable=False)
