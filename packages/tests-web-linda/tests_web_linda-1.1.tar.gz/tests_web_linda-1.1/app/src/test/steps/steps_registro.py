from behave import *
from selenium.common.exceptions import NoSuchElementException
from src.test.pages.pages_OpenCart import WEB_OPENCART

# Inicializar el driver de Selenium
driver = None
page = None

@given('Usuario ingresa a la web de OpenCart "{url}"')
def step_impl(context, url):
    global driver, page
    page = WEB_OPENCART(driver)
    page.abrir_URL(url)

@given('Usuario da click en la opción Registro')
def step_impl(context):
    global driver, page
    page.click_MyAccount(driver)
    page.click_Register(driver)
    page.click_Continue(driver)

@given('Usuario llena los datos de Registro con "{nombre}", "{apellido}", "{correo}" y "{telefono}"')
def step_impl(context, nombre, apellido, correo, telefono):
    global driver, page
    page.ingresaNombre(nombre)
    page.ingresaApellido(apellido)
    page.ingresaEmail(correo)
    page.ingresaTelefono(telefono)

@given('Usuario ingresa sus claves')
def step_impl(context):
    global driver, page
    ruta_json = "./src/test/resources/data/json/credentials.json"
    page.ingresaClave(ruta_json)
    page.ingresaConfirmación(ruta_json)
    page.click_Privacidad(driver)

@then('Se verifica el registro correcto')
def step_impl(context):
    global driver, page
    page.click_Continuar(driver)
    page.verificarRegistro(driver)
    page.cerrarNavegador(driver)