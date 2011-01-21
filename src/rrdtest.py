'''
Created on Jan 18, 2011

@author: rucney
'''
#! coding: utf-8
# pylint: disable-msg=W0311

import time

from pyrrd.rrd import RRD, RRA, DS
from pyrrd.graph import DEF, CDEF, VDEF
from pyrrd.graph import LINE, GPRINT
from pyrrd.graph import ColorAttributes, Graph
#create file name
def drawgraph(data):
  
  exampleNum = 2
  filename = 'speed%s.rrd' % exampleNum
  graphfile = 'speed%s.png' % exampleNum
  graphfileLg = 'speed%s-large.png' % exampleNum
  
  #define times
  hour = 60 * 60
  day = 24 * 60 * 60
  week = 7 * day
  month = day * 30
  quarter = month * 3
  half = 365 * day / 2
  year = 365 * day
  timex = 3 * hour
  step = 10
  endTime = int(time.time())
  startTime = endTime - 2592000
  
  # create RRD file
  dss = []
  ds1 = DS(dsName='bytes_out', dsType='ABSOLUTE', heartbeat=300)
  ds2 = DS(dsName='bytes_in', dsType='ABSOLUTE', heartbeat=300)
  ds3 = DS(dsName='request', dsType='ABSOLUTE', heartbeat=300)
  dss.extend([ds1, ds2, ds3])
  
  rras = []
  rra1 = RRA(cf='AVERAGE', xff=0.5, steps=1, rows=1440)
  rra2 = RRA(cf='AVERAGE', xff=0.5, steps=5, rows=2016)
  rra3 = RRA(cf='AVERAGE', xff=0.5, steps=60, rows=720)
  rras.extend([rra1, rra2, rra3])
  
  myRRD = RRD(filename, step = 5, ds=dss, rra=rras, start=startTime)
  myRRD.create(debug=False)
  

  couter = 0
  a = []
  b = []
  c = []
  d = []
  for i in data:
    couter += 1
    bytes_in = i['bytes_in'] 
    bytes_out = i['bytes_out'] 
    requests = i['request'] 
    d.append(requests)
    b.append(bytes_in)
    c.append(bytes_out)
    times = i['time'] 
    a.append(times)
    myRRD.bufferValue(times, bytes_out, bytes_in, requests)
    if couter % 50 == 0:
      myRRD.update(debug=True)
  myRRD.update(debug=True)
  # make RRD graph.
  def1 = DEF(rrdfile=myRRD.filename, vname='output', dsName=ds1.name)
  def2 = DEF(rrdfile=myRRD.filename, vname='input', dsName=ds2.name)
  def3 = DEF(rrdfile=myRRD.filename, vname='request', dsName=ds3.name)
  
#  cdef1 = CDEF(vname='outbits', rpn='%s,8,*' % def1.vname)
#  vdef2 = VDEF(vname='max', rpn='%s,MAXIMUM' % cdef1.vname)
#  vdef1 = VDEF(vname='avg', rpn='%s,AVERAGE' % cdef1.vname)
#  vdef3 = VDEF(vname='min', rpn='%s,MINIMUM' % cdef1.vname)
  line1 = LINE(1, defObj=def1, color='#2029CC', legend='Out traffic')
  line2 = LINE(1, defObj=def2, color='#00FF00', legend='In traffic')
  line3 = LINE(1, defObj=def3, color='#FF0000', legend='Requests')
#  gprint1 = GPRINT(vdef1, 'Max\\: %5.1lf %Sbps')
#  gprint2 = GPRINT(vdef2, 'Avg\\: %5.1lf %Sbps')
#  gprint3 = GPRINT(vdef3, 'Min\\: %5.1lf %Sbps')
  
  # ColorAttributes
  ca = ColorAttributes()
  ca.back = '#CCCDE2'  #background
  ca.canvas = '#FFFFFF'#the background of the actual graph
  ca.shadea = '#000000'#left and top border
  ca.shadeb = '#111111'#right and bottom border
  ca.mgrid = '#6666CC' #major grid
  ca.axis = '#000000'  #axis of the graph
  ca.frame = '#CCCDE2' #line around the color spots
  ca.font = '#000000'  #color of the font
  ca.arrow = '#CC0000' # arrow head pointing up and forward
  
  
  g = Graph(graphfile, end=endTime, vertical_label='Bytes/s', color=ca)
  g.data.extend([def1, def2, def3, line1, line2, line3])
  g.title = '"report traffic ouput"'


  g.start=endTime - timex
#  g.step = step
  g.width = 397
  g.height = 182
  g.write(debug=False)
  
  g.filename = graphfileLg
  g.width = 800
  g.height = 400
  g.write()

