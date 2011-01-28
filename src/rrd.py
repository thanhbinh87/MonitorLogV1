'''
Created on ian 18, 2011

@author: rucney
'''
#! coding: utf-8
# pylint: disable-msg=W0311
from pyrrd.rrd import RRD, RRA, DS
from pyrrd.graph import DEF, VDEF
from pyrrd.graph import LINE, GPRINT
from pyrrd.graph import ColorAttributes, Graph
import settings

def ds():
  dss = []
  ds1 = DS(dsName='out', dsType='ABSOLUTE', heartbeat=200)
  ds2 = DS(dsName='in', dsType='ABSOLUTE', heartbeat=200)
  ds3 = DS(dsName='request', dsType='ABSOLUTE', heartbeat=200)
  dss.extend([ds1, ds2, ds3])
  return dss

def rra():
  rras = []
  rra1 = RRA(cf='AVERAGE', xff=0.5, steps=1, rows=1440)
  rra2 = RRA(cf='AVERAGE', xff=0.5, steps=6, rows=2016)
  rra3 = RRA(cf='AVERAGE', xff=0.5, steps=60, rows=720)
  rras.extend([rra1, rra2, rra3])
  return rras

def rrdcreate(rrdname):
  myrrd = RRD(filename=rrdname, step=settings.step, ds=ds(), \
              rra=rra(), start=settings.starttime)
  myrrd.create(debug=False)
  return myrrd

def updaterrd(data, myrrd):
  counter = 0
  for i in data:
    counter += 1
    bytes_in = int(i['bytes_in']) 
    bytes_out = int(i['bytes_out']) 
    requests = int(i['request']) 
    times = int(i['time']) 
    myrrd.bufferValue(times, bytes_out, bytes_in, requests)
    if counter % 100 == 0:
      myrrd.update(debug=True)
  myrrd.update(debug=True)
  return True
  
def color():
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
  return ca

def vdef(rrdfile, trafficname, requestname):
  ###
  step = settings.step
  end = settings.endTime
  ### def
  def_out = DEF(rrdfile=rrdfile, vname='out', dsName='out')
  def_in = DEF(rrdfile=rrdfile, vname='in', dsName='in')
  def_request = DEF(rrdfile=rrdfile, vname='request', dsName='request')
  ### vdef
  vdef_out1 = VDEF(vname='maxout', rpn='%s,MAXIMUM' % def_out.vname)
  vdef_out2 = VDEF(vname='avgout', rpn='%s,AVERAGE' % def_out.vname)
  vdef_in1 = VDEF(vname='maxin', rpn='%s,MAXIMUM' % def_in.vname)
  vdef_in2 = VDEF(vname='avgin', rpn='%s,AVERAGE' % def_in.vname)
  vdef_request1 = VDEF(vname='maxreq', rpn='%s,MAXIMUM' % def_request.vname)
  vdef_request2 = VDEF(vname='avgreq', rpn='%s,AVERAGE' % def_request.vname)
  ### line
  line_out = LINE(2, defObj=def_out, color='#2029CC', legend='Out')
  line_in = LINE(2, defObj=def_in, color='#00FF00', legend='In')
  line_request = LINE(2, defObj=def_request, color='#FF0000', legend='Request')
  ### gprint
  gprint_out1 = GPRINT(vdef_out1, 'max\\: %5.1lf %Sbps')
  gprint_out2 = GPRINT(vdef_out2, 'avg\\: %5.1lf %Sbps\\n')
  gprint_in1 = GPRINT(vdef_in1, 'max\\: %5.1lf %Sbps')
  gprint_in2 = GPRINT(vdef_in2, 'avg\\: %5.1lf %Sbps\\n')
  gprint_request1 = GPRINT(vdef_request1, 'max\\: %5.1lf %S')
  gprint_request2 = GPRINT(vdef_request2, 'avg\\: %5.1lf %S\\n')
  ###
#  for delta in settings.DELTA:
  delta = settings.DELTA
  start = settings.endTime - delta
  ### traffic
  g_traffic = Graph(trafficname, step=step, start=start, end=end, \
                    vertical_label='Bytes/s', color=color())
  g_traffic.data.extend([def_out, def_in, \
                         vdef_out1, vdef_out2, vdef_in1, vdef_in2, \
                         line_out, gprint_out1, gprint_out2, \
                         line_in, gprint_in1, gprint_in2])
  g_traffic.title = '"report traffic "'
  g_traffic.write(debug=True)
  ### request
  g_request = Graph(requestname, step=step, start=start, end=end, \
                    vertical_label='Requests/s', color=color())
  g_request.data.extend([def_request, vdef_request1, vdef_request2, \
                         line_request, gprint_request1, gprint_request2])
  
  g_request.title = '"report request "'
  g_request.write(debug=True)
  
  return True
  
def graphrrd(data, res, group):
  
  #### graph by group 
  rrdname = 'network.rrd'
  trafficname = 'traffic%s.png' %group
  requestname = 'request%s.png' %group
  
  myrrd = rrdcreate(rrdname)
  
  updaterrd(data, myrrd)
  
  vdef(rrdname, trafficname, requestname)
  
  ### graph total
  rrdtotal = 'total.rrd'
  traffictotal = 'traffic_total.png'
  requesttotal = 'request_total.png'
  
  myrrdtotal = rrdcreate(rrdtotal)
  
  updaterrd(res, myrrdtotal)
  
  vdef(rrdtotal, traffictotal, requesttotal)
  
  return True
  
 
  