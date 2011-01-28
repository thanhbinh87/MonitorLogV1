'''
Created on Jan 25, 2011

@author: rucney
'''
#! coding: utf-8
# pylint: disable-msg=W0311
import time
from api import get_total, get_stats
from rrd import graphrrd

def graph(group, t):
  """draw graph by t, group"""
  
  data = get_stats(group, t)
  res = get_total(t)
  graphrrd(data, res, group)
  
if __name__ == '__main__':
  while True:
    graph('hosting', 3600)
    print 'done'
    time.sleep(300) 
    