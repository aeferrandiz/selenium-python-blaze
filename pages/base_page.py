"""
Base class for all pages in the framework
Implements common methods and wait handling
"""

import logging
import time
from typing import List, Optional, Union
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    ElementClickInterceptedException,
    StaleElementReferenceException
)
from config.config import Config


class BasePage:
    """Base class with common methods for all pages"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.actions = ActionChains(driver)
    
    def find_element(self, locator: tuple, timeout: int = None) -> WebElement:
        """
        Find element with explicit wait
        
        Args:
            locator (tuple): Tuple (By, selector)
            timeout (int): Custom wait time
        
        Returns:
            WebElement: Found element
        """
        try:
            wait_time = timeout or Config.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.presence_of_element_located(locator))
            self.logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            raise
    
    def find_elements(self, locator: tuple, timeout: int = None) -> List[WebElement]:
        """
        Find multiple elements with explicit wait
        
        Args:
            locator (tuple): Tuple (By, selector)
            timeout (int): Custom wait time
        
        Returns:
            List[WebElement]: Found elements
        """
        try:
            wait_time = timeout or Config.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            elements = wait.until(EC.presence_of_all_elements_located(locator))
            self.logger.debug(f"Elements found: {len(elements)} {locator}")
            return elements
        except TimeoutException:
            self.logger.error(f"Elements not found: {locator}")
            return []
    
    def wait_for_element_visible(self, locator: tuple, timeout: int = None) -> WebElement:
        """
        Wait for element to be visible
        
        Args:
            locator (tuple): Tuple (By, selector)
            timeout (int): Custom wait time
        
        Returns:
            WebElement: Visible element
        """
        try:
            wait_time = timeout or Config.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.visibility_of_element_located(locator))
            self.logger.debug(f"Element visible: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not visible: {locator}")
            raise
    
    def wait_for_element_clickable(self, locator: tuple, timeout: int = None) -> WebElement:
        """
        Wait for element to be clickable
        
        Args:
            locator (tuple): Tuple (By, selector)
            timeout (int): Custom wait time
        
        Returns:
            WebElement: Clickable element
        """
        try:
            wait_time = timeout or Config.EXPLICIT_WAIT
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.element_to_be_clickable(locator))
            self.logger.debug(f"Element clickable: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not clickable: {locator}")
            raise
    
    def click_element(self, locator: tuple, timeout: int = None) -> bool:
        """
        Click element with retry mechanism
        
        Args:
            locator (tuple): Tuple (By, selector)
            timeout (int): Custom wait time
        
        Returns:
            bool: True if successful
        """
        for attempt in range(Config.MAX_RETRIES):
            try:
                element = self.wait_for_element_clickable(locator, timeout)
                element.click()
                self.logger.info(f"Click successful: {locator}")
                return True
            except (ElementClickInterceptedException, StaleElementReferenceException) as e:
                self.logger.warning(f"Click attempt {attempt + 1} failed: {e}")
                if attempt < Config.MAX_RETRIES - 1:
                    time.sleep(Config.RETRY_DELAY)
                else:
                    self.logger.error(f"Click failed after {Config.MAX_RETRIES} attempts: {locator}")
                    return False
        return False
    
    def send_keys(self, locator: tuple, text: str, clear: bool = True, timeout: int = None) -> bool:
        """
        Send keys to element
        
        Args:
            locator (tuple): Tuple (By, selector)
            text (str): Text to send
            clear (bool): Whether to clear field first
            timeout (int): Custom wait time
        
        Returns:
            bool: True if successful
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            if clear:
                element.clear()
            element.send_keys(text)
            self.logger.info(f"Text sent to {locator}: {text}")
            return True
        except Exception as e:
            self.logger.error(f"Error sending keys to {locator}: {e}")
            return False
    
    def get_text(self, locator: tuple, timeout: int = None) -> str:
        """
        Get text from element
        
        Args:
            locator (tuple): Tuple (By, selector)
            timeout (int): Custom wait time
        
        Returns:
            str: Element text
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            text = element.text
            self.logger.debug(f"Text from {locator}: {text}")
            return text
        except Exception as e:
            self.logger.error(f"Error getting text from {locator}: {e}")
            return ""
    
    def get_attribute(self, locator: tuple, attribute: str, timeout: int = None) -> str:
        """
        Get attribute value from element
        
        Args:
            locator (tuple): Tuple (By, selector)
            attribute (str): Attribute name
            timeout (int): Custom wait time
        
        Returns:
            str: Attribute value
        """
        try:
            element = self.wait_for_element_visible(locator, timeout)
            value = element.get_attribute(attribute)
            self.logger.debug(f"Attribute {attribute} from {locator}: {value}")
            return value or ""
        except Exception as e:
            self.logger.error(f"Error getting attribute {attribute} from {locator}: {e}")
            return ""
    
    def is_element_present(self, locator: tuple, timeout: int = None) -> bool:
        """
        Check if element is present
        
        Args:
            locator (tuple): Tuple (By, selector)
            timeout (int): Custom wait time
        
        Returns:
            bool: True if present
        """
        try:
            wait_time = timeout or 2
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator: tuple, timeout: int = None) -> bool:
        """
        Check if element is visible
        
        Args:
            locator (tuple): Tuple (By, selector)
            timeout (int): Custom wait time
        
        Returns:
            bool: True if visible
        """
        try:
            wait_time = timeout or 2
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_clickable(self, locator: tuple, timeout: int = None) -> bool:
        """
        Check if element is clickable
        
        Args:
            locator (tuple): Tuple (By, selector)
            timeout (int): Custom wait time
        
        Returns:
            bool: True if clickable
        """
        try:
            wait_time = timeout or 2
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_alert(self, timeout: int = None) -> bool:
        """
        Wait for alert to appear
        
        Args:
            timeout (int): Custom wait time
        
        Returns:
            bool: True if alert appears
        """
        try:
            wait_time = timeout or 5
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(EC.alert_is_present())
            return True
        except TimeoutException:
            return False
    
    def get_alert_text(self) -> str:
        """
        Get alert text
        
        Returns:
            str: Alert text
        """
        try:
            alert = self.driver.switch_to.alert
            text = alert.text
            self.logger.debug(f"Alert text: {text}")
            return text
        except Exception as e:
            self.logger.error(f"Error getting alert text: {e}")
            return ""
    
    def accept_alert(self) -> bool:
        """
        Accept alert
        
        Returns:
            bool: True if successful
        """
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
            self.logger.info("Alert accepted")
            return True
        except Exception as e:
            self.logger.error(f"Error accepting alert: {e}")
            return False
    
    def dismiss_alert(self) -> bool:
        """
        Dismiss alert
        
        Returns:
            bool: True if successful
        """
        try:
            alert = self.driver.switch_to.alert
            alert.dismiss()
            self.logger.info("Alert dismissed")
            return True
        except Exception as e:
            self.logger.error(f"Error dismissing alert: {e}")
            return False
    
    def scroll_to_element(self, locator: tuple) -> bool:
        """
        Scroll to element
        
        Args:
            locator (tuple): Tuple (By, selector)
        
        Returns:
            bool: True if successful
        """
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.logger.debug(f"Scrolled to element: {locator}")
            return True
        except Exception as e:
            self.logger.error(f"Error scrolling to element {locator}: {e}")
            return False
    
    def hover_element(self, locator: tuple) -> bool:
        """
        Hover over element
        
        Args:
            locator (tuple): Tuple (By, selector)
        
        Returns:
            bool: True if successful
        """
        try:
            element = self.wait_for_element_visible(locator)
            self.actions.move_to_element(element).perform()
            self.logger.debug(f"Hovered over element: {locator}")
            return True
        except Exception as e:
            self.logger.error(f"Error hovering over element {locator}: {e}")
            return False
    
    def double_click_element(self, locator: tuple) -> bool:
        """
        Double click element
        
        Args:
            locator (tuple): Tuple (By, selector)
        
        Returns:
            bool: True if successful
        """
        try:
            element = self.wait_for_element_clickable(locator)
            self.actions.double_click(element).perform()
            self.logger.debug(f"Double clicked element: {locator}")
            return True
        except Exception as e:
            self.logger.error(f"Error double clicking element {locator}: {e}")
            return False
    
    def right_click_element(self, locator: tuple) -> bool:
        """
        Right click element
        
        Args:
            locator (tuple): Tuple (By, selector)
        
        Returns:
            bool: True if successful
        """
        try:
            element = self.wait_for_element_clickable(locator)
            self.actions.context_click(element).perform()
            self.logger.debug(f"Right clicked element: {locator}")
            return True
        except Exception as e:
            self.logger.error(f"Error right clicking element {locator}: {e}")
            return False
    
    def take_screenshot(self, filename: str = None) -> str:
        """
        Take screenshot
        
        Args:
            filename (str): Screenshot filename
        
        Returns:
            str: Screenshot path
        """
        try:
            if not filename:
                timestamp = int(time.time())
                filename = f"screenshot_{timestamp}.png"
            
            screenshot_path = f"{Config.SCREENSHOTS_DIR}/{filename}"
            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {e}")
            return ""
    
    def execute_javascript(self, script: str, *args) -> any:
        """
        Execute JavaScript
        
        Args:
            script (str): JavaScript code
            *args: Arguments for the script
        
        Returns:
            any: Script result
        """
        try:
            result = self.driver.execute_script(script, *args)
            self.logger.debug(f"JavaScript executed: {script}")
            return result
        except Exception as e:
            self.logger.error(f"Error executing JavaScript: {e}")
            return None
    
    def wait_for_page_load(self, timeout: int = None) -> bool:
        """
        Wait for page to load completely
        
        Args:
            timeout (int): Custom wait time
        
        Returns:
            bool: True if page loaded
        """
        try:
            wait_time = timeout or Config.PAGE_LOAD_TIMEOUT
            wait = WebDriverWait(self.driver, wait_time)
            wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            self.logger.debug("Page loaded completely")
            return True
        except TimeoutException:
            self.logger.error("Page load timeout")
            return False
    
    def refresh_page(self) -> bool:
        """
        Refresh current page
        
        Returns:
            bool: True if successful
        """
        try:
            self.driver.refresh()
            self.wait_for_page_load()
            self.logger.info("Page refreshed")
            return True
        except Exception as e:
            self.logger.error(f"Error refreshing page: {e}")
            return False
    
    def get_current_url(self) -> str:
        """
        Get current URL
        
        Returns:
            str: Current URL
        """
        try:
            url = self.driver.current_url
            self.logger.debug(f"Current URL: {url}")
            return url
        except Exception as e:
            self.logger.error(f"Error getting current URL: {e}")
            return ""
    
    def get_page_title(self) -> str:
        """
        Get page title
        
        Returns:
            str: Page title
        """
        try:
            title = self.driver.title
            self.logger.debug(f"Page title: {title}")
            return title
        except Exception as e:
            self.logger.error(f"Error getting page title: {e}")
            return ""