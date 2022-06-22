# -*- coding: UTF-8 -*-
'''
 (c) Copyright 2020, XDMTECH All rights reserved.

 Source name: core.py
 Description: File to DB(select-delete-insert-update)

 Modification history:
 Date        Ver.   Author           Comment
 ----------  -----  ---------------  -----------------------------------------
 2020/09/12  I0.00  Owen Wang        Initial Release
 2021/09/29  I0.00  Angel Luo        Update DB information for Koresemi
 '''
import XdmLib
import importlib
import datetime
import os 
import imp
import shutil
import pandas as pd
from glob2 import glob
log = XdmLib.logging.getLogger()
config_sql = importlib.import_module("config_sql")
config = imp.load_source('config', 'config.py')
import Parsing
import time
import traceback
import hashlib
import numpy
import statistics

def logicfunction(sourcedb, targetdb,sLastDataTime,sMaxDataTime):
    
    # fpath1 = glob(os.path.join(os.path.abspath(config.SOURCE_FOLDER), '**/*.*'), recursive=True)
    fpaths = glob(os.path.join(os.path.abspath(config.SOURCE_FOLDER), '**/**'), recursive=True)
    errmsg = ''
    try:
        tStarts=time.time()#begin time
        for fpath in fpaths:
            file_name, file_extension = os.path.splitext(fpath)
            if file_extension.lower() != '.csv':
                log.error("%s is NOT CSV file.", os.path.basename(fpath))
                # msg = XdmLib.MoveFile(fpath, config.SKIP_FOLDER + '/ExtensionNotCSV')
                msg = XdmLib.MoveFile(fpath, config.ERROR_FOLDER)
                log.error("Move file: %s to Skip folder: %s.", fpath, msg)
                log.critical("{os.path.basename(file)} is NOT CSV file.\nMove file: {file} to Skip folder: {msg}.")  #A0.04 Error Message
                continue
            
            print("The size of file is %f KB"%(os.path.getsize(fpath)/float(1024)))
            log.info("The size of file is %f KB"%(os.path.getsize(fpath)/float(1024)))
            df,errmsg,tStart = Parsing.convertallfiletodfinlist(fpath,targetdb)
            try:
                log.info(""""*delete SQL_DEL_ICP_DATA_BY_KEY: sql start""")
                for index, row in df.iterrows():
                    targetdb.execute(config_sql.SQL_DEL_ICP_DATA_BY_KEY, RUN=row['RUN'],PROCESS_START_TIME=row['Process Start Time'],TOTALTIME=row['TotalTime'])
                log.info(""""*delete: sql end""")


                log.info(""""*INSERT: sql start""")
                targetdb.executemanyfordataframe(config_sql.SQL_INS_ICP_DATA, df)
                log.info(""""*INSERT: sql end""")
                msg = XdmLib.MoveFile(fpath, config.ARCHIVE_FOLDER)
                if config.ARCHIVE_FOLDER:
                    log.info("Move file: %s to Archive folder: %s.", fpath, msg)
                else:
                    log.info("Delete file: %s.", fpath)
                if targetdb:
                    targetdb.commit()
                if sourcedb:
                    sourcedb.commit()
                tEnd = time.time()#計時結束
                log.info("bulk insert, It cost %f sec" % (tEnd - tStart))
                print("bulk insert, It cost %f sec" % (tEnd - tStart))
            except Exception as ex:
                XdmLib.message = "Fail!"+ str(ex)
                log.error(ex, exc_info=True, stack_info=True)
                errmsg = errmsg + '{0}\n'.format(traceback.format_exc())
                msg = XdmLib.MoveFile(fpath, config.ERROR_FOLDER)
                log.error("Move file: %s to Error folder: %s.", fpath, msg)
                if sourcedb:
                    log.debug(sourcedb.getstatement())
                    sourcedb.rollback()
                log.error(ex, exc_info=True, stack_info=True)

                if targetdb:
                    log.debug(targetdb.getstatement())
                    targetdb.rollback()

                log.error(ex, exc_info=True, stack_info=True)

                raise ex
        tEnds=time.time()#end time 
        log.info("all files,it cost %f sec" %(tEnds - tStarts))
        print("all files,it cost %f sec" %(tEnds - tStarts))
    except Exception as ex:
        log.error(ex, exc_info=True, stack_info=True)
        errmsg = errmsg + '{0}\n'.format(traceback.format_exc())
        XdmLib.WriteToErrorLog("FileError", "Parsing.py", "file parsing error", errmsg)    
    
def LoaderMain(sourcedb, targetdb, sourcedbForHA=None, targetdbForHA=None, SQLObjectForHA=None):
    Database = importlib.import_module(XdmLib.Database.DbClient.imp_module)
    config = XdmLib.config
    # 0=InProcess,1=Success,2=Done,9=Fail/CMD:-1:Run,-2=Cancel
    status = 0
    XdmLib.SetProcessStatus(status)

    try:
        log.debug("Main Code Start")
        # source db connection
        if not sourcedb:
            sourcedb = XdmLib.Database.DbClient(config.SOURCE_CONNECT_STRING)

        if not targetdb:
            targetdb = XdmLib.Database.DbClient(config.TARGET_CONNECT_STRING)


        #last_data_time = None
        if XdmLib.last_data_time is None:
            log.error("last_data_time is None ")
            XdmLib.last_data_time = datetime.datetime.strptime('2020-01-01 00:00:00','%Y-%m-%d %H:%M:%S')
        last_data_time = datetime.datetime.strftime(XdmLib.last_data_time,'%Y-%m-%d %H:%M:%S')


        if last_data_time == None: #sure is last_data_time null?
            log.error("last_data_time is null ")
        else:
            log.debug("last_data_time = " + last_data_time) #there is setting last_data_time
               
        ####Set Logical Time        
        try:
                    
            max_data_time_temp = sourcedb.execute(config_sql.SQL_GET_MAX_DATATIME).fetchall()
            
            for row in max_data_time_temp:
                log.debug("actual max_data_time = " + row[0])
                #max_data_time = row[0]
                max_data_time_temp = row[0]  #save max_data_time
            #}

            #region time control
            Max_query_hour = datetime.timedelta(hours = int(config.Max_query_hour))
            Time_frequency = datetime.timedelta(minutes = int(config.Time_frequency))
            sysdate_program_start = datetime.datetime.now()
            
            if isinstance(max_data_time_temp, str) == False:
                log.error("max_data_time_temp is not str")
                max_data_time_temp = '1911-01-01 00:00:00'
                
            if Time_frequency > sysdate_program_start - datetime.datetime.strptime(max_data_time_temp,'%Y-%m-%d %H:%M:%S'):
                max_data_time_temp = datetime.datetime.strftime((sysdate_program_start - Time_frequency), '%Y-%m-%d %H:%M:%S')
            #}
            # confirm max_data_time > last_data_time
            if datetime.datetime.strptime(max_data_time_temp,'%Y-%m-%d %H:%M:%S') < datetime.datetime.strptime(last_data_time,'%Y-%m-%d %H:%M:%S'):
                log.error("max_data_time <= last_data_time:" + "actual max_data_time = " + max_data_time_temp +";current last_data_time=" + last_data_time)
            #}
            #revise max_data_time - last_data_time < Max_query_day total_seconds()
            if (datetime.datetime.strptime(max_data_time_temp,'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(last_data_time,'%Y-%m-%d %H:%M:%S')).total_seconds()/3600 > int(config.Max_query_hour):
                max_data_time = datetime.datetime.strftime((datetime.datetime.strptime(last_data_time,'%Y-%m-%d %H:%M:%S') +Max_query_hour), '%Y-%m-%d %H:%M:%S')
            else:
                max_data_time = max_data_time_temp
                  
            sLastDataTime = datetime.datetime.strftime(datetime.datetime.strptime(last_data_time, '%Y-%m-%d %H:%M:%S'), '%Y%m%d %H%M%S')
            sMaxDataTime = datetime.datetime.strftime(datetime.datetime.strptime(max_data_time, '%Y-%m-%d %H:%M:%S'), '%Y%m%d %H%M%S')
            
            targetdb.begin()
            
            # parsing data
            logicfunction(sourcedb, targetdb,sLastDataTime,sMaxDataTime)
            
            XdmLib.last_data_time = datetime.datetime.strptime(max_data_time, '%Y-%m-%d %H:%M:%S')

            #if targetdb:
            #    targetdb.commit()
            #if sourcedb:
            #    sourcedb.commit()
                
            log.debug("Record Table:XDM_PROG_CONTROL, column:Data_TIME_FLG = " + max_data_time)
            XdmLib.message = "Success!"
        except Database.DatabaseError as ex:
            XdmLib.message = "Fail!"+ str(ex)
            if sourcedb:
                log.debug(sourcedb.getstatement())
                sourcedb.rollback()
            log.error(ex, exc_info=True, stack_info=True)   

            if targetdb:
                log.debug(targetdb.getstatement())
                targetdb.rollback()

            log.error(ex, exc_info=True, stack_info=True)
            
            raise ex
    except Database.DatabaseError as ex:
        error, = ex.args
        if error.code in [1]:
            # 1=unique constraint violated
            if sourcedb:
                log.debug(sourcedb.getstatement())
                sourcedb.rollback()
                log.error(ex, exc_info=True, stack_info=True)
            if targetdb:
                log.debug(targetdb.getstatement())
                targetdb.rollback()
                log.error(ex, exc_info=True, stack_info=True)            
        ##################################A0.01 Oracle(ORA-12899 or ORA-01847)
        elif error.code in [12899]:
            # 1=unique constraint violated
            if sourcedb:
                log.debug(sourcedb.getstatement())
                sourcedb.rollback()
                log.error(ex, exc_info=True, stack_info=True)
            if targetdb:
                log.debug(targetdb.getstatement())
                targetdb.rollback()
                log.error(ex, exc_info=True, stack_info=True)            
        elif error.code in [1847]:
            # 1=unique constraint violated
            if sourcedb:
                log.debug(sourcedb.getstatement())
                sourcedb.rollback()
                log.error(ex, exc_info=True, stack_info=True)
            if targetdb:
                log.debug(targetdb.getstatement())
                targetdb.rollback()
                log.error(ex, exc_info=True, stack_info=True)        
        
        raise ex
    except Exception as ex:
        if sourcedb:
            log.debug(sourcedb.getstatement())
            sourcedb.rollback()
        log.error(ex, exc_info=True, stack_info=True)   

        if targetdb:
            log.debug(targetdb.getstatement())
            targetdb.rollback()
        log.error(ex, exc_info=True, stack_info=True)
        raise ex
    finally:
        if sourcedb:
            sourcedb.disconnect()
            sourcedb = None
        del sourcedb

        if targetdb:
            targetdb.disconnect()
            targetdb = None
        del targetdb
    # }try
    
    XdmLib.SetProcessStatus(1)
def compute_md5_value(fileName):
    #"""Compute md5 hash of the specified file"""
    m = hashlib.md5()
    try:
        fd = open(fileName,"rb")
    except IOError:
        log.info("Reading file has problem:%s", fileName)
        return
    x = fd.read()
    fd.close()
    m.update(x)
    return m.hexdigest()


    
    
