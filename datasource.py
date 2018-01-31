# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 14:57:23 2017

@author: xuzhi
"""


from elasticsearch import Elasticsearch
import json
import requests

class estools(object):
    def __init__(self,host,index,doc_type,port='9200'):
        self.host = host
        self.port = port
        self.es = es = Elasticsearch([{'host':host,'port':port}])
        self.index = index
        self.doc_type = doc_type
    
    def upsert(self,index,doc_type,id,body):
        
        self.es.update(index,doc_type,id,{"doc":body,"upsert":body})
        
    def getkv(self,index,doc_type,id):
        ##待增加处理id不存在的情况
        data = self.es.get(index,doc_type,id=id)
        return data['_source']

    
    #post批量插入
    def insertDataframeIntoElastic(self,dataFrame,chunk_size = 2000):
        headers = {'content-type': 'application/x-ndjson', 'Accept-Charset': 'UTF-8'}
        records = dataFrame.to_dict(orient='records')
        
        #索引
#       actions = ["""{ "index" : { "_index" : "%s", "_type" : "%s","_id":"%s"} }\n""" % (self.index, self.doc_type,records[j]['S_INFO_WINDCODE']) +json.dumps(records[j])
#                        for j in range(len(records))]
        #upsert          ##注意\n为何要放在下个串，；注意doc_
        actions = ["""{ "update" : { "_index" : "%s", "_type" : "%s","_id":"%s"} }"""%(self.index, self.doc_type,records[j]['S_INFO_WINDCODE'])+"""\n{"doc":%s,"doc_as_upsert":true}"""%(json.dumps(records[j])) for j in range(len(records))]        
        #print(actions)
        i=0
        while i<len(actions):
            serverAPI = "http://"+self.host + ':9200/_bulk' 
            data='\n'.join(actions[i:min([i+chunk_size,len(actions)])])
            data = data + '\n'
            r = requests.post(serverAPI, data = data, headers=headers)
            print(r.content)
            i = i+chunk_size

##https://stackoverflow.com/questions/25186148/creating-dataframe-from-elasticsearch-results
#    def search_and_export_to_dict(self, *args, **kwargs):
#        _id = kwargs.pop('_id', True)
#        data_key = kwargs.pop('data_key', kwargs.get('fields')) or '_source'
#        kwargs = dict({'index': self.index, 'doc_type': self.doc_type}, **kwargs)
#        if kwargs.get('size', None) is None:
#            kwargs['size'] = 1
#            t = self.es.search(*args, **kwargs)
#            kwargs['size'] = t['hits']['total']
#
#        return get_search_hits(self.es.search(*args, **kwargs), _id=_id, data_key=data_key)
#
#    def search_and_export_to_df(self, *args, **kwargs):
#        convert_numeric = kwargs.pop('convert_numeric', True)
#        convert_dates = kwargs.pop('convert_dates', 'coerce')
#        df = pd.DataFrame(self.search_and_export_to_dict(*args, **kwargs))
#        if convert_numeric:
#            df = df.convert_objects(convert_numeric=convert_numeric, copy=True)
#        if convert_dates:
#            df = df.convert_objects(convert_dates=convert_dates, copy=True)
#        return df
#
#    def get_search_hits(es_response, _id=True, data_key=None):
#        response_hits = es_response['hits']['hits']
#        if len(response_hits) > 0:
#            if data_key is None:
#                for hit in response_hits:
#                    if '_source' in hit.keys():
#                        data_key = '_source'
#                        break
#                    elif 'fields' in hit.keys():
#                        data_key = 'fields'
#                        break
#                if data_key is None:
#                    raise ValueError("Neither _source nor fields were in response hits")
#    
#            if _id is False:
#                return [x.get(data_key, None) for x in response_hits]
#            else:
#                return [dict(_id=x['_id'], **x.get(data_key, {})) for x in response_hits]
#        else:
#            return []




if __name__ == '__main__':
    fortest = estools(host="10.237.2.132",index="airr_2017.12.6",doc_type="airr_mapping")
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
    
    print(fortest.getkv("600309","airr_2017.12.6","airr_mapping"))