import os
import json
from selenium.webdriver import Chrome, Firefox, Edge
import configparser

class UTIL_WEB:

    @staticmethod
    def get_web_driver():
        config = configparser.ConfigParser()
        config.read('browser.properties')
        browser = config.get('General', 'browser')
        so = config.get('General', 'so')
        ruta_proyecto = os.getcwd()+"/src/test/resources/drivers"
        print(ruta_proyecto)
        if so.lower()=="linux":
            ruta_proyecto = ruta_proyecto+"/linux"
            if browser.lower() == "chrome":
                ruta_proyecto = ruta_proyecto+"/chromedriver"
                return Chrome(ruta_proyecto)
            elif browser.lower() == "firefox":
                ruta_proyecto = ruta_proyecto+"/geckodriver.exe"
                return Firefox(ruta_proyecto)
            elif browser.lower() == "edge":
                ruta_proyecto = ruta_proyecto+"/msedgedriver.exe"
                return Edge(ruta_proyecto)
            else:
                raise ValueError("Unsupported browser!")
        if so.lower()=="windows":
            ruta_proyecto = ruta_proyecto+"/windows"
            if browser.lower() == "chrome":
                ruta_proyecto = ruta_proyecto+"/chromedriver.exe"
                return Chrome(ruta_proyecto)
            elif browser.lower() == "firefox":
                ruta_proyecto = ruta_proyecto+"/geckodriver.exe"
                return Firefox(ruta_proyecto)
            elif browser.lower() == "edge":
                ruta_proyecto = ruta_proyecto+"/msedgedriver.exe"
                return Edge(ruta_proyecto)
            else:
                raise ValueError("Unsupported browser!")
    
    @staticmethod
    def read_browser_config():
        config = configparser.ConfigParser()
        config.read('browser.properties')
        return config.get('General', 'browser')

    @staticmethod
    def capture_screenshot(driver, filename, directory='screenshots'):
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, filename)
        driver.save_screenshot(filepath)

    @staticmethod
    def obtener_contraseña_desde_json(ruta_json):
        with open(ruta_json, 'r') as archivo_json:
            datos = json.load(archivo_json)
            return datos["credentials"]["password"]
        
    @staticmethod
    def obtener_confirmacion_desde_json(ruta_json):
        with open(ruta_json, 'r') as archivo_json:
            datos = json.load(archivo_json)
            return datos["credentials"]["confirm_password"]
        
    
    