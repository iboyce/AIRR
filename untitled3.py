# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 14:34:15 2017

@author: xuzhi
"""

#coding:utf-8  
  

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
    S_INFO_CHINESEINTRODUCTION = Column(String) #这里的String可以指定长度，比如：String(20)
    S_INFO_WINDCODE = Column(String)
    
    def __init__(self):
        pass

    def __repr(self):
        return "<User('%s')>"%(self.S_INFO_CHINESEINTRODUCTION)

Base.metadata.create_all(engine)



#创建连接 
from sqlalchemy.orm import sessionmaker
DB_Session = sessionmaker(bind=engine)
session = DB_Session()


print(session.query(ASHAREINTRODUCTION).filter_by(S_INFO_WINDCODE='600519.SH').first().S_INFO_CHINESEINTRODUCTION)
