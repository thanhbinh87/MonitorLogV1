#! coding: utf-8
# pylint: disable-msg=W0311
import time
import api

def analysis():
  logs = api.fetch_info(3600)
  for log in logs:
    print log
    time = log.get('time')
    time_used = log.get('time_used')
    time_list = range(time - time_used, time + 1)
    bytes_out = log.get('bytes_out') / (time_used + 1)
    bytes_in = log.get('bytes_in') / (time_used + 1)
    group = log.get('group')
    
    for i in time_list:
      api.incr(group, i, bytes_in, bytes_out)




if __name__ == "__main__":
  while True:
    analysis()
    time.sleep(60)