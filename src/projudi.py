import mechanize
from BeautifulSoup import BeautifulSoup


BASE_URL = 'https://projudi.tjrn.jus.br/projudi/'
LOGIN_URL = BASE_URL + 'indexParte.jsp'
MAIN_PAGE_URL = BASE_URL + 'parte/frameCentroParte.jsp'
PROCESSO_PAGE_URL = BASE_URL + 'listagens/DadosProcesso?numeroProcesso=%s'


def init_session():
  browser = mechanize.Browser()
  browser.open(LOGIN_URL)
  return browser


def login(browser, cpf, password):
  browser.select_form('formLogin')
  form = browser.form
  
  # emulate js
  radio_cpf = form.find_control(name='tipoDocumento')
  radio_cpf.get(nr=0).selected = True

  pass_field = form.find_control(id='senha')
  pass_field.disabled = False

  # enter login info
  form.set_value(cpf, id='cpfCnpj', nr=0)
  form.set_value(password, id='senha')

  return browser.submit()


def _goto_main_page(browser):
  return browser.open(MAIN_PAGE_URL)


def get_processos_ativo(browser):
  res = browser.follow_link(url_regex='ativosPoloAtivo')

  soup = BeautifulSoup(res.read())
  table_procs = soup.find(id='texto').table

  processos = []

  for row_proc in table_procs.findAll('tr')[2:]:
    check = row_proc.find(type='checkbox')
    proc_id = str(check['value'])
    processos.append(proc_id)

  _goto_main_page(browser)
  return processos


def get_events_processo(browser, proc_id):
  res = browser.open(PROCESSO_PAGE_URL % proc_id)

  soup = BeautifulSoup(res.read())
  proc_table = soup.find(id='Arquivos').table

  events = []

  for event_row in proc_table('tr', recursive=False)[1:]:
    sub_table = event_row.table
    main_row = sub_table.tr

    columns = main_row('td', recursive=False)
    event = [td.getText('\n') for td in columns[2:-1]]
    events.append(event)

  _goto_main_page(browser)

  events.reverse()
  return events

