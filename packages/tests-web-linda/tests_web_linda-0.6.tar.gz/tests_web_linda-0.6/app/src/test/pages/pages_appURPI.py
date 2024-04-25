# from selenium.webdriver import Chrome
# from appium.webdriver.common.appiumby import AppiumBy
# from selenium.common.exceptions import NoSuchElementException
# from src.test.library.util_mobile import UTIL_MOBILE
# from allure import attach
# import time


# class APP_URPI:

#     screenshot_counter = 0
    
#     def __init__(self, xdriver):
#         self.xdriver = xdriver

#     def abrir_app_URPI(self):
#         if self.xdriver is None:  # Usar self.xdriver en lugar de xdriver
#             self.xdriver = UTIL_MOBILE.get_driver_app_URPI()  # Utilizar self.xdriver en lugar de xdriver
#         return self.xdriver  # Devolver el controlador
    
#     def click_permitir(self):
#         try:
#             btn_permitir = self.xdriver.find_element(AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button")
#             btn_permitir.click()
#         except NoSuchElementException:
#             print("No se encontró el elemento necesario para realizar la verificación.")
#             self.xdriver.close()

#     def click_permitirUbicacion(self):
#         try:
#             btn_permitirUbica = self.xdriver.find_element(AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button")
#             btn_permitirUbica.click()
#         except NoSuchElementException:
#             print("No se encontró el elemento necesario para realizar la verificación.")
#             self.xdriver.close()

#     def ingresa_correo_urpi(self, correo):
#         try:
#             self.xdriver.implicitly_wait(15)
#             txt_correo = self.xdriver.find_element(AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.RelativeLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[1]/android.view.View[2]/android.view.View/android.view.View[3]/android.view.View/android.widget.EditText")
#             txt_correo.send_keys(correo)
#         except NoSuchElementException:
#             print("No se encontró el elemento necesario para realizar la verificación.")
#             self.xdriver.close()

#     def click_siguiente(self):
#         try:
#             btn_siguiente = self.xdriver.find_element(AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.RelativeLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[1]/android.view.View[2]/android.view.View/android.view.View[5]/android.widget.Button[2]")
#             btn_siguiente.click()
#         except NoSuchElementException:
#             print("No se encontró el elemento necesario para realizar la verificación.")
#             self.xdriver.close()

#     def ingresa_password_urpi(self, password):
#         try:
#             self.xdriver.implicitly_wait(5)
#             txt_password = self.xdriver.find_element(AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.RelativeLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[2]/android.view.View[2]/android.widget.EditText")
#             txt_password.send_keys(password)
#         except NoSuchElementException:
#             print("No se encontró el elemento necesario para realizar la verificación.")
#             self.xdriver.close()
    
#     def click_iniciar(self):
#         try:
#             btn_iniciar = self.xdriver.find_element(AppiumBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.RelativeLayout/android.widget.RelativeLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.view.View[4]/android.widget.Button")
#             btn_iniciar.click()
#         except NoSuchElementException:
#             print("No se encontró el elemento necesario para realizar la verificación.")
#             self.xdriver.close()