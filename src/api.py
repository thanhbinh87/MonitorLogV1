'''
Created on Jan 19, 2011

@author: rucney
'''
#! coding: utf-8
# pylint: disable-msg=W0311
import time
import pymongo
import settings


DATABASE = pymongo.Connection(settings.MONGODB_NODE).infoging.info
GRAPH = pymongo.Connection(settings.MONGODB_NODE).infoging.graph

def insert(info):
  """ insert to database"""
  
  time = info.get('time')
  time_used = info.get('time_used')
  time_list = range(time - time_used, time + 1)
  bytes_out = info.get('bytes_out') / (time_used + 1)
  bytes_in = info.get('bytes_in') / (time_used + 1)
  group = info.get('group')
  for i in time_list:
    GRAPH.update({"time": i, 'group': group}, 
                    {"$inc": {"bytes_out": bytes_out,
                              "bytes_in": bytes_in,
                              'request': 1}}, upsert = True)
  return DATABASE.insert(info)

def get_total(t):
  """ mongodb group by """
  t0 = int(time.time())
  t1 = t0 - t
  res = GRAPH.group(key={"time": True},
  condition={"time": {"$gte": t1}},
  initial={'bytes_out': 0, 'bytes_in': 0, 'request': 0},
  reduce="function(info, prev) { prev.bytes_out += info.bytes_out; \
  prev.bytes_in +=info.bytes_in; prev.request += info.request }"
  )
  res.sort(key=lambda k: k['time'])
  return res

def get_stats(group, t):
  """ mongodb time, group"""
  
  t0 = int(time.time())
  t1 = t0 - t
  data = list(GRAPH.find({"time": {"$gte": t1}, 'group':group})) 
  data.sort(key=lambda k: k['time'])
  return data
