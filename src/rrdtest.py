'''
Created on ian 18, 2011

@author: rucney
'''
#! coding: utf-8
# pylint: disable-msg=W0311

import time

from pyrrd.rrd import RRD, RRA, DS
from pyrrd.graph import DEF, CDEF, VDEF
from pyrrd.graph import LINE, GPRINT, AREA
from pyrrd.graph import ColorAttributes, Graph

def draw_graph(data, group):
  ## Graph bytes_in, bytes_out, request, by time+group
  filename = 'network%s.rrd' %group
  graphfile_traffic = 'traffic%s.png' %group
#  graphfileLg_traffic = 'traffic-large.png'
  graphfile_request = 'request%s.png' %group
#  graphfileLg_request = 'request-large'
  
  #define times
  hour = 60 * 60
  day = 24 * 60 * 60
  week = 7 * day
  month = day * 30
  quarter = month * 3
  half = 365 * day / 2
  year = 365 * day
  delta = 5 * hour
  step = 10
  endTime = int(time.time())
  startTime = endTime - 36000
  maxSteps = int((endTime-startTime)/step)
  
  # create RRD file
 
#  DSTYPE
#  Counter:Use this format with value of snmp MIB like traffic counter or 
#  packet number for a interface. 
#  Gauge:Use this format for value like temperature,  indicator of pressure.
#  Derive:Use this format if you variation or delta between a moment and 
#  an another moment like the rate of of people entering or leaving a
#  room and derive works exactly like COUNTER but without overflow checks.
#  Absolute:Use this format when you count the number of mail after an alert. 
#   
#  HEARTBEAT
#  Is define the frequency between each update of value in the database but some time
#  it is possible to have UNKNOWN value.
#  MIN AND MAX are optional parameters witch define the range of your data source (DS).
#  If your value is out of the range the value will be defined as UNKNOWN.
#  If you don not know exactly the range of you value you can set the MIN and MAX value with 
#  U for unknown
  dss = []
  ds1 = DS(dsName='bytes_out', dsType='ABSOLUTE', heartbeat=300)
  ds2 = DS(dsName='bytes_in', dsType='ABSOLUTE', heartbeat=300)
  ds3 = DS(dsName='request', dsType='ABSOLUTE', heartbeat=300)
  dss.extend([ds1, ds2, ds3])
  
  rras1 = []
  rra1 = RRA(cf='AVERAGE', xff=0.5, steps=1, rows=1440)
  rra2 = RRA(cf='AVERAGE', xff=0.5, steps=6, rows=2016)
  rra3 = RRA(cf='AVERAGE', xff=0.5, steps=60, rows=720)
  rras1.extend([rra1, rra2, rra3])
  
  myRRD = RRD(filename, step=step, ds=dss, rra=rras1, start=startTime)
  myRRD.create(debug=False)
  
  ## RRD update
  
  counter = 0
  for i in data:
    counter += 1
    bytes_in = i['bytes_in'] or 0
    bytes_out = i['bytes_out'] or 0
    requests = i['request'] or 0
    times = i['time'] 
    myRRD.bufferValue(times, bytes_out, bytes_in, requests)
    if counter % 100 == 0:
      myRRD.update(debug=True)
  myRRD.update(debug=True)
  
  ## RRD graph
  
  def1 = DEF(rrdfile=myRRD.filename, vname='output', dsName=ds1.name)
  def2 = DEF(rrdfile=myRRD.filename, vname='input', dsName=ds2.name)
  def3 = DEF(rrdfile=myRRD.filename, vname='request', dsName=ds3.name)
  cdef1 = CDEF(vname='outbits', rpn='%s,8,*' % def1.vname)
  cdef2 = CDEF(vname='inbits', rpn='%s,8,*' % def2.vname)
  vdef11 = VDEF(vname='max_out', rpn='%s,MAXIMUM' % cdef1.vname)
  vdef12 = VDEF(vname='avg_out', rpn='%s,AVERAGE' % cdef1.vname)
  vdef21 = VDEF(vname='max_in', rpn='%s,MAXIMUM' % cdef2.vname)
  vdef22 = VDEF(vname='avg_in', rpn='%s,AVERAGE' % cdef2.vname)
  vdef31 = VDEF(vname='max_request', rpn='%s,MAXIMUM' % def3.vname)
  vdef32 = VDEF(vname='avg_request', rpn='%s,AVERAGE' % def3.vname)
  
  line1 = LINE(2, defObj=def1, color='#2029CC', legend='Out traffic')
  line2 = LINE(2, defObj=def2, color='#00FF00', legend='In traffic\\n')
  line3 = LINE(2, defObj=def3, color='#FF0000', legend='Requests\\n')
  gprint11 = GPRINT(vdef11, 'Max_out\\: %5.1lf %Sbps')
  gprint12 = GPRINT(vdef12, 'Avg_out\\: %5.1lf %Sbps\\n')
  gprint21 = GPRINT(vdef21, 'Max_in\\: %5.1lf %Sbps')
  gprint22 = GPRINT(vdef22, 'Avg_in\\: %5.1lf %Sbps')
  gprint31 = GPRINT(vdef31, 'Max_request\\: %5.1lf %S')
  gprint32 = GPRINT(vdef32, 'Avg_request\\: %5.1lf %S')
  
  
  # ColorAttributes
  ca = ColorAttributes()
  ca.back = '#CCCDE2'  #background
  ca.canvas = '#FFFFFF'#the background of the actual graph
  ca.shadea = '#000000'#left and top border
  ca.shadeb = '#111111'#right and bottom border
  ca.mgrid = '#6666CC' #maior grid
  ca.axis = '#000000'  #axis of the graph
  ca.frame = '#CCCDE2' #line around the color spots
  ca.font = '#000000'  #color of the font
  ca.arrow = '#CC0000' # arrow head pointing up and forward
  
## graph traffic
  g = Graph(graphfile_traffic, end=endTime, vertical_label='Bytes/s', color=ca)
  g.data.extend([def1, def2, line1, line2, cdef1, cdef2, vdef11, vdef12, vdef21, vdef22, gprint11, gprint12, gprint21, gprint22])
  g.title = '"report traffic %s"'%group
  
  g.start=endTime - delta
  g.step = step
  g.width = 397
  g.height = 182
  g.write(debug=False)
  
#  g.filename = graphfileLg_traffic
#  g.width = 800
#  g.height = 400
#  g.write()

## graph request
  g1 = Graph(graphfile_request, end=endTime, vertical_label='Request/s', color=ca)
  g1.data.extend([def3, vdef31, vdef32, line3, gprint31, gprint32])
  g1.title = '"report request %s"'%group

  g1.start=endTime - delta
  g1.step = step
  g1.width = 397
  g1.height = 182
  g1.write(debug=False)
  
#  g1.filename = graphfileLg_request
#  g1.width = 800
#  g1.height = 400
#  g1.write()


  
def draw_total(res):
  ## graph total(bytes_out, bytes_in, request) by time
  
  # define name
  total_network = 'total.rrd'
  graphfile_total_traffic = 'total_traffic.png' 
#  graphfileLg_total_traffic = 'total_traffic-large.png'
  graphfile_total_request = 'total_request.png'
#  graphfileLg_total_request = 'total_request-large'
  
  #define times
  hour = 60 * 60
  day = 24 * 60 * 60
  week = 7 * day
  month = day * 30
  quarter = month * 3
  half = 365 * day / 2
  year = 365 * day
  delta = 10 * hour
  step = 1
  endTime = int(time.time())
  startTime = endTime - 360000
  maxSteps = int((endTime-startTime)/step)
  
  ## Create RRD 
  dss = []
  ds1 = DS(dsName='total_bytes_out', dsType='ABSOLUTE', heartbeat=300)
  ds2 = DS(dsName='total_bytes_in', dsType='ABSOLUTE', heartbeat=300)
  ds3 = DS(dsName='total_request', dsType='ABSOLUTE', heartbeat=300)
  dss.extend([ds1, ds2, ds3])

  rras1 = []
  rra1 = RRA(cf='AVERAGE', xff=0.5, steps=1, rows=1440)
  rra2 = RRA(cf='AVERAGE', xff=0.5, steps=6, rows=2016)
  rra3 = RRA(cf='AVERAGE', xff=0.5, steps=60, rows=720)
  rras1.extend([rra1, rra2, rra3])
  
  myRRD = RRD(total_network, step=step, ds=dss, rra=rras1, start=startTime)
  myRRD.create(debug=False)
  
  ## RRD update
  counter = 0
  for i in res:
    counter += 1
    total_bytes_in = int(i['total_bytes_in']) or 0
    total_bytes_out = int(i['total_bytes_out']) or 0
    total_requests = int(i['total_request']) or 0
    t_times = int(i['time']) 
    myRRD.bufferValue(t_times, total_bytes_out, total_bytes_in, total_requests)
    if counter % 100 == 0:
      myRRD.update(debug=True)
  myRRD.update(debug=True)
  
  ## RRD graph
  def1 = DEF(rrdfile=myRRD.filename, vname='total_output', dsName=ds1.name)
  def2 = DEF(rrdfile=myRRD.filename, vname='total_input', dsName=ds2.name)
  def3 = DEF(rrdfile=myRRD.filename, vname='total_request', dsName=ds3.name)
  cdef = CDEF(vname='totaloutbits', rpn='%s,8,*' % def1.vname)
  vdef = VDEF(vname='max', rpn='%s,MAXIMUM' % cdef.vname)
  
  line1 = LINE(1, defObj=def1, color='#2029CC', legend='Total Out traffic')
  line2 = LINE(1, defObj=def2, color='#00FF00', legend='Total In traffic')
  line3 = LINE(1, defObj=def3, color='#FF0000', legend='Total Requests')
  gprint = GPRINT(vdef, 'Max\\: %5.1lf %Sbps')
  
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
  
  
  ##  
  g = Graph(graphfile_total_traffic, end=endTime, vertical_label='Bytes/s', color=ca)
  g.data.extend([def1, def2, line1, line2, cdef, vdef, gprint])
  g.title = '"report total traffic"'

  g.start = endTime - delta
  g.step = step
  g.width = 397
  g.height = 182
  g.write()
  
#  g.filename = graphfileLg_total_traffic
#  g.width = 800
#  g.height = 400
#  g.write()
#  
##
  g1 = Graph(graphfile_total_request, end=endTime, vertical_label='Request/s', color=ca)
  g1.data.extend([def3, line3])
  g1.title = '"report total request"'

  g1.start = endTime - delta
  g1.step = step
  g1.width = 397
  g1.height = 182
  g1.write(debug=False)
  
#  g1.filename = graphfileLg_total_request
#  g1.width = 800
#  g1.height = 400
#  g1.write()
  
