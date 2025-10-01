"""
Page Object para la funcionalidad de Login
Maneja el modal de login de DemoBlaze
"""

import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
from utils.test_data import TestData


class LoginPage(BasePage):
    """Page Object para el modal de login"""
    
    # Localizadores
    LOGIN_LINK = (By.XPATH, "//a[@id='login2']")
    USERNAME_INPUT = (By.ID, "loginusername")
    PASSWORD_INPUT = (By.ID, "loginpassword")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Log in']")
    CLOSE_BUTTON = (By.XPATH, "//div[@id='logInModal']//button[text()='Close']")
    LOGOUT_LINK = (By.XPATH, "//a[text()='Log out']")
    WELCOME_MESSAGE = (By.XPATH, "//a[@id='nameofuser']")
    MODAL_DIALOG = (By.ID, "logInModal")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
    
    def open_login_modal(self) -> bool:
        """
        Abre el modal de login haciendo click en el enlace de login
        
        Returns:
            bool: True si el modal se abrió correctamente
        """
        try:
            # Esperar a que el enlace de login esté disponible
            if self.click_element(self.LOGIN_LINK):
                # Verificar que el modal se abrió
                if self.wait_for_element_visible(self.MODAL_DIALOG, timeout=5):
                    self.logger.info("Modal de login abierto exitosamente")
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Error al abrir modal de login: {e}")
            return False
    
    def enter_username(self, username: str) -> bool:
        """
        Ingresa el nombre de usuario
        
        Args:
            username (str): Nombre de usuario
        
        Returns:
            bool: True si se ingresó correctamente
        """
        try:
            if self.send_keys(self.USERNAME_INPUT, username):
                self.logger.info(f"Usuario ingresado: {username}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error al ingresar usuario: {e}")
            return False
    
    def enter_password(self, password: str) -> bool:
        """
        Ingresa la contraseña
        
        Args:
            password (str): Contraseña
        
        Returns:
            bool: True si se ingresó correctamente
        """
        try:
            if self.send_keys(self.PASSWORD_INPUT, password):
                self.logger.info("Contraseña ingresada")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error al ingresar contraseña: {e}")
            return False
    
    def click_login_button(self) -> bool:
        """
        Hace click en el botón de login
        
        Returns:
            bool: True si se hizo click correctamente
        """
        try:
            if self.click_element(self.LOGIN_BUTTON):
                self.logger.info("Botón de login presionado")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error al hacer click en botón de login: {e}")
            return False
    
    def close_login_modal(self) -> bool:
        """
        Cierra el modal de login
        
        Returns:
            bool: True si se cerró correctamente
        """
        try:
            # Estrategia 1: Intentar hacer click en el botón Close específico del modal
            if self.click_element(self.CLOSE_BUTTON):
                # Verificar que el modal se cerró
                if not self.is_element_visible(self.MODAL_DIALOG, timeout=3):
                    self.logger.info("Modal de login cerrado con botón Close")
                    return True
            
            # Estrategia 2: Usar JavaScript para hacer click en el botón Close
            try:
                close_button = self.driver.find_element('xpath', "//div[@id='logInModal']//button[text()='Close']")
                self.driver.execute_script("arguments[0].click();", close_button)
                if not self.is_element_visible(self.MODAL_DIALOG, timeout=3):
                    self.logger.info("Modal de login cerrado con JavaScript click")
                    return True
            except:
                pass
            
            # Estrategia 3: Intentar hacer click en el botón X (×)
            try:
                x_button = self.driver.find_element('xpath', "//div[@id='logInModal']//button[text()='×']")
                self.driver.execute_script("arguments[0].click();", x_button)
                if not self.is_element_visible(self.MODAL_DIALOG, timeout=3):
                    self.logger.info("Modal de login cerrado con botón X")
                    return True
            except:
                pass
            
            # Estrategia 4: Presionar Escape
            from selenium.webdriver.common.keys import Keys
            self.driver.find_element(*self.USERNAME_INPUT).send_keys(Keys.ESCAPE)
            
            # Verificar si el modal se cerró
            if not self.is_element_visible(self.MODAL_DIALOG, timeout=2):
                self.logger.info("Modal de login cerrado con Escape")
                return True
                
            return False
        except Exception as e:
            self.logger.error(f"Error al cerrar modal de login: {e}")
            return False
    
    def login(self, username: str = None, password: str = None) -> bool:
        """
        Realiza el proceso completo de login
        
        Args:
            username (str): Nombre de usuario (opcional, usa datos por defecto)
            password (str): Contraseña (opcional, usa datos por defecto)
        
        Returns:
            bool: True si el login fue exitoso
        """
        try:
            # Usar datos por defecto si no se proporcionan
            if not username:
                username = TestData.get_user("valid_user")["username"]
            if not password:
                password = TestData.get_user("valid_user")["password"]
            
            # Abrir modal de login
            if not self.open_login_modal():
                return False
            
            # Ingresar credenciales
            if not self.enter_username(username):
                return False
            
            if not self.enter_password(password):
                return False
            
            # Hacer login
            if not self.click_login_button():
                return False
            
            # Esperar a que el modal se cierre y aparezca el mensaje de bienvenida
            if self.wait_for_login_success():
                self.logger.info("Login exitoso")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error durante el proceso de login: {e}")
            return False
    
    def wait_for_login_success(self, timeout: int = 10) -> bool:
        """
        Espera a que el login sea exitoso verificando la aparición del enlace de logout
        
        Args:
            timeout (int): Tiempo de espera en segundos
        
        Returns:
            bool: True si el login fue exitoso
        """
        try:
            # Esperar a que aparezca el enlace de logout
            if self.wait_for_element_visible(self.LOGOUT_LINK, timeout):
                self.logger.info("Login exitoso - enlace de logout visible")
                return True
            
            # También verificar si hay mensaje de bienvenida
            if self.is_element_present(self.WELCOME_MESSAGE, timeout=2):
                welcome_text = self.get_text(self.WELCOME_MESSAGE)
                if "Welcome" in welcome_text:
                    self.logger.info(f"Login exitoso - mensaje de bienvenida: {welcome_text}")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error al verificar login exitoso: {e}")
            return False
    
    def is_logged_in(self) -> bool:
        """
        Verifica si el usuario está logueado
        
        Returns:
            bool: True si está logueado
        """
        try:
            # Verificar que el enlace de logout esté visible
            return self.is_element_visible(self.LOGOUT_LINK, timeout=2)
        except Exception as e:
            self.logger.error(f"Error al verificar estado de login: {e}")
            return False
    
    def logout(self) -> bool:
        """
        Realiza logout del usuario
        
        Returns:
            bool: True si el logout fue exitoso
        """
        try:
            if self.click_element(self.LOGOUT_LINK):
                # Verificar que el enlace de login aparezca nuevamente
                if self.wait_for_element_visible(self.LOGIN_LINK, timeout=5):
                    self.logger.info("Logout exitoso")
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Error durante logout: {e}")
            return False
    
    def get_welcome_message(self) -> str:
        """
        Obtiene el mensaje de bienvenida del usuario logueado
        
        Returns:
            str: Mensaje de bienvenida
        """
        try:
            if self.is_element_present(self.WELCOME_MESSAGE):
                return self.get_text(self.WELCOME_MESSAGE)
            return ""
        except Exception as e:
            self.logger.error(f"Error al obtener mensaje de bienvenida: {e}")
            return ""
    
    def handle_login_alert(self) -> str:
        """
        Maneja las alertas que pueden aparecer durante el login
        
        Returns:
            str: Texto de la alerta si existe
        """
        try:
            # Esperar un poco para que aparezca la alerta
            import time
            time.sleep(1)
            
            # Intentar detectar la alerta
            if self.wait_for_alert(timeout=2):
                alert_text = self.get_alert_text()
                self.accept_alert()
                self.logger.info(f"Alerta de login manejada: {alert_text}")
                return alert_text
            else:
                self.logger.warning("No se detectó alerta")
                return ""
        except Exception as e:
            self.logger.error(f"Error al manejar alerta de login: {e}")
            return ""
    
    def login_with_invalid_credentials(self, username: str = "invalid", password: str = "invalid") -> str:
        """
        Intenta hacer login con credenciales inválidas para probar manejo de errores
        
        Args:
            username (str): Usuario inválido
            password (str): Contraseña inválida
        
        Returns:
            str: Mensaje de error de la alerta
        """
        try:
            # Abrir modal de login
            if not self.open_login_modal():
                return ""
            
            # Ingresar credenciales inválidas
            self.enter_username(username)
            self.enter_password(password)
            
            # Intentar hacer login
            self.click_login_button()
            
            # Manejar la alerta de error
            error_message = self.handle_login_alert()
            
            # Cerrar el modal
            self.close_login_modal()
            
            return error_message
            
        except Exception as e:
            self.logger.error(f"Error al probar login con credenciales inválidas: {e}")
            return ""
