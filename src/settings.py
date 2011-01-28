'''
Created on Jan 27, 2011

@author: rucney
'''
#! coding: utf-8
# pylint: disable-msg=W0311
import time
SERVERS = ['192.168.3.69', '192.168.6.150']

MONGODB_NODE = None

LOG_DIR = '/var/ramdisk/log/'
hour = 60 * 60
day = 24 * 60 * 60
week = 7 * day
month = day * 30
year = 365 * day
#DELTA = [hour, 12*hour, day, week, month, year]
DELTA = 1 * hour
step = 10

endTime = int(time.time()) - 600
starttime = endTime - 360000