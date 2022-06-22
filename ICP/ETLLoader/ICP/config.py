# -*- coding: utf-8 -*-
''' 
 (c) Copyright 2020, XDMTECH All rights reserved.
  
 Source name: config.py
 Description: Loader configure file
 
 Modification history:
 Date        Ver.   Author           Comment
 ----------  -----  ---------------  -----------------------------------------
 2020/09/12  I0.00  Owen Wang        Initial Release
'''
import imp
import enum

#===============================================================================
# System variable
#===============================================================================
GlobalSetting = imp.load_source('GlobalSetting', '../../GlobalSetting.py')
CTRL_TABLE_CONN = GlobalSetting.CTRL_TABLE_CONN
#===============================================================================
# Setting
#===============================================================================
SOURCE_CONNECT_STRING = GlobalSetting.SOURCE_CONNECT_STRING
TARGET_CONNECT_STRING = GlobalSetting.TARGET_CONNECT_STRING

HA_UID="M2_ETL"
ProgramType = 1 #1 ?O[Primary?D??]?B0 ?O[Standby?D??]
NextRunIdleSeconds = 300 #5????

SOURCE_FOLDER = GlobalSetting.SOURCE_FOLDER
SKIP_FOLDER = GlobalSetting.SKIP_FOLDER
ARCHIVE_FOLDER = GlobalSetting.ARCHIVE_FOLDER
ARCHIVE_TYPE = GlobalSetting.ARCHIVE_TYPE
ARCHIVE_MAX_VALUE = GlobalSetting.ARCHIVE_MAX_VALUE
ARCHIVE_CHECK_MIDNIGHT = GlobalSetting.ARCHIVE_CHECK_MIDNIGHT
ERROR_FOLDER = GlobalSetting.ERROR_FOLDER
ERROR_TYPE = GlobalSetting.ERROR_TYPE
ERROR_MAX_VALUE = GlobalSetting.ERROR_MAX_VALUE
ERROR_CHECK_MIDNIGHT = GlobalSetting.ERROR_CHECK_MIDNIGHT
Max_query_hour = 24
Time_frequency = 10
GROUP = "File"
HOSTNAME = ""
CONTROL_FILE_PATH = GlobalSetting.CONTROL_FILE_PATH
COMMENT = ''
ALLOW_DUPLICATE_EXECUTE = True
DEBUG = ''
#LOG_DB_HANDLER = ''

#===============================================================================
# SMTP Setting
#===============================================================================
sServer = GlobalSetting.sServer
sPort = GlobalSetting.sPort
sUser   = GlobalSetting.sUser
sPres = GlobalSetting.sPres
sPWD   = GlobalSetting.sPWD
bAuth = GlobalSetting.bAuth
bSSL = GlobalSetting.bSSL

#lstTo = ['']
#lstCC = [''] 
