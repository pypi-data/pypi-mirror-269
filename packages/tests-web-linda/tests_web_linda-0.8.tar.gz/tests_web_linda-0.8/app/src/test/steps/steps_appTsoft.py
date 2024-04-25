# from behave import *
# from src.test.pages.pages_appTsoft import APP_TSOFT

# # Inicializar el driver de Selenium
# xdriver = None

# @given('ingreso al App')
# def step_impl(context):
#     global xdriver
#     if xdriver is None:
#         xdriver = APP_TSOFT(xdriver).abrir_app_TSOFT()  # Crear una instancia de APP_TSOFT y llamar abrir_app_TSOFT()
#     else:
#         APP_TSOFT(xdriver).abrir_app_TSOFT()  # Si xdriver ya está inicializado, simplemente llama a abrir_app_TSOFT()

# @when('doy click al boton iniciar sesion')
# def step_impl(context):
#     print("Simulando dar clic al botón iniciar sesión...")


# @when('ingreso mi usuario "{usuario}" y clave "{password}"')
# def step_impl(context, usuario, password):
#     print("Simulando ingresar usuario y clave:", usuario, password)


# @when('doy click en el boton  iniciar')
# def step_impl(context):
#     print("Simulando dar clic al botón iniciar sesión...")


# @then('verifico el ingreso correcto')
# def step_impl(context):
#     print("Simulando dar clic al botón iniciar sesión...")