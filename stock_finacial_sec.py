# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 14:34:15 2017

@author: xuzhi
"""

#coding:utf-8  
  
import numpy as np
import pandas as pd
from sklearn import preprocessing
from datasource import estools


#df = pd.read_csv("../data/afin20170930.csv",header=0,dtype={'SW_FIRST_CODE':"str"})
conn = pymssql.connect(host="10.237.120.198", port="1433" ,user="wande", password="wande", database="cldb")
df = pd.read_sql("SELECT  TOP 10000 FI.S_INFO_WINDCODE,  LEFT(SIC.SW_IND_CODE,4) as SW_FIRST_CODE,\
		S_FA_ROE,                \
		S_FA_ROA2,						\
		S_FA_OPTOGR,					\
		S_FA_OCFTOOPERATEINCOME,      \
		S_FA_DEBTTOASSETS,				\
		S_FA_QUICK,					\
		S_FA_OCFTOSHORTDEBT,				\
		S_FA_INVTURN,      \
		S_FA_ARTURN,      \
		S_FA_CATURN,      \
		S_FA_FATURN,      \
		S_FA_ASSETSTURN,      \
		S_FA_YOYOP,			\
		S_FA_YOY_OR,			\
		S_FA_YOYEPS_BASIC		\
       FROM ASHAREFINANCIALINDICATOR FI LEFT JOIN (SELECT b.S_INFO_WINDCODE,SUBSTRING(b.SW_IND_CODE,1,4) AS SW_IND_CODE FROM  \
       ASHARESWINDUSTRIESCLASS b right join ASHAREINDUSTRIESCODE a         \
       on substring(a.INDUSTRIESCODE,1,4) = substring(b.SW_IND_CODE,1,4)   \
       where a.LEVELNUM='2' AND a.USED='1' AND b.REMOVE_DT is null  and b.S_INFO_WINDCODE is not null) SIC ON  FI.WIND_CODE = SIC.S_INFO_WINDCODE \
       WHERE FI.REPORT_PERIOD='20170930' AND (FI.S_INFO_WINDCODE LIKE '6%' OR FI.S_INFO_WINDCODE LIKE '0%' OR FI.S_INFO_WINDCODE LIKE '3%')",con=conn)


#预处理：删除行业空值行，根据decribe，代替不合理极值
#df['SW_FIRST_CODE']=[ str(a)[0:4] for a in df['SW_FIRST_CODE'] ]            ####这是处理列值的一种方法
df = df[df['SW_FIRST_CODE']!='nan']


df['SW_FIRST_CODE']=df['SW_FIRST_CODE'].apply(lambda x:str(x)[0:4])             ##使用一级行业

##根据dataframe的描述性统计量去除异常值     ,主要是为了画图好看些，  若不处理，绝对的排名是不受影响的
df['S_FA_OPTOGR']=df['S_FA_OPTOGR'].apply(lambda x: -524 if x<-524 else x )
df['S_FA_DEBTTOASSETS']=df['S_FA_DEBTTOASSETS'].apply(lambda x: 100 if x>100 else x )
df['S_FA_INVTURN']=df['S_FA_INVTURN'].apply(lambda x: 100 if x>100 else x )
df['S_FA_ARTURN']=df['S_FA_ARTURN'].apply(lambda x: 100 if x>100 else x )
df['S_FA_FATURN']=df['S_FA_FATURN'].apply(lambda x: 100 if x>100 else x )
df['S_FA_YOYOP']=df['S_FA_YOYOP'].apply(lambda x: 100 if x>100 else x )
df['S_FA_YOYOP']=df['S_FA_YOYOP'].apply(lambda x: -100 if x<-100 else x )

df['S_FA_YOY_OR']=df['S_FA_YOY_OR'].apply(lambda x: 100 if x>100 else x )

df['S_FA_YOYEPS_BASIC']=df['S_FA_YOYEPS_BASIC'].apply(lambda x: -100 if x<-100 else x )

df['S_FA_YOYEPS_BASIC']=df['S_FA_YOYEPS_BASIC'].apply(lambda x: 100 if x>100 else x )



#df = df.set_index(['S_INFO_WINDCODE'])
num_df = df.values[:,2:]                      #dataframe向numpy转化，去除索引S_INFO_WINDCODE及SW_FIRST_CODE


imp=preprocessing.Imputer(missing_values='NaN',strategy='median',axis=0)                #使用imputer作缺失值处理
imp.fit(num_df)                     #根据df计算模型参数
#print(df.head(2))  
df1=imp.transform(num_df)                             #缺失值处理    
df_nonull =  pd.DataFrame(df1,columns=df.columns.values[2:])

scaler = preprocessing.StandardScaler().fit(df1)          
zdf = scaler.transform(df1)                      #同理，标准化处理
zdf=pd.DataFrame(zdf,columns=df.columns.values[2:])

handle_df1 = pd.concat([df.iloc[:,0:2],df_nonull],axis=1)          #从列方向合并两个dataframe, 注意默认是行方向,产生处理过缺失值的个股表
handle_df = pd.concat([df.iloc[:,0:2],zdf],axis=1)            #从列方向合并两个dataframe, 注意默认是行方向,产生个股表

#计算每支股票财务四大能力
handle_df['profitability'] = handle_df['S_FA_ROE']*0.3314 + handle_df['S_FA_ROA2']*0.2455 + handle_df['S_FA_OPTOGR']*0.201 + handle_df['S_FA_OCFTOOPERATEINCOME']*0.222
handle_df['growthability'] = handle_df['S_FA_YOYOP']*0.3754 + handle_df['S_FA_YOY_OR']*0.3754 + handle_df['S_FA_YOYEPS_BASIC']*0.3754
handle_df['debtpayingability'] = handle_df['S_FA_DEBTTOASSETS']*0.3729 + handle_df['S_FA_QUICK']*0.3104 + handle_df['S_FA_OCFTOSHORTDEBT']*0.3104
handle_df['operationability'] = handle_df['S_FA_INVTURN']*0.3314 + handle_df['S_FA_ARTURN']*0.2455 + handle_df['S_FA_CATURN']*0.201 + handle_df['S_FA_ASSETSTURN']*0.222

#handle_df['growthability'].plot()
#计算行业财务四大能力中位数、ROE、YOYOP

grouped = handle_df1.groupby(handle_df1['SW_FIRST_CODE'])     
df_ind_roe_yoyop =  grouped.median()[["S_FA_ROE","S_FA_YOYOP"]]            ## 注意取多列，除了用iloc外，可以用list。
df_ind_count = grouped.count()[['S_INFO_WINDCODE']]
df_ind_count.columns=['stock_count']                  #注意改列名 

grouped1 = handle_df.groupby(handle_df['SW_FIRST_CODE'])
df_ind_other = grouped1.median()[["profitability","growthability","debtpayingability","operationability"]]  

df_ind = pd.merge(df_ind_other,df_ind_roe_yoyop,left_index=True,right_index=True)               #注意连接方法，左右使用索引
df_ind.columns =['ind_profitability', 'ind_growthability', 'ind_debtpayingability','ind_operationability', 'ind_S_FA_ROE','ind_S_FA_YOYOP']
stock_df = pd.merge(handle_df,df_ind,left_on='SW_FIRST_CODE',right_index=True)               #注意连接方法，左用字段，右使用索引
stock_df_all = pd.merge(stock_df,df_ind_count,left_on='SW_FIRST_CODE',right_index=True)

##有可能一个股票对应多个行业，这里先取一个，故有
stock_df_all = stock_df_all.drop_duplicates('S_INFO_WINDCODE')                   #此时，下面的公司X仅对一个行业

#确定行业公司内数，排名

def getnum(x):
    indid = list(stock_df_all[stock_df_all['S_INFO_WINDCODE']==x]['SW_FIRST_CODE'])[0]          #取得 公司x对应行业 ,注意有可能多个
    s_value =  list(stock_df_all[stock_df_all['S_INFO_WINDCODE']==x][s])[0]            #取得 公司x对应指标s,注意有可能多个
    
    li = list(stock_df_all[stock_df_all['SW_FIRST_CODE']==indid][s].sort_values(ascending=False))           ##取得对应行业公司的值，并排序
    return li.index(s_value)

s='S_FA_ROE'
stock_df_all['S_FA_ROE_RANK']=stock_df_all['S_INFO_WINDCODE'].apply(getnum)          ###!!此处时间复杂度N
s='S_FA_YOYEPS_BASIC'
stock_df_all['S_FA_YOYEPS_BASIC_RANK']=stock_df_all['S_INFO_WINDCODE'].apply(getnum)

stock_df_all.rename(columns={'SW_FIRST_CODE':'str_SW_FIRST_CODE'},inplace=True)
fortest = estools(host="10.237.2.132",index="airr_2018.01.17",doc_type="airr_mapping")
fortest.insertDataframeIntoElastic(stock_df_all,chunk_size = 2000)


##df2 = df.dropna(axis=0, how='all')
#grouped = df.groupby(df['SW_FIRST_CODE'])
#
##print(grouped.median().head(1),grouped.max().head(1),grouped.min().head(1),grouped.sum().head(1),grouped.mean().head(1),grouped.mean().head(1))
#
#df['S_FA_ROE'].describe()
#ndf = df['SW_FIRST_CODE']
#ndf['profit']=df['S_FF_ROE']*0.3314 + df['S_FA_ROA2']*0.2455 + df['S_FA_OPTOOR'] + 