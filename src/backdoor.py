#! coding: utf-8
# pylint: disable-msg=W0311
import os
import bottle
import settings

@bottle.route('/fetch/:year/:month/:day/:hour/:minute')
def fetch(year, month, day, hour, minute):
  filename = '%s/%s/%s/%s/%s/access.log' % (year, month, day, hour, minute) 
  path_to_log = os.path.join(settings.log_dir, filename)
  print path_to_log
  data = open(path_to_log).read()
  return data

@bottle.route('/delete/:year/:month/:day/:hour/:minute')
def delete(year, month, day, hour, minute):
  filename = '%s/%s/%s/%s/%s/access.log' % (year, month, day, hour, minute) 
  path_to_log = os.path.join(settings.log_dir, filename)
  os.unlink(path_to_log)
  return 'OK'

if __name__ == "__main__":
  bottle.run(host='0.0.0.0', port=2309)