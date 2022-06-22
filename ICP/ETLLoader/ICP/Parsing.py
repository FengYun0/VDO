# -*- coding: utf-8 -*-
'''
 (c) Copyright 2020, XDMTECH All rights reserved.

 Source name: Parsing.py
 Description: File to db

 Modification history:
 Date        Ver.   Author           Comment
 ----------  -----  ---------------  -----------------------------------------
 2021/11/12  I0.00  Angel Luo        For LeadTrend
'''
import copy

import numpy as np

import XdmLib
# from ETLLoader.CPLoader.Transpose import Transpose
log = XdmLib.logging.getLogger()
import traceback
import pandas as pd
import imp
#from Transpose import *
import itertools
config = imp.load_source('config', 'config.py')
import importlib
config_sql = importlib.import_module("config_sql")
import time
import csv
from collections import namedtuple
import re

def convertallfiletodfinlist(fpath,targetdb):
    errmsg = ''
    result = []
    filelist = []
    errfpath = ''
    errmsg = ''
    try:
        tStart = time.time()#計時開始
        f = open(fpath, 'r', encoding='utf-8')
        # print('------------------',fpath)
        data = f.readlines()
        # df = pd.read_csv(fpath, header=0,encoding='gbk')
        filename = fpath.strip().split("\\")[-1]
        RUN_COMPILE = re.compile(r'[0-9]{5,}')
        RUN_NO = re.findall(RUN_COMPILE,filename)
        info = {}
        info['RUN'] = RUN_NO[0]
        datatop_len = 0
        for i in data:
            datatop_len = datatop_len + 1
            if re.match(r'TotalTime', i):
                datatop_len = datatop_len - 1
                break
            elif re.match(r'Wafer ID:', i) or re.match(r'Lot ID:', i) or re.match(r'Slot ID:', i):
                continue
            else:
                k = i.split(':', 1)[0].rstrip().lstrip() # 1只切割一次
                l = i.split(':', 1)[1].rstrip().lstrip()
                info[k] = l
        f.close()
        df = pd.read_csv(fpath, sep=",", header=datatop_len)
        df = df.drop(['Unnamed: 35'], axis=1)
        while len(info):
            i = info.popitem()
            df.insert(0, i[0], i[1])
            # df.reindex(columns=i,fill_value=info[i])
        # result.append(df)
            

    except Exception as ex:
        log.error(ex, exc_info=True, stack_info=True)
        errmsg = errmsg + 'fname:{0}, errmsg:{1}\n'.format(fpath, traceback.format_exc())
        # Move file to error folder*
        msg = XdmLib.MoveFile(fpath, config.ERROR_FOLDER)
        log.error("Move file: %s to Error folder: %s.", fpath, msg)

    return df,errmsg,tStart

def convertfiletodataframe(fpath):
    df = []
    try:
        df = pd.read_csv(fpath, header=0)
    except Exception as ex:
        log.error(ex, exc_info=True, stack_info=True)
        # Move file to error folder*
        msg = XdmLib.MoveFile(fpath, config.ERROR_FOLDER)
        log.error("Move file: %s to Error folder: %s.", fpath, msg)
        # Move file to error folder&
    return df

 
