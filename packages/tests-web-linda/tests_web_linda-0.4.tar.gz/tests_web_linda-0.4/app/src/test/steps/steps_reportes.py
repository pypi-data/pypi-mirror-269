from behave import *
from selenium.common.exceptions import NoSuchElementException
from src.test.pages.pages_reporteUFT import REPORTE_UFT

# Inicializar el driver de Selenium
driver = None
page = None

@given('Se realiza el proceso de obtener evidencias')
def step_impl(context):
    global driver, page
    page = REPORTE_UFT(driver)
    page.abrir_URLReporte(driver)
    page.procesoCaptura(driver)
    page.cerrarNavegador(driver)
