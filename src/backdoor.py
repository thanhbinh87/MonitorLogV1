'''
Created on Jan 27, 2011

@author: rucney
'''
#! coding: utf-8
# pylint: disable-msg=W0311
import os
import bottle
import settings
import datetime

from bottle import route, run, static_file, request, template
@bottle.route('/fetch/:year/:month/:day/:hour/:minute')
def fetch(year, month, day, hour, minute):
  filename = '%s/%s/%s/%s/%s/access.log' % (year, month, day, hour, minute)
  path_to_log = os.path.join(settings.log_dir, filename)
  print path_to_log
  data = open(path_to_log).read()
  t = datetime.datetime(year, month, hour, minute)
  k = 10
  while True:
    k += 1
    delta = datetime.timedelta(minutes=k)
    t0 = t - delta
    filename = '%s/%s/%s/%s/%s/access.log' % (t0.year, t0.month, t0.day, t0.hour, t0.minute)
    path_to_log = os.path.join(settings.log_dir, filename)
    try:
      os.unlink(path_to_log)
    except OSError:
      break
  return data

if __name__ == "__main__":
  bottle.run(host='0.0.0.0', port=2309)