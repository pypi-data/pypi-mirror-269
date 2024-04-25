# from behave import *
# from src.test.pages.pages_appURPI import APP_URPI

# # Inicializar el driver de Selenium
# xdriver = None
# page = None

# @given('ingreso al App URPI')
# def step_impl(context):
#     global xdriver, page
#     if xdriver is None:
#         xdriver = APP_URPI(xdriver).abrir_app_URPI()  # Crear una instancia de APP_TSOFT y llamar abrir_app_TSOFT()
#     else:
#         APP_URPI(xdriver).abrir_app_URPI()  # Si xdriver ya está inicializado, simplemente llama a abrir_app_TSOFT()

# @when('ingreso mi correo "{correo}"')
# def step_impl(context, correo):
#     global xdriver, page
#     APP_URPI(xdriver).click_permitir()
#     APP_URPI(xdriver).click_permitirUbicacion()
#     APP_URPI(xdriver).ingresa_correo_urpi(correo)
    
# @when('doy click en el boton siguiente')
# def step_impl(context):
#     global xdriver, page
#     APP_URPI(xdriver).click_siguiente()

# @when('ingreso la clave "{password}"')
# def step_impl(context, password):
#     global xdriver, page
#     APP_URPI(xdriver).ingresa_password_urpi(password)
    
# @then('doy click en el boton ingresar')
# def step_impl(context):
#     APP_URPI(xdriver).click_iniciar()
