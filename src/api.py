#! coding: utf-8
# pylint: disable-msg=W0311
import time
import pymongo
import settings


DATABASE = pymongo.Connection(settings.mongodb_nodes).infoging.info
GRAPH = pymongo.Connection(settings.mongodb_nodes).infoging.graph

def insert(info):
  time = info.get('time')
  time_used = info.get('time_used')
  time_list = range(time - time_used, time + 1)
  bytes_out = info.get('bytes_out') / (time_used + 1)
  bytes_in = info.get('bytes_in') / (time_used + 1)
  group = info.get('group')
  for i in time_list:
    GRAPH.update({"time": time, 'group': group}, 
                    {"$inc": {"bytes_out": bytes_out,
                              "bytes_in": bytes_in,
                              'request': 1}}, 
                    upsert=True)
    
  return DATABASE.insert(info)

  
def get_stats(group, t):
  t0 = time.time()
  t1 = t0 - t
  data = list(GRAPH.find({"time": {"$gte": t1}, 'group':group}))
  times = [i.get('time') for i in data]
  print len(times)
  print times
  print times[-1] - times[0]
#  for i in range(t1, t0):
#    if i not in times:
#      data.append({"time": i, "group": group, "bytes_out": 0, "bytes_in": 0, "request": 0})
#  print len(data)
  return data
  
#time>time
if __name__ == "__main__": 
  get_stats('hosting', 3600)