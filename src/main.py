#! coding: utf-8
# pylint: disable-msg=W0311
import time
import api

def analysis():
  logs = api.fetch_info(1000000)
  for log in logs:
    time = log.get('time')
    print time
    time_used = log.get('time_used')
    print time_used
    time_list = range(time - time_used, time + 1)
    bytes_out = log.get('bytes_out') / (time_used + 1)
    bytes_in = log.get('bytes_in') / (time_used + 1)
    for i in time_list:
      api.incr(i, bytes_in, bytes_out)
      
def graph(t):
  t = time.time() - t
  data = api.get_stats(t)
  print data
  return data

if __name__ == "__main__":
#  analysis()
  a = []
  for i in graph(10000000):
    byteout =  i['bytes_out']
    a.append(i)
    api.insert(byteout)
    
#    print i['bytes_out']
  print len(a)