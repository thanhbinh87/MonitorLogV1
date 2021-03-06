'''
Created on Jan 27, 2011

@author: rucney
'''
#! coding: utf-8
# pylint: disable-msg=W0311, E1101
import os
import bottle
import settings
import datetime

@bottle.route('/fetch/:year/:month/:day/:hour/:minute')
def fetch(year, month, day, hour, minute):
  """ define filename, path_log, read_log, del_log"""
  
  filename = '%s/%s/%s/%s/%s/access.log' % (year, month, day, hour, minute)
  path_to_log = os.path.join(settings.LOG_DIR, filename)
  print path_to_log
  data = open(path_to_log).read()
  t = datetime.datetime(year, month, hour, minute)
  k = 10
  while True:
    k += 1
    delta = datetime.timedelta(minutes=k)
    t0 = t - delta
    filename = '%s/%s/%s/%s/%s/access.log' \
            % (t0.year, t0.month, t0.day, t0.hour, t0.minute)
    path_to_log = os.path.join(settings.LOG_DIR, filename)
    try:
      os.unlink(path_to_log)
    except OSError:
      break
  return data

if __name__ == "__main__":
  bottle.run(host='0.0.0.0', port=2309)