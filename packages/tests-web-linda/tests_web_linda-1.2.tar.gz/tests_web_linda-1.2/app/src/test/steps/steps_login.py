from behave import *
from selenium.common.exceptions import NoSuchElementException
from src.test.pages.pages_OpenCart import WEB_OPENCART

# Inicializar el driver de Selenium
driver = None
page = None


@given('Usuario ingresa nuevamente a la web de OpenCart "{url}"')
def step_impl(context, url):
    global driver, page
    page = WEB_OPENCART(driver)
    page.abrir_URL(url)
    

@when('Usuario da click en la opcion Login')
def step_impl(context):
    global driver, page
    page.click_MyAccount(driver)
    page.click_Register(driver)
      

@when('Usuario ingesa su correo "{correo}"')
def step_impl(context, correo):
    global driver, page
    page.ingresaEmail(correo)
    


@when('Usuario ingresa su contraseña')
def step_impl(context):
    global driver, page
    ruta_json = "./src/test/resources/data/json/credentials.json"
    page.ingresaClave(ruta_json)
    


@then('Se verifica el Login correcto')
def step_impl(context):
    global driver, page
    page.click_Login(driver)
    page.cerrarNavegador(driver)
