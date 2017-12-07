# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 14:47:41 2017

@author: xuzhi
"""

#创建连接池
from sqlalchemy import create_engine

DB_CONNECT_STRING = 'mssql+pymssql://wande:wande@10.101.221.183/wande?charset=utf8'
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

#公布重要财务指标
class AShareANNFinancialIndicator(Base):
    __tablename__ = 'AShareANNFinancialIndicator'
    OBJECT_ID = Column(String,primary_key=True)
    ROE_diluted = Column(String)     
    REPORT_PERIOD  = Column(String)  
    S_INFO_WINDCODE = Column(String)

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
        
        self.intro = ''  #简介
        
        #投资评级
        self.srating = -1.0     #评级
        self.est_price = -1.0   #一致性预测平均价格
        
        #行业评级
        self.indrating = -1.0
        self.roe5 = []
        
    def get_intro(self,windcode='600519.SH'):
        self.intro = session.query(ASHAREINTRODUCTION).filter_by(S_INFO_WINDCODE=windcode).first().S_INFO_CHINESEINTRODUCTION  #简介
        return self.intro
        
    def get_srating_price(self,windcode='600519.SH'):
        rating = session.query(ASHARESTOCKRATINGCONSUS).filter_by(S_INFO_WINDCODE=windcode,S_WRATING_CYCLE='263002000').order_by(desc('RATING_DT')).first()
        if rating != None:
            self.srating = rating.S_WRATING_AVG     #评级
            self.est_price = rating.S_EST_PRICE    #一致性预测平均价格
            return self.srating,self.est_price
    
    def get_indrating(self,windcode='600519.SH'):
        #行业评级,使用RAW SQL
        sql = "select avg(score) from (select top 10 SCORE,RATING from ASHAREINDUSRATING \
        where wind_ind_code=(select top 1 wind_ind_code from AShareIndustriesClass where S_INFO_WINDCODE='%s') order by rating_dt desc) as score"%(windcode)
        self.indrating = session.execute(sql).scalar()
        
        return self.indrating
        
    #返回A股票列表
    def get_a_stocklist(self):
        res =session.query(ASHAREINTRODUCTION.S_INFO_WINDCODE).filter(or_(ASHAREINTRODUCTION.S_INFO_WINDCODE.like('6%'),ASHAREINTRODUCTION.S_INFO_WINDCODE.like('3%'),ASHAREINTRODUCTION.S_INFO_WINDCODE.like('0%'))).all()
        #or_(S_INFO_WINDCODE.like('6%'),S_INFO_WINDCODE.like('3%'),S_INFO_WINDCODE.like('0%'))
        
        self.stocklist=[ str(a)[2:-3] for a in res]           #可以通过下标来取sqlalchemy.util._collections.result类型
        
        return self.stocklist
    
    #ROE
    def get_roe(self,windcode='600519.SH'):
        res =session.query(AShareANNFinancialIndicator.ROE_diluted,AShareANNFinancialIndicator.REPORT_PERIOD).filter(and_(AShareANNFinancialIndicator.REPORT_PERIOD.like('%0930'),AShareANNFinancialIndicator.S_INFO_WINDCODE==windcode)).order_by(desc('REPORT_PERIOD')).limit(5)
        self.roe5 = [ a[0] for a in res]          #取5个ROE值
        return self.roe5  

from datasource import estools

class windes(object):
    def __init__(self,server="10.237.2.132"):
        self.es = estools(server)
    
    #处理wind中所有A股
    def atoes(self):
        wd = windata()

        todo = wd.get_a_stocklist()
        
        for stockid in todo:
                self.stocktoes(stockid)
       
    def stocktoes(self,stockid):
        wd.get_intro(stockid)
        wd.get_srating_price(stockid)
        wd.get_indrating(stockid)
        
        body={
                "@timestamp":"2017-12-07",
                "date_airr":"2017-12-07T10:07:17.136+0800",
                "astr_intro":wd.intro,
                "double_srating":wd.srating,
                "double_est_price":wd.est_price,
                "double_indrating":wd.indrating
                }     
        self.es.upsert("airr_2017.12.7","airr_mapping",stockid,body)            
        
        
if __name__ == '__main__':
    
    import time
    t0 = time.time()
    wd = windata()
    wdes = windes()   
    
    #print("intro:",wd.get_intro(),wd.get_srating_price(),wd.get_indrating()) 
    wd.get_roe()
    
    print("Total time getting data:%s"%str(time.time()-t0))