'''
Created on Jan 27, 2011

@author: rucney
'''
#! coding: utf-8
# pylint: disable-msg=W0311
import settings
import api
from master import parse_log
from celery.decorators import task

import datetime
import urllib
@task
def fetch_logs():
  delta = datetime.timedelta(minutes=1)
  t = datetime.datetime.now() - delta
  print t
  log_file = "%s/%02d/%02d/%02d/%02d" % (t.year, t.month, t.day, t.hour, t.minute)
  for ip in settings.servers:   
    url = 'http://%s:2309/fetch/%s/access.log' % (ip, log_file)
    print url
    data = urllib.urlopen(url).read()
    if data != '':
      lines = data.split("\n")
      for line in lines:
        if line != '':
          params = parse_log(line)
          print line
          api.insert(params)
    # TODO: delete log
  return True