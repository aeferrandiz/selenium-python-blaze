"""
Driver Factory for creating WebDriver instances
Supports Chrome and Firefox with optimized configurations
"""

import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class DriverFactory:
    """Factory for creating WebDriver instances with specific configurations"""
    
    def __init__(self):
        self.driver = None
        self.logger = logging.getLogger(__name__)
    
    def create_driver(self, browser="chrome", headless=False, window_size=(1920, 1080)):
        """
        Create a WebDriver instance
        
        Args:
            browser (str): Browser to use ('chrome' or 'firefox')
            headless (bool): Whether to run in headless mode
            window_size (tuple): Window size (width, height)
        
        Returns:
            WebDriver: Configured browser instance
        """
        try:
            if browser.lower() == "chrome":
                self.driver = self._create_chrome_driver(headless, window_size)
            elif browser.lower() == "firefox":
                self.driver = self._create_firefox_driver(headless, window_size)
            else:
                raise ValueError(f"Browser '{browser}' not supported. Use 'chrome' or 'firefox'")
            
            # Common configurations
            self._configure_driver()
            self.logger.info(f"Driver {browser} created successfully")
            return self.driver
            
        except Exception as e:
            self.logger.error(f"Error creating driver: {e}")
            raise
    
    def _create_chrome_driver(self, headless, window_size):
        """Create Chrome driver with optimized settings"""
        chrome_options = ChromeOptions()
        
        # Basic options
        if headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--ignore-certificate-errors-spki-list")
        
        # Performance options
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-features=TranslateUI")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        
        # Disable images for faster loading (optional)
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Create service and driver
        try:
            # Try to use system ChromeDriver first
            service = ChromeService()
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception:
            # If that fails, use webdriver-manager
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        
        return driver
    
    def _create_firefox_driver(self, headless, window_size):
        """Create Firefox driver with optimized settings"""
        firefox_options = FirefoxOptions()
        
        # Basic options
        if headless:
            firefox_options.add_argument("--headless")
        
        firefox_options.add_argument(f"--width={window_size[0]}")
        firefox_options.add_argument(f"--height={window_size[1]}")
        
        # Performance options
        firefox_options.set_preference("dom.webnotifications.enabled", False)
        firefox_options.set_preference("media.volume_scale", "0.0")
        firefox_options.set_preference("dom.push.enabled", False)
        firefox_options.set_preference("dom.push.connection.enabled", False)
        firefox_options.set_preference("dom.push.serverURL", "")
        firefox_options.set_preference("dom.push.userAgentID", "")
        firefox_options.set_preference("dom.push.registrationURL", "")
        
        # Disable images for faster loading (optional)
        firefox_options.set_preference("permissions.default.image", 2)
        
        # Create service and driver
        try:
            service = FirefoxService()
            driver = webdriver.Firefox(service=service, options=firefox_options)
        except Exception:
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=firefox_options)
        
        return driver
    
    def _configure_driver(self):
        """Apply common driver configurations"""
        if self.driver:
            # Set timeouts
            self.driver.implicitly_wait(10)
            self.driver.set_page_load_timeout(30)
            self.driver.set_script_timeout(30)
            
            # Maximize window if not headless
            if not self.driver.capabilities.get('headless', False):
                self.driver.maximize_window()
    
    def quit_driver(self):
        """Quit the current driver instance"""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("Driver closed successfully")
            except Exception as e:
                self.logger.error(f"Error closing driver: {e}")
            finally:
                self.driver = None


# Global instance
driver_factory = DriverFactory()