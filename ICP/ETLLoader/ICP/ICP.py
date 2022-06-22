# -*- coding: utf-8 -*-
''' 
 (c) Copyright 2020, XDMTECH All rights reserved.
  
 Source name: Loader.py
 Description: db to db (select_delete_insert)
 
 Modification history:
 Date        Ver.   Author           Comment
 ----------  -----  ---------------  -----------------------------------------
 2020/09/12  I0.00  Owen Wang        Initial Release
 2021/09/29  I0.00  Angel Luo        For Koresemi
'''
#===============================================================================
# Initial
#===============================================================================
import os.path
os.chdir(os.path.dirname(os.path.realpath(__file__))) 
os.environ['NLS_LANG']='SIMPLIFIED CHINESE_CHINA.UTF8'
import datetime
import importlib
import glob
import socket
import traceback
import sys
sys.path.append('../..')
import XdmLib
log = XdmLib.logging.getLogger()
config = XdmLib.config

#===============================================================================
# Finalize method
#===============================================================================
def __del__(self):
    pass

            
#===============================================================================
# Main method
#===============================================================================
if __name__ == "__main__":
    try:
        Database = importlib.import_module(XdmLib.Database.DbClient.imp_module)
        config_sql = importlib.import_module("config_sql")
        core = importlib.import_module("core")
        
        sourcedb = None
        targetdb = None
        
        sServerName = socket.gethostname()
        sProgramPath = os.path.abspath(__file__)
        sProgramName = os.path.basename(__file__)
        #SQLObjectForHA = XdmLib.HA.checkIfCURDwithXdmProgHaControlTable(sServerName, sProgramPath, sProgramName, 
                                                            #ProgramType = config.ProgramType, 
                                                            #NextRunIdleSeconds = config.NextRunIdleSeconds,
                                                            #HA_UID = config.HA_UID,
                                                            #sourcedbForException = sourcedb)
        
        core.LoaderMain(sourcedb, targetdb)
       # XdmLib.HA.Loader_HA(core.LoaderMain, sourcedbForHA=sourcedb, targetdbForHA=targetdb, SQLObjectForHA=SQLObjectForHA)
    except Exception as ex:
        log.error(ex, exc_info=True, stack_info=True)
        XdmLib.SetProcessStatus(9, traceback.format_exc())