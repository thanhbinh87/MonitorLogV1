'''
Created on Jan 18, 2011

@author: rucney
'''
#! coding: utf-8
# pylint: disable-msg=W0311

import time
import random

from pyrrd.rrd import RRD, RRA, DS
from pyrrd.graph import Graph, LINE, DEF

#create file name
exampleNum = 2
filename = 'speed%s.rrd' % exampleNum
graphfile = 'speed%s.png' % exampleNum
graphfileLg = 'speed%s-large.png' % exampleNum

#define times
day = 24 * 60 * 60
week = 7 * day
month = day * 30
quarter = month * 3
half = 365 * day / 2
year = 365 * day

endTime = int(round(time.time()))
delta = 13136400
startTime = endTime - delta
step = 300 # This database is created for updates every 5 minutes (300 seconds)
maxSteps = int((endTime-startTime)/step)

# create RRD file
dss = []
ds = DS(dsName='output', dsType='COUNTER', heartbeat=600)
dss.append(ds)

rras = []
rra1 = RRA(cf='AVERAGE', xff=0.5, steps=1, rows=600)
rra2 = RRA(cf='AVERAGE', xff=0.5, steps=6, rows=700)
rra3 = RRA(cf='MAX', xff=0.5, steps=1, rows=600)
rra4 = RRA(cf='MAX', xff=0.5, steps=6, rows=700)
rras.extend([rra1, rra2, rra3, rra4])
myRRD = RRD(filename, ds=dss, rra=rras, start=startTime)
myRRD.create()

# RRD update
currentTime = startTime
value = 0
a = []
for i in xrange(maxSteps):
  currentTime += step
  # lets update the RRD/purge the buffer ever 100 entires
  if i % 100 == 0:
    myRRD.update(debug=False)
      
  value += random.randrange(1000, 3000)
  # added to the RRD object.
  myRRD.bufferValue(currentTime, value)
myRRD.update()

# make RRD graph
def1 = DEF(rrdfile=myRRD.filename, vname='output', dsName=ds.name)
line = LINE(defObj=def1, color='#0000FF', legend='Out traffic')
startTime = endTime - 1 * day
g = Graph(graphfile, start=startTime, end=endTime, title = 'Speed', vertical_label='Bytes/s')
g.data.extend([def1, line])
g.write()

g.filename = graphfileLg
g.width = 800
g.height = 400
g.write()
