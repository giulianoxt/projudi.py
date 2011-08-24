#!/usr/bin/env python

import sys
import projudi


if __name__ == '__main__':
  login = sys.argv[1]
  password = sys.argv[2]

  print 'Connecting to projudi...'
  browser = projudi.init_session()

  print 'Logging in....'
  projudi.login(browser, login, password)

  print 'Getting list of processos...'
  processos = projudi.get_processos_ativo(browser)

  print 'Fetching event data...'
  data = { }
  for proc_id in processos:
    data[proc_id] = projudi.get_events_processo(browser, proc_id)

  print 'Displaying event data...\n'
  for proc_id, events in data.viewitems():
    print '--- Processo #%s ---' % (proc_id)

    for event in events:
      print '\n- Evento #%s:' % (event[0])
      print event[1], ''
      for data in event[2:]:
        print data

    print '\n'

