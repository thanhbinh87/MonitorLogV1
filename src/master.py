'''
Created on Dec 29, 2010

@author: rucney
'''
#! coding: utf-8
# pylint: disable-msg=W0311, E1101
import time
import re
import tasklog

def parse_log(line=None):
  """ parse log :{time:bytes_out:bytes_in:group...}"""
  
  parts = [
      r'(?P<remote_host>\S+)',            # host %h
      r'\[(?P<time>.+)\]',                # time %t
      r'"(?P<request>.+)"',               # request "%r"
      r'(?P<status>[0-9]+)',              # status %>s
      r'(?P<size>\S+)',                   # size %b (careful, can be '-')
      r'"(?P<referer>.*)"',               # referer "%{Referer}i"
      r'"(?P<agent>.*)"',                 # user agent "%{User-agent}i"
      r'(?P<bytes_in>\S+)',               # %I   
      r'(?P<bytes_out>\S+)',              # %O   
      r'(?P<time_used>\S+)'               # %T  
  ]
  pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')
     
  m = pattern.match(line)
  res = m.groupdict()
  res["status"] = int(res["status"])
  res["group"] = res["request"].split('?')[-1].split('&')[0].split('=')[-1]  
  res["bytes_out"] = int(res["bytes_out"])
  res["time_used"] = int(res["time_used"])
  
  if res["size"] == "-":
    res["size"] = 0
  else:
    res["size"] = int(res["size"])
  
  if res["bytes_in"] == "-":
    res["bytes_in"] = 0
  else:
    res["bytes_in"] = int(res["bytes_in"])
  
  if res["referer"] == "-":
    res["referer"] = None

  tt = time.strptime(res["time"][:-6], "%d/%b/%Y:%H:%M:%S")
  res["time"] = int(time.mktime(tt))
  
  return res

if __name__ == "__main__":
  while True:
    if int(time.time()) % 60 == 0:
      tasklog.fetch_logs.delay() #@UndefinedVariable
    time.sleep(1)
    print 'done'
  