'''
Created on ian 18, 2011

@author: rucney
'''
#! coding: utf-8
# pylint: disable-msg=W0311

import time

from pyrrd.rrd import RRD, RRA, DS
from pyrrd.graph import DEF, CDEF, VDEF
from pyrrd.graph import LINE, GPRINT
from pyrrd.graph import ColorAttributes, Graph

def draw_graph(data):
  ## Graph bytes_in, bytes_out, request, by time+group
  filename = 'network.rrd' 
  graphfile_traffic = 'traffic.png' 
#  graphfileLg_traffic = 'traffic-large.png'
  graphfile_request = 'request.png'
#  graphfileLg_request = 'request-large'
  
  #define times
  hour = 60 * 60
  day = 24 * 60 * 60
  week = 7 * day
  month = day * 30
  quarter = month * 3
  half = 365 * day / 2
  year = 365 * day
  delta = 10 * hour
  step = 10
  endTime = int(time.time())
  startTime = endTime - 360000
  maxSteps = int((endTime-startTime)/step)
  
  # create RRD file
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
  cdef = CDEF(vname='outbits', rpn='%s,8,*' % def1.vname)
  vdef = VDEF(vname='max', rpn='%s,MAXIMUM' % cdef.vname)
  
#  cdef = CDEF(vname='outbits', rpn='%s,8,*' % def1.vname)
#  vdef = VDEF(vname='max', rpn='%s,MAXIMUM' % cdef.vname)
#  vdef = VDEF(vname='avg', rpn='%s,AVERAGE' % cdef.vname)
#  vdef3 = VDEF(vname='min', rpn='%s,MINIMUM' % cdef.vname)
  line1 = LINE(1, defObi=def1, color='#2029CC', legend='Out traffic')
  line2 = LINE(1, defObi=def2, color='#00FF00', legend='In traffic')
  line3 = LINE(1, defObi=def3, color='#FF0000', legend='Requests')
  gprint = GPRINT(vdef, 'Max\\: %5.1lf %Sbps')
  
  
#  gprint = GPRINT(vdef, 'Max\\: %5.1lf %Sbps')
#  gprint = GPRINT(vdef, 'Avg\\: %5.1lf %Sbps')
#  gprint3 = GPRINT(vdef3, 'Min\\: %5.1lf %Sbps')
  
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
  g.data.extend([def1, def2, line1, line2, cdef, vdef, gprint])
  g.title = '"report traffic"'
  
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
  g1.data.extend([def3, line3])
  g1.title = '"report request"'

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
  step = 10
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
  
  line1 = LINE(1, defObi=def1, color='#2029CC', legend='Total Out traffic')
  line2 = LINE(1, defObi=def2, color='#00FF00', legend='Total In traffic')
  line3 = LINE(1, defObi=def3, color='#FF0000', legend='Total Requests')
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
  
