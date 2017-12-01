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
class windata(object):
    
    from sqlalchemy.orm import sessionmaker
    DB_Session = sessionmaker(bind=engine)
    session = DB_Session()
    
    def __init__(self,windcode='600519.SH'):
        
        
        self.windcode = windcode 
        self.intro = ''  #简介
        
        #投资评级
        self.srating = ''     #评级
        self.est_price = ''    #一致性预测平均价格
        
        #行业评级
        self.indrating = ''
        
        
    def get_intro(self):
        self.intro = session.query(ASHAREINTRODUCTION).filter_by(S_INFO_WINDCODE=self.windcode).first().S_INFO_CHINESEINTRODUCTION  #简介
        return self.intro
        
    def get_srating_price(self):
        rating = session.query(ASHARESTOCKRATINGCONSUS).filter_by(S_INFO_WINDCODE=self.windcode,S_WRATING_CYCLE='263002000').order_by(desc('RATING_DT')).first()
        self.srating = rating.S_WRATING_AVG     #评级
        self.est_price = rating.S_EST_PRICE    #一致性预测平均价格
        return self.srating,self.est_price
    
    def get_indrating(self):
        #行业评级,使用RAW SQL
        sql = "select avg(score) from (select top 10 SCORE,RATING from ASHAREINDUSRATING \
        where wind_ind_code=(select wind_ind_code from AShareIndustriesClass where S_INFO_WINDCODE='%s') order by rating_dt desc) as score"%(self.windcode)
        self.indrating = session.execute(sql).scalar()
        
        return self.indrating
    
if __name__ == '__main__':
    
    import time
    t0 = time.time()
    wd = windata('600519.SH')
    
    
    print("intro:",wd.get_intro(),wd.get_srating_price(),wd.get_indrating())
    
    
    print("Total time getting data:%s"%str(time.time()-t0))