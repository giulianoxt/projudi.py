import mechanize
from BeautifulSoup import BeautifulSoup


LOGIN_URL = 'https://projudi.tjrn.jus.br/projudi/indexParte.jsp'


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

  response = browser.submit()
  return response
