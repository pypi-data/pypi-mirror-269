from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from allure import attach
import allure
from src.test.library.util_web import UTIL_WEB

class WEB_OPENCART:

    screenshot_counter = 0
    
    def __init__(self, driver):
        self.driver = driver
    
    
    def abrir_URL(self, url):
        browser = UTIL_WEB.read_browser_config()
        self.driver = UTIL_WEB.get_web_driver()
        self.driver.get(url)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        WEB_OPENCART.screenshot_counter += 1  # Incrementar el contador de capturas
        screenshot_name = f"{WEB_OPENCART.screenshot_counter}_screenshot_abreWeb.png"
        UTIL_WEB.capture_screenshot(self.driver, screenshot_name)
        allure.attach(self.driver.get_screenshot_as_png(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)

    def cerrarNavegador(self, driver):
        self.driver.close()

    def click_MyAccount(self, driver):
        try:
            btn_my_account = self.driver.find_element(By.LINK_TEXT, "My Account")
            btn_my_account.click()
            WEB_OPENCART.screenshot_counter += 1
            screenshot_name = f"{WEB_OPENCART.screenshot_counter}_screenshot_clickMyAccount.png"
            UTIL_WEB.capture_screenshot(self.driver, screenshot_name)
            allure.attach(self.driver.get_screenshot_as_png(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)
        except NoSuchElementException:
            print("No se encontró el elemento necesario para realizar la verificación.")
            self.driver.close()
    
    def click_Register(self, driver):
        try:
            listLogin = self.driver.find_element(By.LINK_TEXT, "Login")
            listLogin.click()
            WEB_OPENCART.screenshot_counter += 1
            screenshot_name = f"{WEB_OPENCART.screenshot_counter}_screenshot_clickLogin.png"
            UTIL_WEB.capture_screenshot(self.driver, screenshot_name)
            allure.attach(self.driver.get_screenshot_as_png(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)
        except NoSuchElementException:
            print("No se encontró el elemento necesario para realizar la verificación.")
            self.driver.close()
    
    def click_Continue(self, driver):
        try:
            btnContinue = self.driver.find_element(By.LINK_TEXT, "Continue")
            btnContinue.click()
            WEB_OPENCART.screenshot_counter += 1
            screenshot_name = f"{WEB_OPENCART.screenshot_counter}_screenshot_clickContinue.png"
            UTIL_WEB.capture_screenshot(self.driver, screenshot_name)
            allure.attach(self.driver.get_screenshot_as_png(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)
        except NoSuchElementException:
            print("No se encontró el elemento necesario para realizar la verificación.")
            self.driver.close()

    def ingresaNombre(self, nombre):
        try:
            txtFirstName = self.driver.find_element(By.ID, "input-firstname")
            txtFirstName.send_keys(nombre)
            WEB_OPENCART.screenshot_counter += 1
            screenshot_name = f"{WEB_OPENCART.screenshot_counter}_screenshot_ingresoNombre.png"
            UTIL_WEB.capture_screenshot(self.driver, screenshot_name)
            allure.attach(self.driver.get_screenshot_as_png(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)
        except NoSuchElementException:
            print("No se encontró el elemento necesario para realizar la verificación.")
            self.driver.close()

    def ingresaApellido(self, apellido):
        try:
            txtLastname = self.driver.find_element(By.ID, "input-lastname")
            txtLastname.send_keys(apellido)
            WEB_OPENCART.screenshot_counter += 1
            screenshot_name = f"{WEB_OPENCART.screenshot_counter}_screenshot_ingresoApellido.png"
            UTIL_WEB.capture_screenshot(self.driver, screenshot_name)
            allure.attach(self.driver.get_screenshot_as_png(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)
        except NoSuchElementException:
            print("No se encontró el elemento necesario para realizar la verificación.")
            self.driver.close()
    
    def ingresaEmail(self, correo):
        try:
            txtEmail = self.driver.find_element(By.ID, "input-email")
            txtEmail.send_keys(correo)
            WEB_OPENCART.screenshot_counter += 1
            screenshot_name = f"{WEB_OPENCART.screenshot_counter}_screenshot_ingresoEmail.png"
            UTIL_WEB.capture_screenshot(self.driver, screenshot_name)
            allure.attach(self.driver.get_screenshot_as_png(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)
        except NoSuchElementException:
            print("No se encontró el elemento necesario para realizar la verificación.")
            self.driver.close()
    
    def ingresaTelefono(self, telefono):
        try:
            txtPhone = self.driver.find_element(By.ID, "input-telephone")
            txtPhone.send_keys(telefono)
            WEB_OPENCART.screenshot_counter += 1
            screenshot_name = f"{WEB_OPENCART.screenshot_counter}_screenshot_ingresoTelefono.png"
            UTIL_WEB.capture_screenshot(self.driver, screenshot_name)
            allure.attach(self.driver.get_screenshot_as_png(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)
        except NoSuchElementException:
            print("No se encontró el elemento necesario para realizar la verificación.")
            self.driver.close()


    def ingresaClave(self, ruta_json):
        try:            
            password = UTIL_WEB.obtener_contraseña_desde_json(ruta_json)
            print("Contraseña obtenida del archivo JSON:", password)
            txtPass1 = self.driver.find_element(By.ID, "input-password")
            txtPass1.send_keys(password)  # Usamos la contraseña obtenida del JSON
            WEB_OPENCART.screenshot_counter += 1
            screenshot_name = f"{WEB_OPENCART.screenshot_counter}_screenshot_ingresoClave.png"
            UTIL_WEB.capture_screenshot(self.driver, screenshot_name)
            allure.attach(self.driver.get_screenshot_as_png(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)
        except NoSuchElementException:
            print("No se encontró el elemento necesario para realizar la verificación.")
            self.driver.close()

    def ingresaConfirmación(self, ruta_json):
        try:            
            p_confirmar = UTIL_WEB.obtener_confirmacion_desde_json(ruta_json)
            print("Contraseña obtenida del archivo JSON:", p_confirmar)
            txtPass2 = self.driver.find_element(By.ID, "input-confirm")
            txtPass2.send_keys(p_confirmar)
            WEB_OPENCART.screenshot_counter += 1
            screenshot_name = f"{WEB_OPENCART.screenshot_counter}_screenshot_ingresoConfirmacion.png"
            UTIL_WEB.capture_screenshot(self.driver, screenshot_name)
            allure.attach(self.driver.get_screenshot_as_png(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)
        except NoSuchElementException:
            print("No se encontró el elemento necesario para realizar la verificación.")
            self.driver.close()

    def click_Privacidad(self, driver):
        try:
            checkBox = self.driver.find_element(By.NAME, "agree")
            checkBox.click()
            WEB_OPENCART.screenshot_counter += 1
            screenshot_name = f"{WEB_OPENCART.screenshot_counter}_screenshot_clickPrivacidad.png"
            UTIL_WEB.capture_screenshot(self.driver, screenshot_name)
            allure.attach(self.driver.get_screenshot_as_png(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)
        except NoSuchElementException:
            print("No se encontró el elemento necesario para realizar la verificación.")
            self.driver.close()
    
    def click_Continuar(self, driver):
        try:
            btnSumit = self.driver.find_element(By.CSS_SELECTOR, "input[class='btn btn-primary']")
            btnSumit.click()
            WEB_OPENCART.screenshot_counter += 1
            screenshot_name = f"{WEB_OPENCART.screenshot_counter}_screenshot_clickSubmit.png"
            UTIL_WEB.capture_screenshot(self.driver, screenshot_name)
            allure.attach(self.driver.get_screenshot_as_png(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)
        except NoSuchElementException:
            print("No se encontró el elemento necesario para realizar la verificación.")
            self.driver.close()
            

    def click_Login(self, driver):
        try:
            btnLogin = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit'][value='Login']")
            btnLogin.click()
            WEB_OPENCART.screenshot_counter += 1
            screenshot_name = f"{WEB_OPENCART.screenshot_counter}_screenshot_clickLogin.png"
            UTIL_WEB.capture_screenshot(self.driver, screenshot_name)
            allure.attach(self.driver.get_screenshot_as_png(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)
        except NoSuchElementException:
            print("No se encontró el elemento necesario para realizar la verificación.")
            self.driver.close()

    def verificarRegistro(self, driver):
        try:
            label = self.driver.find_element(By.XPATH, "//*[@id='content']/p[1]")
            textoOutput = label.text
            textoEsperado = "Congratulations! Your new account has been successfully created!"
            assert textoOutput == textoEsperado
            WEB_OPENCART.screenshot_counter += 1
            screenshot_name = f"{WEB_OPENCART.screenshot_counter}_screenshot_verificacion.png"
            UTIL_WEB.capture_screenshot(self.driver, screenshot_name)
            allure.attach(self.driver.get_screenshot_as_png(), name=screenshot_name, attachment_type=allure.attachment_type.PNG)
        except AssertionError:
            print("La verificación falló: el texto obtenido no coincide con el texto esperado.")
            self.driver.close()
        except NoSuchElementException:
            print("No se encontró el elemento necesario para realizar la verificación.")
            self.driver.close()
        except Exception as e:
            print(f"Ocurrió un error inesperado: {str(e)}")
            self.driver.close()
            