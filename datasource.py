# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 14:57:23 2017

@author: xuzhi
"""


from elasticsearch import Elasticsearch

class estools(object):
    def __init__(self,host,port='9200'):
        self.host = host
        self.port = port
        self.es = es = Elasticsearch([{'host':host,'port':port}])
    
    def upsert(self,index,doc_type,id,body):
        
        self.es.update(index,doc_type,id,{"doc":body,"upsert":body})
        
    def getkv(self,index,doc_type,id):
        data = self.es.get(index=index,doc_type=doc_type,id=id)
        return data['_source']



if __name__ == '__main__':
    fortest = estools("10.237.2.132")
#    body={
#            "@timestamp":"2017-12-06",
#            "date_airr":"2017-12-06T11:18:17.136+0800",
#            "long_reporttime":6.1,
#            "long_reporttime_1":6.0,
#            "astr_intro":"Some People say hi!",
#            "str_intro2":"Some People say no",
#            "bool_rate":"false",
#            "double_price_2":1,
#            "date_airr_3":"2013-08-03"
#            }
#    fortest.upsert("airr_2017.12.6","airr_mapping","600309",body)
    
    print(fortest.getkv("airr_2017.12.6","airr_mapping","600309"))