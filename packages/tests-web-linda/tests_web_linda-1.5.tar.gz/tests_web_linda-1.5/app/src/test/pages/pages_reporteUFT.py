from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from src.test.library.util_web import UTIL_WEB
from allure import attach
import time
import keyboard
import os

class REPORTE_UFT:
    screenshot_counter = 0

    def __init__(self, driver):
        self.driver = driver

    def abrir_URLReporte(self, driver):
        browser = UTIL_WEB.read_browser_config()
        self.driver = UTIL_WEB.get_web_driver()
        self.driver.get("D:/MIBANCO-PLAYWRIGHT/src/test/resources/reports/cucumber-html-reports/overview-tags.html")
        self.driver.implicitly_wait(2)
        self.driver.maximize_window()
        # Crear la carpeta "screenshots" si no existe
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
    
    def procesoCaptura(self, driver):
        # Encontrar todos los elementos de fila <tr> dentro del elemento de la tabla
        filas = self.driver.find_elements(By.XPATH, '//*[@id="tablesorter"]/tbody/tr')
        # Obtener el número de filas
        numero_de_filas = len(filas)-1
        # Imprimir el número de filas
        print("El número de filas es:", numero_de_filas)
            # Iterar sobre cada fila y hacer clic en el primer elemento de la fila y luego en otro elemento deseado
        
        for indice, fila in enumerate(filas, start=2):
            # Construir el XPath dinámicamente con el índice de fila actual para el primer elemento de la fila
            xpath_primer_elemento = f'//*[@id="tablesorter"]/tbody/tr[{indice}]/td[1]/a'
            # Encontrar el primer elemento <td> de la fila utilizando el XPath construido
            primer_elemento = self.driver.find_element(By.XPATH, xpath_primer_elemento)
            # Hacer clic en el primer elemento de la fila
            primer_elemento.click()
        
            # Verificar si el elemento "Doc string" ya existe
            try:
                nombreTag = self.driver.find_element(By.XPATH, '//*[@id="report"]/div/div/table/tbody/tr/td[1]')
                textoTag = nombreTag.text
                texto_sin_arroba = textoTag[1:]
                
                doc_string = self.driver.find_element(By.LINK_TEXT, "Doc string")
                # Si existe, hacer clic en él y continuar con las acciones restantes
                doc_string.click()
                time.sleep(1)
                # Encontrar el elemento del cual deseas tomar el screenshot
                elementoWin = self.driver.find_element(By.ID, "msg-3")
                time.sleep(1)
                # Realizar un scroll hacia abajo en toda la página
                self.driver.execute_script("window.scrollBy(0, 800);")
                time.sleep(1)
                # Tomar el screenshot del elemento y guardarlo en un archivo
                elementoWin.screenshot(f"screenshots/{texto_sin_arroba}_v1.png")
                # Desplaza el elemento hacia la derecha usando JavaScript
                elementoWin.click()
                # Espera unos segundos antes de empezar
                time.sleep(1)
                # Número de veces que quieres presionar y soltar la tecla "right"
                num_veces = 30
                # Bucle para presionar y soltar la tecla "right" múltiples veces
                for _ in range(num_veces):
                    keyboard.press("right")
                    keyboard.release("right")
                time.sleep(1)
                elementoWin.screenshot(f"screenshots/{texto_sin_arroba}_v2.png")
                # Encontrar el segundo elemento utilizando el XPath construido
                segundo_elemento = self.driver.find_element(By.XPATH, '//*[@id="navigation"]/div/div/ul/li[2]')
                segundo_elemento.click()
                # Agregar una pausa de 1 segundo
                time.sleep(1)
            except NoSuchElementException:
                # Si no existe el elemento "Doc string", continuar con las acciones habituales
                nombreTag = self.driver.find_element(By.XPATH, '//*[@id="report"]/div/div/table/tbody/tr/td[1]')
                textoTag = nombreTag.text
                texto_sin_arroba = textoTag[1:]
                # Encontrar el elemento "Scenario" y hacer clic en él
                tercer_elemento = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Scenario')]")
                tercer_elemento.click()
                time.sleep(1)

                # Encontrar el elemento "Steps" y hacer clic en él
                cuarto_elemento = self.driver.find_element(By.XPATH, "//span[contains(text(), 'Steps')]")
                cuarto_elemento.click()
                time.sleep(1)

                # Encontrar el elemento "Doc string" y hacer clic en él
                doc_string = self.driver.find_element(By.LINK_TEXT, "Doc string")
                doc_string.click()
                time.sleep(1)

                # Encontrar el elemento del cual deseas tomar el screenshot
                elementoWin = self.driver.find_element(By.ID, "msg-3")
                time.sleep(1)
                # Realizar un scroll hacia abajo en toda la página
                self.driver.execute_script("window.scrollBy(0, 800);")
                time.sleep(1)
                # Tomar el screenshot del elemento y guardarlo en un archivo
                elementoWin.screenshot(f"screenshots/{texto_sin_arroba}_v1.png")
                # Desplaza el elemento hacia la derecha usando JavaScript
                elementoWin.click()
                # Espera unos segundos antes de empezar
                time.sleep(1)
                # Número de veces que quieres presionar y soltar la tecla "right"
                num_veces = 30
                # Bucle para presionar y soltar la tecla "right" múltiples veces
                for _ in range(num_veces):
                    keyboard.press("right")
                    keyboard.release("right")
                time.sleep(1)
                elementoWin.screenshot(f"screenshots/{texto_sin_arroba}_v2.png")
            
                # Encontrar el segundo elemento utilizando el XPath construido
                segundo_elemento = self.driver.find_element(By.XPATH, '//*[@id="navigation"]/div/div/ul/li[2]')
                segundo_elemento.click()
                # Agregar una pausa de 1 segundo
                time.sleep(1)
        
    def cerrarNavegador(self, driver):
        self.driver.close()