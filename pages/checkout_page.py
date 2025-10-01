"""
Page Object for checkout page
Handles the purchase completion process
"""

import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config.config import Config


class CheckoutPage(BasePage):
    """Page Object for checkout page"""
    
    # Checkout modal
    CHECKOUT_MODAL = (By.ID, "orderModal")
    MODAL_TITLE = (By.XPATH, "//h5[@id='orderModalLabel']")
    
    # Information form
    NAME_INPUT = (By.ID, "name")
    COUNTRY_INPUT = (By.ID, "country")
    CITY_INPUT = (By.ID, "city")
    CREDIT_CARD_INPUT = (By.ID, "card")
    MONTH_INPUT = (By.ID, "month")
    YEAR_INPUT = (By.ID, "year")
    
    # Buttons
    PURCHASE_BUTTON = (By.XPATH, "//button[text()='Purchase']")
    CLOSE_BUTTON = (By.XPATH, "//button[text()='Close']")
    
    # Confirmation modal (Sweet Alert)
    CONFIRMATION_MODAL = (By.CLASS_NAME, "sweet-alert")
    CONFIRMATION_TITLE = (By.XPATH, "//div[@class='sweet-alert showSweetAlert visible']//h2")
    CONFIRMATION_MESSAGE = (By.XPATH, "//div[@class='sweet-alert showSweetAlert visible']//p[@class='lead text-muted']")
    CONFIRMATION_BUTTON = (By.XPATH, "//div[@class='sweet-alert showSweetAlert visible']//div[@class='sa-confirm-button-container']//button")
    
    # Order information
    ORDER_ID = (By.XPATH, "//p[contains(text(), 'Id:')]")
    ORDER_AMOUNT = (By.XPATH, "//p[contains(text(), 'Amount:')]")
    ORDER_CARD = (By.XPATH, "//p[contains(text(), 'Card:')]")
    ORDER_NAME = (By.XPATH, "//p[contains(text(), 'Name:')]")
    ORDER_DATE = (By.XPATH, "//p[contains(text(), 'Date:')]")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
    
    def proceed_to_checkout(self) -> bool:
        """
        Proceed to checkout from cart page
        
        Returns:
            bool: True if successful
        """
        try:
            # Look for Place Order button
            place_order_button = (By.XPATH, "//button[text()='Place Order']")
            if self.wait_for_element_clickable(place_order_button, timeout=10):
                self.click_element(place_order_button)
                self.logger.info("Clicked Place Order button")
                return True
            else:
                self.logger.error("Place Order button not found or not clickable")
                return False
        except Exception as e:
            self.logger.error(f"Error proceeding to checkout: {e}")
            return False
    
    def is_checkout_modal_visible(self) -> bool:
        """
        Check if checkout modal is visible
        
        Returns:
            bool: True if modal is visible
        """
        try:
            # Check if modal is visible by looking for the modal with display: block style
            modal_element = self.find_element(self.CHECKOUT_MODAL)
            if modal_element:
                # Check if modal has the 'show' class and is not hidden
                modal_classes = modal_element.get_attribute("class")
                modal_style = modal_element.get_attribute("style")
                
                # Modal is visible if it has 'show' class OR doesn't have 'display: none'
                is_visible = "show" in modal_classes or "display: none" not in modal_style
                self.logger.info(f"Modal visibility check - classes: {modal_classes}, style: {modal_style}, visible: {is_visible}")
                return is_visible
            return False
        except Exception as e:
            self.logger.error(f"Error checking checkout modal visibility: {e}")
            return False
    
    def fill_name(self, name: str) -> bool:
        """
        Fill name field
        
        Args:
            name (str): Customer name
        
        Returns:
            bool: True if successful
        """
        try:
            if self.send_keys(self.NAME_INPUT, name):
                self.logger.info(f"Name filled: {name}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error filling name: {e}")
            return False
    
    def fill_country(self, country: str) -> bool:
        """
        Fill country field
        
        Args:
            country (str): Country name
        
        Returns:
            bool: True if successful
        """
        try:
            if self.send_keys(self.COUNTRY_INPUT, country):
                self.logger.info(f"Country filled: {country}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error filling country: {e}")
            return False
    
    def fill_city(self, city: str) -> bool:
        """
        Fill city field
        
        Args:
            city (str): City name
        
        Returns:
            bool: True if successful
        """
        try:
            if self.send_keys(self.CITY_INPUT, city):
                self.logger.info(f"City filled: {city}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error filling city: {e}")
            return False
    
    def fill_credit_card(self, card_number: str) -> bool:
        """
        Fill credit card field
        
        Args:
            card_number (str): Credit card number
        
        Returns:
            bool: True if successful
        """
        try:
            if self.send_keys(self.CREDIT_CARD_INPUT, card_number):
                self.logger.info("Credit card filled")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error filling credit card: {e}")
            return False
    
    def fill_month(self, month: str) -> bool:
        """
        Fill month field
        
        Args:
            month (str): Month
        
        Returns:
            bool: True if successful
        """
        try:
            if self.send_keys(self.MONTH_INPUT, month):
                self.logger.info(f"Month filled: {month}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error filling month: {e}")
            return False
    
    def fill_year(self, year: str) -> bool:
        """
        Fill year field
        
        Args:
            year (str): Year
        
        Returns:
            bool: True if successful
        """
        try:
            if self.send_keys(self.YEAR_INPUT, year):
                self.logger.info(f"Year filled: {year}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error filling year: {e}")
            return False
    
    def fill_checkout_form(self, form_data: dict = None) -> bool:
        """
        Fill complete checkout form
        
        Args:
            form_data (dict): Form data dictionary
        
        Returns:
            bool: True if successful
        """
        try:
            # Use default data if not provided
            if not form_data:
                form_data = Config.TEST_DATA["shipping"]
            
            # Fill all form fields
            fields = [
                (self.NAME_INPUT, form_data.get('name', '')),
                (self.COUNTRY_INPUT, form_data.get('country', '')),
                (self.CITY_INPUT, form_data.get('city', '')),
                (self.CREDIT_CARD_INPUT, form_data.get('credit_card', '')),
                (self.MONTH_INPUT, form_data.get('month', '')),
                (self.YEAR_INPUT, form_data.get('year', ''))
            ]
            
            for locator, value in fields:
                if not self.send_keys(locator, value):
                    self.logger.error(f"Failed to fill field: {locator}")
                    return False
            
            self.logger.info("Checkout form filled successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error filling checkout form: {e}")
            return False
    
    def click_purchase(self) -> bool:
        """
        Click purchase button
        
        Returns:
            bool: True if successful
        """
        try:
            if self.click_element(self.PURCHASE_BUTTON):
                self.logger.info("Purchase button clicked")
                
                # Handle any alert that might appear
                try:
                    if self.wait_for_alert(timeout=2):
                        alert = self.driver.switch_to.alert
                        alert_text = alert.text
                        self.logger.info(f"Alert appeared after purchase click: {alert_text}")
                        alert.accept()
                except Exception as alert_error:
                    self.logger.debug(f"No alert or error handling alert: {alert_error}")
                
                # Wait a bit for Sweet Alert to appear
                import time
                time.sleep(2)
                
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error clicking purchase: {e}")
            return False
    
    def close_checkout_modal(self) -> bool:
        """
        Close checkout modal
        
        Returns:
            bool: True if successful
        """
        try:
            # Try multiple strategies to close the modal
            
            # Strategy 1: Click the Close button directly
            try:
                if self.click_element(self.CLOSE_BUTTON):
                    self.logger.info("Checkout modal closed with Close button")
                    return True
            except Exception as e:
                self.logger.warning(f"Close button click failed: {e}")
            
            # Strategy 2: Use JavaScript to click the Close button
            try:
                close_button = self.find_element(self.CLOSE_BUTTON)
                self.driver.execute_script("arguments[0].click();", close_button)
                
                # Wait a bit for the modal to close
                import time
                time.sleep(1)
                
                # Verify modal is actually closed
                if not self.is_checkout_modal_visible():
                    self.logger.info("Checkout modal closed with JavaScript")
                    return True
                else:
                    self.logger.warning("Modal still visible after JavaScript close")
            except Exception as e:
                self.logger.warning(f"JavaScript close button click failed: {e}")
            
            # Strategy 3: Try clicking the X button (if different from Close button)
            try:
                x_button = (By.XPATH, "//div[@id='orderModal']//button[@class='close']")
                if self.click_element(x_button):
                    self.logger.info("Checkout modal closed with X button")
                    return True
            except Exception as e:
                self.logger.warning(f"X button click failed: {e}")
            
            # Strategy 4: Press Escape key
            try:
                from selenium.webdriver.common.keys import Keys
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                
                # Wait a bit for the modal to close
                import time
                time.sleep(1)
                
                # Verify modal is actually closed
                if not self.is_checkout_modal_visible():
                    self.logger.info("Checkout modal closed with Escape key")
                    return True
                else:
                    self.logger.warning("Modal still visible after Escape key")
            except Exception as e:
                self.logger.warning(f"Escape key failed: {e}")
            
            return False
        except Exception as e:
            self.logger.error(f"Error closing checkout modal: {e}")
            return False
    
    def complete_purchase(self, form_data: dict = None) -> bool:
        """
        Complete entire purchase process
        
        Args:
            form_data (dict): Form data dictionary
        
        Returns:
            bool: True if successful
        """
        try:
            # Fill form
            if not self.fill_checkout_form(form_data):
                return False
            
            # Click purchase
            if not self.click_purchase():
                return False
            
            # Wait for confirmation
            if self.wait_for_confirmation_modal():
                self.logger.info("Purchase completed successfully")
                return True
            
            return False
        except Exception as e:
            self.logger.error(f"Error completing purchase: {e}")
            return False
    
    def wait_for_confirmation_modal(self, timeout: int = 10) -> bool:
        """
        Wait for confirmation modal to appear
        
        Args:
            timeout (int): Wait timeout
        
        Returns:
            bool: True if modal appears
        """
        try:
            # Try multiple selectors for the Sweet Alert
            selectors = [
                (By.XPATH, "//div[@class='sweet-alert showSweetAlert visible']"),
                (By.XPATH, "//div[contains(@class, 'sweet-alert') and contains(@class, 'showSweetAlert')]"),
                (By.XPATH, "//div[contains(@class, 'sweet-alert') and contains(@class, 'visible')]"),
                (By.CLASS_NAME, "sweet-alert"),
                (By.XPATH, "//div[@class='sweet-alert']"),
                (By.XPATH, "//h2[contains(text(), 'Thank you')]"),
                (By.XPATH, "//h2[contains(text(), 'purchase')]")
            ]
            
            for selector in selectors:
                try:
                    if self.wait_for_element_visible(selector, timeout=3):
                        self.logger.info(f"Confirmation modal appeared with selector: {selector}")
                        return True
                except:
                    continue
            
            # If no specific modal found, check if there's any alert or confirmation
            try:
                if self.wait_for_alert(timeout=2):
                    alert = self.driver.switch_to.alert
                    alert_text = alert.text
                    self.logger.info(f"Alert appeared instead of modal: {alert_text}")
                    alert.accept()
                    return True
            except:
                pass
            
            self.logger.warning("No confirmation modal found")
            return False
        except Exception as e:
            self.logger.error(f"Error waiting for confirmation modal: {e}")
            return False
    
    def get_confirmation_title(self) -> str:
        """
        Get confirmation modal title
        
        Returns:
            str: Confirmation title
        """
        try:
            # Try multiple selectors for the confirmation title
            selectors = [
                self.CONFIRMATION_TITLE,
                (By.XPATH, "//div[@class='sweet-alert showSweetAlert visible']//h2"),
                (By.XPATH, "//div[@class='sweet-alert']//h2"),
                (By.XPATH, "//div[@class='sweet-alert']//h1"),
                (By.XPATH, "//div[@class='sweet-alert']//div[contains(@class, 'title')]"),
                (By.XPATH, "//div[@class='sweet-alert']//*[contains(text(), 'Thank you')]"),
                (By.XPATH, "//div[@class='sweet-alert']//*[contains(text(), 'Success')]")
            ]
            
            for selector in selectors:
                try:
                    title = self.get_text(selector)
                    if title and title.strip():
                        self.logger.info(f"Confirmation title found: {title}")
                        return title
                except:
                    continue
            
            # If no specific title found, try to get any text from the modal
            try:
                modal_text = self.get_text(self.CONFIRMATION_MODAL)
                if modal_text and "Thank you" in modal_text:
                    self.logger.info(f"Confirmation modal text: {modal_text}")
                    return "Thank you for your purchase!"
            except:
                pass
            
            self.logger.warning("No confirmation title found")
            return ""
        except Exception as e:
            self.logger.error(f"Error getting confirmation title: {e}")
            return ""
    
    def get_confirmation_message(self) -> str:
        """
        Get confirmation modal message
        
        Returns:
            str: Confirmation message
        """
        try:
            # Try to get the message from the specific element first
            try:
                message = self.get_text(self.CONFIRMATION_MESSAGE)
                if message and message.strip():
                    self.logger.info(f"Confirmation message: {message}")
                    return message
            except:
                pass
            
            # If that fails, try to get the full modal text and extract the message
            try:
                modal_text = self.get_text(self.CONFIRMATION_MODAL)
                if modal_text and "Thank you" in modal_text:
                    # Extract the order details part (everything after "Thank you for your purchase!")
                    lines = modal_text.split('\n')
                    message_lines = []
                    found_thank_you = False
                    
                    for line in lines:
                        line = line.strip()
                        if line == "Thank you for your purchase!":
                            found_thank_you = True
                            continue
                        elif found_thank_you and line and line != "OK":
                            message_lines.append(line)
                    
                    if message_lines:
                        message = '\n'.join(message_lines)
                        self.logger.info(f"Confirmation message extracted: {message}")
                        return message
            except Exception as e:
                self.logger.warning(f"Could not extract message from modal text: {e}")
            
            self.logger.warning("No confirmation message found")
            return ""
        except Exception as e:
            self.logger.error(f"Error getting confirmation message: {e}")
            return ""
    
    def click_confirmation_ok(self) -> bool:
        """
        Click OK button on confirmation modal
        
        Returns:
            bool: True if successful
        """
        try:
            # Try multiple selectors for the OK button
            selectors = [
                (By.XPATH, "//div[contains(@class, 'sweet-alert')]//div[@class='sa-confirm-button-container']//button"),
                (By.XPATH, "//div[contains(@class, 'sweet-alert')]//button[contains(@class, 'confirm')]"),
                (By.XPATH, "//div[contains(@class, 'sweet-alert')]//button[text()='OK']"),
                (By.XPATH, "//button[text()='OK']")
            ]
            
            for selector in selectors:
                try:
                    if self.click_element(selector):
                        self.logger.info(f"Confirmation OK button clicked with selector: {selector}")
                        return True
                except:
                    continue
            
            self.logger.warning("Could not find confirmation OK button")
            return False
        except Exception as e:
            self.logger.error(f"Error clicking confirmation OK: {e}")
            return False
    
    def get_order_details(self) -> dict:
        """
        Get order details from confirmation modal
        
        Returns:
            dict: Order details
        """
        try:
            # Wait a few seconds for the modal to fully load
            import time
            time.sleep(3)
            
            order_details = {}
            
            # Use the working selector
            selectors = [
                (By.XPATH, "//div[contains(@class, 'sweet-alert')]//p[contains(@class, 'text-muted')]"),
                (By.XPATH, "//div[contains(@class, 'sweet-alert')]//p"),
                (By.XPATH, "//p[contains(@class, 'text-muted')]")
            ]
            
            order_text = ""
            for selector in selectors:
                try:
                    element = self.find_element(selector)
                    order_text = element.text
                    if order_text and order_text.strip():
                        self.logger.info(f"Found order text with selector: {selector}")
                        break
                except:
                    continue
            
            if not order_text:
                self.logger.warning("No order details text found")
                return {}
            
            # Parse the order text - it's separated by <br> tags in HTML, so split by newlines
            lines = order_text.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('Id:'):
                    order_details['id'] = line
                elif line.startswith('Amount:'):
                    order_details['amount'] = line
                elif line.startswith('Card Number:'):
                    order_details['card'] = line
                elif line.startswith('Name:'):
                    order_details['name'] = line
                elif line.startswith('Date:'):
                    order_details['date'] = line
            
            self.logger.info(f"Order details retrieved: {order_details}")
            return order_details
                
        except Exception as e:
            self.logger.error(f"Error getting order details: {e}")
            return {}
    
    def handle_checkout_error(self) -> str:
        """
        Handle checkout errors and get error message
        
        Returns:
            str: Error message
        """
        try:
            # Check for alerts
            if self.wait_for_alert(timeout=3):
                error_message = self.get_alert_text()
                self.accept_alert()
                self.logger.error(f"Checkout error: {error_message}")
                return error_message
            
            # Check for validation errors
            if self.is_element_visible(self.CHECKOUT_MODAL, timeout=2):
                self.logger.warning("Checkout modal still visible - possible validation error")
                return "Validation error - please check form fields"
            
            return ""
        except Exception as e:
            self.logger.error(f"Error handling checkout error: {e}")
            return str(e)
    
    def verify_form_validation(self) -> bool:
        """
        Verify form validation is working
        
        Returns:
            bool: True if validation is working
        """
        try:
            # Try to submit empty form
            if self.click_purchase():
                # Check for validation alert
                if self.wait_for_alert(timeout=3):
                    alert = self.driver.switch_to.alert
                    alert_text = alert.text
                    self.logger.info(f"Validation alert appeared: {alert_text}")
                    alert.accept()
                    
                    # Check if modal is still visible after accepting alert
                    if self.is_element_visible(self.CHECKOUT_MODAL, timeout=2):
                        self.logger.info("Form validation working - modal still visible after alert")
                        return True
                else:
                    # If no alert, check if modal is still visible
                    if self.is_element_visible(self.CHECKOUT_MODAL, timeout=2):
                        self.logger.info("Form validation working - modal still visible")
                        return True
            
            return False
        except Exception as e:
            self.logger.error(f"Error verifying form validation: {e}")
            return False
    
    def clear_form(self) -> bool:
        """
        Clear all form fields
        
        Returns:
            bool: True if successful
        """
        try:
            fields = [
                self.NAME_INPUT,
                self.COUNTRY_INPUT,
                self.CITY_INPUT,
                self.CREDIT_CARD_INPUT,
                self.MONTH_INPUT,
                self.YEAR_INPUT
            ]
            
            for field in fields:
                try:
                    element = self.find_element(field)
                    element.clear()
                except:
                    continue
            
            self.logger.info("Form cleared")
            return True
        except Exception as e:
            self.logger.error(f"Error clearing form: {e}")
            return False
    
    def is_form_complete(self) -> bool:
        """
        Check if all required form fields are filled
        
        Returns:
            bool: True if form is complete
        """
        try:
            fields = [
                self.NAME_INPUT,
                self.COUNTRY_INPUT,
                self.CITY_INPUT,
                self.CREDIT_CARD_INPUT,
                self.MONTH_INPUT,
                self.YEAR_INPUT
            ]
            
            for field in fields:
                try:
                    element = self.find_element(field)
                    if not element.get_attribute('value'):
                        self.logger.warning(f"Field not filled: {field}")
                        return False
                except:
                    return False
            
            self.logger.info("Form is complete")
            return True
        except Exception as e:
            self.logger.error(f"Error checking form completion: {e}")
            return False