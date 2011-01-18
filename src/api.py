#! coding: utf-8
# pylint: disable-msg=W0311
import time
import pymongo
import settings


DATABASE = pymongo.Connection(settings.mongodb_nodes).Logging.RRD
CACHE = pymongo.Connection(settings.mongodb_nodes).Logging.cache
BYTEOUT = pymongo.Connection(settings.mongodb_nodes).Logging.byteout

def insert(info):
  return DATABASE.insert(info)

def fetch_info(t, group=None):
  """ time = 3600s 
  time = 24 * 60 *60 
  """
  t1 = time.time() - t
  if not group:
    info = DATABASE.find({"time": {"$gte": t1}})
  else:
    info = DATABASE.find({"time": {"$gte": t1}, "group": group})
  return info

def incr(time, bytes_in, bytes_out):
  return CACHE.update({"time": time}, 
                      {"$inc": {"bytes_out": bytes_out,
                                "bytes_in": bytes_in}}, 
                      upsert=True)
  
def get_stats(t):
  return CACHE.find({"time": {"$gte": t}})

if __name__ == "__main__": 
  for i in DATABASE.find():
    print i  