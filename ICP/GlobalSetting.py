# -*- coding: UTF-8 -*-
''' 
 (c) Copyright 2020, XDMTECH All rights reserved.
  
 Source name: GlobalSetting.py
 Description: Python Loader global setting file
 
 Modification history:
 Date        Ver.   Author           Comment
 ----------  -----  ---------------  -----------------------------------------
 2020/09/12  I0.00  Owen Wang        Initial Release
 2021/09/29  I0.00  Angel Luo        Update DB connection for Koresemi
 '''
import XdmLib.Base
#===============================================================================
# Setting
#===============================================================================
DEBUG = False
# Oracle RAC Load Balance Ref: https://docs.oracle.com/cd/E57185_01/EPMIS/apbs01s01.html
CTRL_TABLE_CONN = 'oracle+cx_oracle://SYSTEM:Wfy123456@localhost:1521/orcl'
SOURCE_CONNECT_STRING = 'oracle+cx_oracle://SYSTEM:Wfy123456@localhost:1521/orcl'
TARGET_CONNECT_STRING = 'oracle+cx_oracle://SYSTEM:Wfy123456@localhost:1521/orcl'
GROUP = ''
HOSTNAME = ''
CONTROL_FILE_PATH = ""
ALLOW_DUPLICATE_EXECUTE = True
IS_USING_LATESTJSON=False
#===============================================================================
# SMTP Setting
#===============================================================================
sServer = 'smtp.gmail.com'
sPort = 587
sUser   = 'xdmtech@gmail.com'
sPres = 'xdm'
sPWD   = ''
bAuth = False
bSSL = False
#===============================================================================
# File to DB Setting
#===============================================================================
SOURCE_FOLDER = 'D:/To/ICP'
SKIP_FOLDER = './Data/Skip'
ARCHIVE_FOLDER = './Data/Archive'
ERROR_FOLDER = './Data/Error'
ARCHIVE_TYPE = XdmLib.Base.KeepType.Days.value
ARCHIVE_MAX_VALUE = 3
ARCHIVE_CHECK_MIDNIGHT = 0 # Check midnight, minutes: default = -1 = 1440, 0 = don't check
ERROR_TYPE = XdmLib.Base.KeepType.Days.value
ERROR_MAX_VALUE = 30
ERROR_CHECK_MIDNIGHT = 0 # Check midnight, minutes: default = -1 = 1440, 0 = don't check
FAB=''
# CTRL_TABLE_CONN = CTRL_TABLE_CONN if CTRL_TABLE_CONN else EDADB
GROUP = "PROD"
HOSTNAME = ""
CONTROL_FILE_PATH = ""