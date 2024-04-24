# from selenium.webdriver import Chrome
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException
# from src.test.library.util_mobile import UTIL_MOBILE
# from allure import attach


# class APP_TSOFT:

#     screenshot_counter = 0
    
#     def __init__(self, xdriver):
#         self.xdriver = xdriver

#     def abrir_app_TSOFT(self):
#         if self.xdriver is None:  # Usar self.xdriver en lugar de xdriver
#             self.xdriver = UTIL_MOBILE.get_driver_app_TSOFT()  # Utilizar self.xdriver en lugar de xdriver
#         return self.xdriver  # Devolver el controlador
    