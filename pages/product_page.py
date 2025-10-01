"""
Page Object for individual product page
Handles product display and specific actions
"""

import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config.config import Config


class ProductPage(BasePage):
    """Page Object for individual product pages"""
    
    # Product locators
    PRODUCT_TITLE = (By.XPATH, "//h2[@class='name']")
    PRODUCT_PRICE = (By.XPATH, "//h3[@class='price-container']")
    PRODUCT_DESCRIPTION = (By.XPATH, "//div[@id='more-information']")
    ADD_TO_CART_BUTTON = (By.XPATH, "//a[text()='Add to cart']")
    
    # Navigation
    BACK_TO_PRODUCTS = (By.XPATH, "//button[text()='Add to cart']/following-sibling::a")
    HOME_LINK = (By.XPATH, "//a[text()='Home ']")
    
    # Product image
    PRODUCT_IMAGE = (By.XPATH, "//div[@class='item active']//img")
    
    # Additional information
    PRODUCT_ID = (By.XPATH, "//small[@class='text-muted']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
    
    def get_product_title(self) -> str:
        """
        Get current product title
        
        Returns:
            str: Product title
        """
        try:
            title = self.get_text(self.PRODUCT_TITLE)
            self.logger.info(f"Product title: {title}")
            return title
        except Exception as e:
            self.logger.error(f"Error getting product title: {e}")
            return ""
    
    def get_product_price(self) -> str:
        """
        Get current product price
        
        Returns:
            str: Product price
        """
        try:
            price = self.get_text(self.PRODUCT_PRICE)
            self.logger.info(f"Product price: {price}")
            return price
        except Exception as e:
            self.logger.error(f"Error getting product price: {e}")
            return ""
    
    def get_product_description(self) -> str:
        """
        Get product description
        
        Returns:
            str: Product description
        """
        try:
            description = self.get_text(self.PRODUCT_DESCRIPTION)
            self.logger.info(f"Product description: {description}")
            return description
        except Exception as e:
            self.logger.error(f"Error getting product description: {e}")
            return ""
    
    def add_to_cart(self) -> bool:
        """
        Add current product to cart
        
        Returns:
            bool: True if successful
        """
        try:
            if self.click_element(self.ADD_TO_CART_BUTTON):
                # Handle alert
                if self.wait_for_alert(timeout=3):
                    alert_text = self.get_alert_text()
                    self.accept_alert()
                    self.logger.info(f"Product added to cart: {alert_text}")
                    return True
                else:
                    self.logger.warning("No alert after adding to cart")
                    return True  # Still consider success
            return False
        except Exception as e:
            self.logger.error(f"Error adding product to cart: {e}")
            return False
    
    def go_back_to_products(self) -> bool:
        """
        Go back to products list
        
        Returns:
            bool: True if successful
        """
        try:
            if self.click_element(self.BACK_TO_PRODUCTS):
                self.wait_for_page_load()
                self.logger.info("Navigated back to products")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error going back to products: {e}")
            return False
    
    def go_to_home(self) -> bool:
        """
        Navigate to home page
        
        Returns:
            bool: True if successful
        """
        try:
            if self.click_element(self.HOME_LINK):
                self.wait_for_page_load()
                self.logger.info("Navigated to home page")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error navigating to home: {e}")
            return False
    
    def get_product_image_src(self) -> str:
        """
        Get product image source
        
        Returns:
            str: Image source URL
        """
        try:
            image_element = self.find_element(self.PRODUCT_IMAGE)
            src = image_element.get_attribute('src')
            self.logger.debug(f"Product image source: {src}")
            return src
        except Exception as e:
            self.logger.error(f"Error getting product image: {e}")
            return ""
    
    def get_product_id(self) -> str:
        """
        Get product ID
        
        Returns:
            str: Product ID
        """
        try:
            id_element = self.find_element(self.PRODUCT_ID)
            product_id = id_element.text
            self.logger.debug(f"Product ID: {product_id}")
            return product_id
        except Exception as e:
            self.logger.error(f"Error getting product ID: {e}")
            return ""
    
    def is_product_available(self) -> bool:
        """
        Check if product is available for purchase
        
        Returns:
            bool: True if available
        """
        try:
            return self.is_element_visible(self.ADD_TO_CART_BUTTON, timeout=2)
        except Exception as e:
            self.logger.error(f"Error checking product availability: {e}")
            return False
    
    def get_product_info(self) -> dict:
        """
        Get complete product information
        
        Returns:
            dict: Product information
        """
        try:
            product_info = {
                'title': self.get_product_title(),
                'price': self.get_product_price(),
                'description': self.get_product_description(),
                'image_src': self.get_product_image_src(),
                'product_id': self.get_product_id(),
                'available': self.is_product_available()
            }
            self.logger.info(f"Product info retrieved: {product_info['title']}")
            return product_info
        except Exception as e:
            self.logger.error(f"Error getting product info: {e}")
            return {}
    
    def wait_for_product_to_load(self, timeout: int = 10) -> bool:
        """
        Wait for product page to load completely
        
        Args:
            timeout (int): Wait timeout
        
        Returns:
            bool: True if loaded
        """
        try:
            if self.wait_for_element_visible(self.PRODUCT_TITLE, timeout):
                self.logger.info("Product page loaded successfully")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error waiting for product to load: {e}")
            return False
    
    def verify_product_page_elements(self) -> bool:
        """
        Verify all essential product page elements are present
        
        Returns:
            bool: True if all elements present
        """
        try:
            elements = [
                self.PRODUCT_TITLE,
                self.PRODUCT_PRICE,
                self.ADD_TO_CART_BUTTON
            ]
            
            for element in elements:
                if not self.is_element_present(element, timeout=2):
                    self.logger.error(f"Required element not present: {element}")
                    return False
            
            self.logger.info("All product page elements verified")
            return True
        except Exception as e:
            self.logger.error(f"Error verifying product page elements: {e}")
            return False
    
    def take_product_screenshot(self, filename: str = None) -> str:
        """
        Take screenshot of product page
        
        Args:
            filename (str): Screenshot filename
        
        Returns:
            str: Screenshot path
        """
        try:
            if not filename:
                product_title = self.get_product_title().replace(' ', '_')
                filename = f"product_{product_title}.png"
            
            screenshot_path = self.take_screenshot(filename)
            self.logger.info(f"Product screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            self.logger.error(f"Error taking product screenshot: {e}")
            return ""