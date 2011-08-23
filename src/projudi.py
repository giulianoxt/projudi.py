import mechanize
from BeautifulSoup import BeautifulSoup


LOGIN_URL = 'https://projudi.tjrn.jus.br/projudi/indexParte.jsp'
MAIN_PAGE_URL = 'https://projudi.tjrn.jus.br/projudi/parte/frameCentroParte.jsp'


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


def _goto_processos_ativo(browser):
  return browser.follow_link(url_regex='ativosPoloAtivo')

def _goto_main_page(browser):
  return browser.open(MAIN_PAGE_URL)


def get_processos_ativo(browser):
  res = _goto_processos_ativo(browser)

  soup = BeautifulSoup(res.read())
  table_procs = soup.find(id='texto').table

  processos = []

  for row_proc in table_procs.findAll('tr')[2:]:
    td = row_proc.findAll('td')[1]
    proc_str = td.a.text.strip()
    processos.append(str(proc_str))

  _goto_main_page(browser)
  return processos
