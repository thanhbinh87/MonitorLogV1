'''
Created on Jan 25, 2011

@author: rucney
'''
#! coding: utf-8
# pylint: disable-msg=W0311
import time
from api import get_total, get_stats
from rrdtest import draw_graph, draw_total

def graph(group, t):
  data = get_stats(group, t)
  res = get_total(t)
  draw_graph(data, group)
  draw_total(res)
  
if __name__ == '__main__':
  while True:
    graph('hosting', 36000)
    graph('baamboo', 36000)
    graph('flv', 36000)
    time.sleep(300) 
  