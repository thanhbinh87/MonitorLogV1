'''
Created on Jan 25, 2011

@author: rucney
'''
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
    graph('hosting', 3600)
    print 'done'
    time.sleep(300) 
    
#import time
#from api import get_total
#from testrrd import draw_total
#
#def graph(t):
#  res = get_total(t)
#  draw_total(res)
#  
#if __name__ == '__main__':
#  graph(36000)