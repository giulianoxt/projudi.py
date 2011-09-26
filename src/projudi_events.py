#!/usr/bin/env python

import os
import sys
import json
import hashlib
import smtplib
from datetime import datetime
from email.MIMEText import MIMEText

import projudi


CONFIG_PATH = os.path.join(os.getenv('HOME'), '.projudi')


def load_config():
  with open(CONFIG_PATH, 'r') as config_f:
    return json.load(config_f)
    
def save_config(config):
  config['timestamp'] = str(datetime.now())
  with open(CONFIG_PATH, 'w') as config_f:
    json.dump(config, config_f, indent=2)

def send_email(subject, body, config):
  email_cfg = config['email']
  
  charset = 'UTF-8' 
  msg = MIMEText(body.encode(charset), 'plain', charset)
  msg['From'] = email_cfg['from_addr']
  msg['To'] = email_cfg['to_addr']
  msg['Subject'] = subject
  
  server = smtplib.SMTP(email_cfg['smtp'])
  server.starttls()
  server.login(email_cfg['username'], email_cfg['password'])
  server.sendmail(email_cfg['from_addr'], email_cfg['to_addr'], msg.as_string())
  server.quit()


def events_str(event_data):
  str = u''
  
  for proc_id, events in event_data.viewitems():
    str += u'--- Process #%s ---\n' % (proc_id)
    for event in reversed(events):
      str += u'\n- Event #%s:\n' % (event[0])
      str += unicode(event[1]) + '\n'
      for data in event[2:]:
        str += unicode(data) + '\n'
    str += '\n'

  return str
  
  
def events_hash(event_data):
  str = events_str(event_data)
  md5 = hashlib.md5(str.encode('UTF-8'))
  return md5.hexdigest()


def events_changed(event_data, config):
  last_hash = config['last_update']
  current_hash = events_hash(event_data)
  
  return current_hash != last_hash


def notify_change(event_data, config):
  str = events_str(event_data)
  send_email('[PROJUDI ALERT] Events changed', str, config)
  
  config['last_update'] = events_hash(event_data)


if __name__ == '__main__':
  print '[%s] ' % (datetime.now(),),

  config = load_config()
  
  login = config['projudi']['cpf']
  password = config['projudi']['password']

  browser = projudi.init_session()
  projudi.login(browser, login, password)
  processos = projudi.get_processos_ativo(browser)

  data = { }
  for proc_id in processos:
    data[proc_id] = projudi.get_events_processo(browser, proc_id)

  if events_changed(data, config):
    print 'CHANGED! Notifying...'
    notify_change(data, config)
  else:
    print 'Same.'

  save_config(config)

