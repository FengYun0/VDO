# -*- coding: utf-8 -*-





### A0.01 end# -*- coding: utf-8 -*-
''' 
 (c) Copyright 2020, XDMTECH All rights reserved.
  
 Source name: config_sql.py
 Description: Loader SQL Template file
 
 Modification history:
 Date        Ver.   Author           Comment
 ----------  -----  ---------------  -----------------------------------------
 2020/09/12  I0.00  Owen Wang        Initial Release
 2021/09/29  I1.00  Hugo Wang        JNFN Revised Ver. for Oracle
'''

#===============================================================================
# SQL Template
#===============================================================================
SQL_GET_MAX_DATATIME = """
select to_char(SYSDATE, 'YYYY-MM-DD HH24:MI:SS') from dual
"""

SQL_DEL_ICP_DATA_BY_KEY="""
DELETE FROM ICP
WHERE 1=1
AND RUN = :RUN
AND PROCESS_START_TIME = TO_DATE(:PROCESS_START_TIME,'YYYY-MM-DD HH24:mi:ss')
AND TOTALTIME = :TOTALTIME
"""

SQL_INS_ICP_DATA="""
INSERT INTO ICP
(
    RUN,
    PROCESS_START_TIME,
    PM_SN,
    RECIPE,
    WAFER_COUNTER,
    SRF_HOUR,
    BRF_HOUR,
    TOTALTIME,
    STEP_NAME,
    STEP_ID,
    STEPTIME,
    PROCESSPRESSURE,
    HEPRESSURE,
    HEFLOW,
    VATPOSITION,
    CHAMBERPRESSURE,
    FORLINEPRESSURE,
    SRFFORWARDPOWER,
    SRFREFL,
    BRFFORWARDPOWER,
    BRFREFL,
    DCBIAS,
    TOPC1,
    TOPC2,
    BOTTOMC1,
    BOTTOMC2,
    AR,
    O2,
    N2,
    CL2,
    BCL3,
    CHF3,
    HBR,
    SPARE8,
    CHILLERTEMP,
    MIDDLETEMP1,
    MIDDLETEMP2,
    MIDDLETEMP3,
    MIDDLETEMP4,
    TOPTEMP,
    BOTTOMTEMP,
    INNERPIPETEMP,
    UPDATE_TIME
)VALUES(
    :RUN,
    TO_DATE(:PROCESS_START_TIME,'YYYY-MM-DD HH24:mi:ss'),
    :PM_SN,
    :RECIPE,
    :WAFER_COUNTER,
    :SRF_HOUR,
    :BRF_HOUR,
    :TOTALTIME,
    :STEP_NAME,
    :STEP_ID,
    :STEPTIME,
    :PROCESSPRESSURE,
    :HEPRESSURE,
    :HEFLOW,
    :VATPOSITION,
    :CHAMBERPRESSURE,
    :FORLINEPRESSURE,
    :SRFFORWARDPOWER,
    :SRFREFL,
    :BRFFORWARDPOWER,
    :BRFREFL,
    :DCBIAS,
    :TOPC1,
    :TOPC2,
    :BOTTOMC1,
    :BOTTOMC2,
    :AR,
    :O2,
    :N2,
    :CL2,
    :BCL3,
    :CHF3,
    :HBR,
    :SPARE8,
    :CHILLERTEMP,
    :MIDDLETEMP1,
    :MIDDLETEMP2,
    :MIDDLETEMP3,
    :MIDDLETEMP4,
    :TOPTEMP,
    :BOTTOMTEMP,
    :INNERPIPETEMP,
    SYSDATE
)
"""

