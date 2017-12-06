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



class ASHAREINTRODUCTION(Base):
    __tablename__ = 'ASHAREINTRODUCTION'
    OBJECT_ID = Column(String,primary_key=True)
    S_INFO_CHINESEINTRODUCTION = Column(String)     ##0.0 公司简介
    S_INFO_WINDCODE = Column(String)
    
    def __init__(self):
        pass

    def __repr(self):
        return "<User('%s')>"%(self.S_INFO_CHINESEINTRODUCTION)


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

DB_Session = sessionmaker(bind=engine)
session = DB_Session()



class windata(object):
    
    
    def __init__(self):
        
        self.intro = ''  #简介
        
        #投资评级
        self.srating = ''     #评级
        self.est_price = ''    #一致性预测平均价格
        
        #行业评级
        self.indrating = ''
        
        
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
        res =session.query(ASHAREINTRODUCTION.S_INFO_WINDCODE).filter(ASHAREINTRODUCTION.S_INFO_WINDCODE.like('6%')).all()
        #or_(S_INFO_WINDCODE.like('6%'),S_INFO_WINDCODE.like('3%'),S_INFO_WINDCODE.like('0%'))
        
        self.stocklist=[ str(a)[2:-3] for a in res]
        
        return self.stocklist
    
class windes(object):
    def __init__(self,windcode='600519.SH'):
        pass
    
if __name__ == '__main__':
    
    import time
    t0 = time.time()
    wd = windata()
    
    
    #print("intro:",wd.get_intro(),wd.get_srating_price(),wd.get_indrating()) 
    todo = wd.get_a_stocklist()[0:10]
            
    for stockid in todo:
        print("intro:",stockid,wd.get_intro(stockid),wd.get_srating_price(stockid),wd.get_indrating(stockid)) 
    
    print("Total time getting data:%s"%str(time.time()-t0))