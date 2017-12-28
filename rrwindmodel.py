# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 14:47:41 2017

@author: xuzhi
"""

#创建连接池
from sqlalchemy import create_engine

DB_CONNECT_STRING = 'mssql+pymssql://wande:wande@10.237.120.198/cldb?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, echo=True)



#映射表
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column,Integer,String


#介绍
class ASHAREINTRODUCTION(Base):
    __tablename__ = 'ASHAREINTRODUCTION'
    OBJECT_ID = Column(String,primary_key=True)
    S_INFO_CHINESEINTRODUCTION = Column(String)     ##0.0 公司简介
    S_INFO_WINDCODE = Column(String)
    
    def __init__(self):
        pass

    def __repr(self):
        return "<User('%s')>"%(self.S_INFO_CHINESEINTRODUCTION)

#财务指标
class ASHAREFINANCIALINDICATOR(Base):
    __tablename__ = 'ASHAREFINANCIALINDICATOR'
    OBJECT_ID = Column(String,primary_key=True)
    S_FA_ROE = Column(String)     
    REPORT_PERIOD  = Column(String)  
    S_INFO_WINDCODE = Column(String)
    S_FA_YOYEPS_BASIC = Column(String)

#一致性评级
class ASHARESTOCKRATINGCONSUS(Base):
    __tablename__ = 'ASHARESTOCKRATINGCONSUS'
    OBJECT_ID = Column(String,primary_key=True)
    S_WRATING_AVG = Column(String)  #评级
    S_EST_PRICE = Column(String)    #一致性预测 
    S_WRATING_CYCLE  = Column(String)    #周期30，90，180
    S_INFO_WINDCODE = Column(String)



#Base.metadata.create_all(engine)
from sqlalchemy import desc
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from sqlalchemy import and_

DB_Session = sessionmaker(bind=engine)
session = DB_Session()



class windata(object):
    
    
    def __init__(self):
        
        self.astr_intro = -111  #简介
        
        #投资评级
        self.double_srating = -111     #评级
        self.double_est_price = -111   #一致性预测平均价格
        
        #行业评级
        self.double_indrating = -111
        self.array_roe_diluted5 = []
        self.double_yoy_eps  = []
        self.str_windindname = -111
        self.double_pe_ttm = -111
        self.double_pb = -111
        
        self.array_zj_time  = []
        self.array_zj_ex = []
        self.array_zj_large = []
        self.array_zj_med = []
        self.array_zj_small = []
        
        
    def get_intro(self,windcode='600519.SH'):
        self.astr_intro = session.query(ASHAREINTRODUCTION).filter_by(S_INFO_WINDCODE=windcode).first().S_INFO_CHINESEINTRODUCTION  #简介
        return self.astr_intro
        
    def get_srating_price(self,windcode='600519.SH'):
        rating = session.query(ASHARESTOCKRATINGCONSUS).filter_by(S_INFO_WINDCODE=windcode,S_WRATING_CYCLE='263002000').order_by(desc('RATING_DT')).first()
        if rating != None:
            self.double_srating = rating.S_WRATING_AVG     #评级
            self.double_est_price = rating.S_EST_PRICE    #一致性预测平均价格
            return self.double_srating,self.double_est_price
    
    def get_windindname(self,windcode='600519.SH'):
        sql =  "select   top 1 INDUSTRIESNAME from ASHAREINDUSTRIESCODE where INDUSTRIESCODE=( select top 1  WIND_IND_CODE from ASHAREINDUSTRIESCLASS where S_INFO_WINDCODE='%s')"%(windcode)
        self.str_windindname = session.execute(sql).scalar()
        return self.str_windindname
        
    def get_indrating(self,windcode='600519.SH'):
        #行业评级,使用RAW SQL
        sql = "select avg(SCORE) from (select top 10 SCORE,RATING from ASHAREINDUSRATING \
        where WIND_IND_CODE=(select top 1 WIND_IND_CODE from ASHAREINDUSTRIESCLASS where S_INFO_WINDCODE='%s') order by RATING_DT desc) as score"%(windcode)
        self.double_indrating = session.execute(sql).scalar()
        
        return self.double_indrating
        
    #返回A股票列表
    def get_a_stocklist(self):
        res =session.query(ASHAREINTRODUCTION.S_INFO_WINDCODE).filter(or_(ASHAREINTRODUCTION.S_INFO_WINDCODE.like('6%'),ASHAREINTRODUCTION.S_INFO_WINDCODE.like('3%'),ASHAREINTRODUCTION.S_INFO_WINDCODE.like('0%'))).all()
        #or_(S_INFO_WINDCODE.like('6%'),S_INFO_WINDCODE.like('3%'),S_INFO_WINDCODE.like('0%'))
        
        self.stocklist=[ str(a)[2:-3] for a in res]           #可以通过下标来取sqlalchemy.util._collections.result类型
        
        return self.stocklist
    
    #ROE
    def get_roe(self,windcode='600519.SH'):
        res =session.query(ASHAREFINANCIALINDICATOR.S_FA_ROE,ASHAREFINANCIALINDICATOR.REPORT_PERIOD).filter(and_(ASHAREFINANCIALINDICATOR.REPORT_PERIOD.like('%0930'),ASHAREFINANCIALINDICATOR.S_INFO_WINDCODE==windcode)).order_by(desc('REPORT_PERIOD')).limit(5)
        if res != None:
            self.array_roe_diluted5 = [ a[0] for a in res]          #取5个ROE值
            return self.array_roe_diluted5 
       
    #YOYEES
    def get_yoy_eps(self,windcode='600519.SH'):
        res =session.query(ASHAREFINANCIALINDICATOR.S_FA_YOYEPS_BASIC,ASHAREFINANCIALINDICATOR.REPORT_PERIOD).filter(and_(ASHAREFINANCIALINDICATOR.REPORT_PERIOD.like('%0930'),ASHAREFINANCIALINDICATOR.S_INFO_WINDCODE==windcode)).order_by(desc('REPORT_PERIOD')).limit(5)
        if res != None:
            self.double_yoy_eps = [ a[0] for a in res]          #取5个ROE值
            return self.double_yoy_eps     
    
    def get_pepb(self,windcode='600519.SH'):
        sql ="select top 1 S_VAL_PE_TTM,S_VAL_PB_NEW from ASHAREEODDERIVATIVEINDICATOR where  S_INFO_WINDCODE='%s' and TRADE_DT = convert(varchar, GETDATE()-1, 112)"%(windcode)
        res = [d for d in session.execute(sql)]         #取得行列表
        #print(res)
        if len(res)>0:
            self.double_pe_ttm = res[0][0]
            self.double_pb = res[0][1]
            return self.double_pe_ttm,self.double_pb
        
        
    def get_zj(self,windcode='600519.SH'):
        sql = " select top 15 TRADE_DT, BUY_VALUE_EXLARGE_ORDER,SELL_VALUE_EXLARGE_ORDER,BUY_VALUE_LARGE_ORDER,SELL_VALUE_LARGE_ORDER,BUY_VALUE_MED_ORDER,SELL_VALUE_MED_ORDER,BUY_VALUE_SMALL_ORDER,SELL_VALUE_SMALL_ORDER \
                from ASHAREMONEYFLOW a where  S_INFO_WINDCODE='%s' and TRADE_DT > convert(varchar, GETDATE()-15, 112) order by a.TRADE_DT"%(windcode)
        res = session.execute(sql)
        
        
        if res != None:
            res = [ list(e) for e in res ]
            
            if len(res)==0:
                return None
            
            data = zip(*res)
            
            #print(res,data)
            
            self.array_zj_time = list(next(data))
            #print(self.pepb_time)
            BUY_VALUE_EXLARGE_ORDER =  list(next(data))
            SELL_VALUE_EXLARGE_ORDER =  list(next(data)) 
            #print("BUY_VALUE_EXLARGE_ORDER",BUY_VALUE_EXLARGE_ORDER)
            self.array_zj_ex = list(map(lambda x: x[0]-x[1], zip(BUY_VALUE_EXLARGE_ORDER, SELL_VALUE_EXLARGE_ORDER))) #BUY_VALUE_EXLARGE_ORDER - SELL_VALUE_EXLARGE_ORDER
            BUY_VALUE_LARGE_ORDER  =  list(next(data) )
            SELL_VALUE_LARGE_ORDER  = list( next(data)) 
            self.array_zj_large = list(map(lambda x: x[0]-x[1], zip(BUY_VALUE_LARGE_ORDER, SELL_VALUE_LARGE_ORDER))) #BUY_VALUE_LARGE_ORDER - SELL_VALUE_LARGE_ORDER
            BUY_VALUE_MED_ORDER  =  list(next(data) )
            SELL_VALUE_MED_ORDER  =  list(next(data) )
            self.array_zj_med =  list(map(lambda x: x[0]-x[1], zip(BUY_VALUE_MED_ORDER, SELL_VALUE_MED_ORDER)))#BUY_VALUE_MED_ORDER - SELL_VALUE_MED_ORDER
            BUY_VALUE_SMALL_ORDER  =  list(next(data) )
            SELL_VALUE_SMALL_ORDER  =  list(next(data) )
            self.array_zj_small =  list(map(lambda x: x[0]-x[1], zip(BUY_VALUE_SMALL_ORDER, SELL_VALUE_SMALL_ORDER)))#BUY_VALUE_SMALL_ORDER - SELL_VALUE_SMALL_ORDER
            
            return  self.array_zj_time,self.array_zj_ex,self.array_zj_large,self.array_zj_med,self.array_zj_small
        

from datasource import estools

class windes(object):
    def __init__(self,server="10.237.2.132"):
        self.es = estools(host="10.237.2.132",index="airr_2017.12.6",doc_type="airr_mapping")
    
    #处理wind中所有A股
    def atoes(self,index="airr_2017.12.6",doc_type="airr_mapping"):
        wd = windata()

        todo = wd.get_a_stocklist()
        
        for stockid in todo:
                self.stocktoes(stockid,index=index,doc_type=doc_type)
       
    def stocktoes(self,stockid="600519.SH",index="airr_2017.12.6",doc_type="airr_mapping"):
        wd.get_intro(stockid)
        wd.get_srating_price(stockid)
        wd.get_indrating(stockid)
        wd.get_windindname(stockid)
        wd.get_roe(stockid)
        wd.get_zj(stockid)
        wd.get_pepb(stockid)
        wd.get_yoy_eps(stockid)
        
        body={
                "@timestamp":"2017-12-08",
                "date_airr":"2017-12-08T18:48:17.136+0800",
                "astr_intro":wd.astr_intro,
                "double_srating":wd.double_srating,
                "double_est_price":wd.double_est_price,
                "double_indrating":wd.double_indrating,
                "str_windindname":wd.str_windindname,
                "array_roe_diluted5":wd.array_roe_diluted5,
                "double_yoy_eps":wd.double_yoy_eps,
                "double_pe_ttm":wd.double_pe_ttm,
                "double_pb":wd.double_pb,
                "array_zj_time":wd.array_zj_time,
                "array_zj_ex":wd.array_zj_ex,
                "array_zj_large":wd.array_zj_large,
                "array_zj_med":wd.array_zj_med,
                "array_zj_small":wd.array_zj_small
                
                }     
        print(body)
        self.es.upsert(index,doc_type,stockid,body)            
        
        
if __name__ == '__main__':
    
    import time
    t0 = time.time()
    wd = windata()
    wdes = windes()   
    
    #print("intro:",wd.get_intro(),wd.get_srating_price(),wd.get_indrating()) 
    #cc=wd.get_zj()
    #wdes.stocktoes("600519.SH")
    #c=wd.get_indrating("600519.SH")
    #cc=wd.get_windindname("600519.SH")
    #cc=wd.get_pepb()
    wdes.atoes(index="airr_2017.12.21",doc_type="airr_mapping")
    #wdes.stocktoes(stockid="600519.SH",index="airr_2017.12.21",doc_type="airr_mapping")
    #cc=wd.get_yoy_eps()
    print("Total time getting data:%s"%str(time.time()-t0))