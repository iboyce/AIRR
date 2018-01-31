# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 13:48:40 2017

@author: xuzhi
"""

# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl 
import math
from datasource import estools

conn = pymssql.connect(host="10.237.120.198", port="1433" ,user="wande", password="wande", database="cldb")
conn1 = pymssql.connect(host="10.101.221.183", port="1433" ,user="wande", password="wande", database="wande")
#df = pd.read_sql("Select top 10 TRADE_DT,S_VAL_PE_TTM,S_VAL_PB_NEW from ASHAREEODDERIVATIVEINDICATOR where  S_INFO_WINDCODE='600519.SH' and TRADE_DT = convert(varchar, GETDATE()-1, 112)",con=conn)

stockid='603899.SH'
##取最大近3年的净利润net_profit
sql1="SELECT TOP 3 avg(NET_PROFIT_AVG) as NET_PROFIT_AVG,EST_REPORT_DT FROM AShareConsensusData where S_INFO_WINDCODE='%s' and (EST_REPORT_DT='20191231' or EST_REPORT_DT='20181231' or EST_REPORT_DT='20171231') group by  EST_REPORT_DT"%(stockid)
pre_df_profit_max = pd.read_sql(sql1,con=conn1)
year_num =  len(pre_df_profit_max)

#取2016年净利
pre_profit_max = max(pre_df_profit_max['NET_PROFIT_AVG'])
sql2=" select net_profit_ttm from  AShareTTMHis WHERE report_period='20161231' AND S_INFO_WINDCODE='%s'"%(stockid)
pre_df_profit_min = pd.read_sql(sql2,con=conn1)
pre_profit_min = pre_df_profit_min.iat[0,0]/10000.0

#计算复合增速
compoundrate = math.pow(pre_profit_max/pre_profit_min,1.0/year_num)

#取PE
es = estools(host="10.237.2.132",index="airr_2017.12.21",doc_type="airr_mapping")
data = es.getkv("airr_2017.12.21","airr_mapping",stockid)
stkpe = data.get('double_pe_ttm',-111)

#计算peg
stkpeg = stkpe/((compoundrate-1)*100)

print(compoundrate-1,stkpeg)
