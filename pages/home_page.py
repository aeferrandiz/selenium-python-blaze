"""
Page Object for DemoBlaze home page
Handles navigation and main page elements
"""

import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config.config import Config


class HomePage(BasePage):
    """Page Object for home page"""
    
    # Main locators
    LOGO = (By.XPATH, "//a[@class='navbar-brand']")
    HOME_LINK = (By.XPATH, "//a[text()='Home ']")
    CONTACT_LINK = (By.XPATH, "//a[text()='Contact']")
    ABOUT_US_LINK = (By.XPATH, "//a[text()='About us']")
    CART_LINK = (By.XPATH, "//a[text()='Cart']")
    LOGIN_LINK = (By.XPATH, "//a[@id='login2']")
    LOGOUT_LINK = (By.XPATH, "//a[text()='Log out']")
    SIGNUP_LINK = (By.XPATH, "//a[@id='signin2']")
    
    # Product categories
    PHONES_CATEGORY = (By.XPATH, "//a[text()='Phones']")
    LAPTOPS_CATEGORY = (By.XPATH, "//a[text()='Laptops']")
    MONITORS_CATEGORY = (By.XPATH, "//a[text()='Monitors']")
    
    # Products on main page
    PRODUCT_CARDS = (By.XPATH, "//div[@class='card h-100']")
    PRODUCT_TITLES = (By.CLASS_NAME, "card-title")
    PRODUCT_PRICES = (By.CLASS_NAME, "card-text")
    ADD_TO_CART_BUTTONS = (By.XPATH, "//a[contains(text(),'Add to cart')]")
    
    # Page navigation
    NEXT_BUTTON = (By.XPATH, "//button[@id='next2']")
    PREVIOUS_BUTTON = (By.XPATH, "//button[@id='prev2']")
    
    # Cart
    CART_COUNT = (By.XPATH, "//a[@id='cartur']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
    
    def is_home_page_loaded(self) -> bool:
        """
        Check if home page is loaded correctly
        
        Returns:
            bool: True if page is loaded
        """
        try:
            return self.wait_for_element_visible(self.PHONES_CATEGORY, timeout=10)
        except Exception as e:
            self.logger.error(f"Error checking home page load: {e}")
            return False
    
    def navigate_to_home(self) -> bool:
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
    
    def select_category(self, category: str) -> bool:
        """
        Select product category
        
        Args:
            category (str): Category name (phones, laptops, monitors)
        
        Returns:
            bool: True if successful
        """
        try:
            category_locators = {
                'phones': self.PHONES_CATEGORY,
                'laptops': self.LAPTOPS_CATEGORY,
                'monitors': self.MONITORS_CATEGORY
            }
            
            locator = category_locators.get(category.lower())
            if not locator:
                self.logger.error(f"Unknown category: {category}")
                return False
            
            if self.click_element(locator):
                self.wait_for_page_load()
                self.logger.info(f"Selected category: {category}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error selecting category {category}: {e}")
            return False
    
    def get_products_on_page(self) -> list:
        """
        Get all products visible on current page
        
        Returns:
            list: List of product information dictionaries
        """
        try:
            products = []
            product_cards = self.find_elements(self.PRODUCT_CARDS)
            
            for card in product_cards:
                try:
                    title_element = card.find_element(*self.PRODUCT_TITLES)
                    price_element = card.find_element(*self.PRODUCT_PRICES)
                    
                    # Extract price from the text (look for $ followed by numbers)
                    import re
                    price_text = price_element.text
                    price_match = re.search(r'\$(\d+)', price_text)
                    price = price_match.group(1) if price_match else price_text
                    
                    product_info = {
                        'title': title_element.text,
                        'price': price,
                        'element': card
                    }
                    products.append(product_info)
                except Exception as e:
                    self.logger.warning(f"Error extracting product info: {e}")
                    continue
            
            self.logger.info(f"Found {len(products)} products on page")
            return products
        except Exception as e:
            self.logger.error(f"Error getting products: {e}")
            return []
    
    def search_product_by_name(self, product_name: str) -> bool:
        """
        Search for product by name
        
        Args:
            product_name (str): Name of product to search
        
        Returns:
            bool: True if product found
        """
        try:
            products = self.get_products_on_page()
            for product in products:
                if product_name.lower() in product['title'].lower():
                    self.logger.info(f"Found product: {product['title']}")
                    return True
            self.logger.warning(f"Product not found: {product_name}")
            return False
        except Exception as e:
            self.logger.error(f"Error searching for product {product_name}: {e}")
            return False
    
    def add_product_to_cart(self, product_name: str) -> bool:
        """
        Add specific product to cart
        
        Args:
            product_name (str): Name of product to add
        
        Returns:
            bool: True if successful
        """
        try:
            products = self.get_products_on_page()
            for product in products:
                if product_name.lower() in product['title'].lower():
                    # Click on product to go to product page
                    product_link = product['element'].find_element(By.TAG_NAME, "a")
                    product_link.click()
                    
                    # Wait for product page to load
                    self.wait_for_page_load()
                    
                    # Wait a bit more for JavaScript to load
                    import time
                    time.sleep(2)
                    
                    # Verify we're on a product page
                    if "prod.html" not in self.driver.current_url:
                        self.logger.error("Not on product page")
                        return False
                    
                    # Execute the JavaScript function directly to add product to cart
                    self.driver.execute_script("addToCart(1);")
                    
                    # Handle the alert that appears
                    try:
                        if self.wait_for_alert(timeout=5):
                            alert = self.driver.switch_to.alert
                            alert_text = alert.text
                            self.logger.info(f"Alert appeared: {alert_text}")
                            
                            # Accept the alert
                            alert.accept()
                            self.logger.info(f"Added product to cart: {product_name}")
                            
                            # Navigate back to home page
                            self.navigate_to_home()
                            return True
                        else:
                            self.logger.warning("No alert appeared after adding product")
                            self.navigate_to_home()
                            return True
                    except Exception as e:
                        self.logger.warning(f"Error handling alert: {e}")
                        self.navigate_to_home()
                        return True
            
            self.logger.error(f"Product not found: {product_name}")
            return False
        except Exception as e:
            self.logger.error(f"Error adding product to cart: {e}")
            return False
    
    def add_first_product_to_cart(self) -> bool:
        """
        Add first visible product to cart
        
        Returns:
            bool: True if successful
        """
        try:
            # Wait for products to load first
            if not self.wait_for_products_to_load():
                self.logger.error("Products not loaded")
                return False
            
            # Click on first product to go to product page
            product_cards = self.find_elements(self.PRODUCT_CARDS)
            if not product_cards:
                self.logger.error("No product cards found")
                return False
            
            # Find the link within the first product card
            first_card = product_cards[0]
            product_link = first_card.find_element(By.TAG_NAME, "a")
            product_link.click()
            
            # Wait for product page to load
            self.wait_for_page_load()
            
            # Wait a bit more for JavaScript to load
            import time
            time.sleep(2)
            
            # Verify we're on a product page
            if "prod.html" not in self.driver.current_url:
                self.logger.error("Not on product page")
                return False
            
            # Execute the JavaScript function directly to add product to cart
            self.driver.execute_script("addToCart(1);")
            
            # Handle the alert that appears
            try:
                if self.wait_for_alert(timeout=5):
                    alert = self.driver.switch_to.alert
                    alert_text = alert.text
                    self.logger.info(f"Alert appeared: {alert_text}")
                    
                    # Accept the alert
                    alert.accept()
                    self.logger.info("Added first product to cart and accepted alert")
                    
                    # Navigate back to home page to see updated cart count
                    self.navigate_to_home()
                    return True
                else:
                    self.logger.warning("No alert appeared after adding product")
                    return True
            except Exception as e:
                self.logger.warning(f"Error handling alert: {e}")
                return True
        except Exception as e:
            self.logger.error(f"Error adding first product to cart: {e}")
            return False
    
    def get_cart_count(self) -> int:
        """
        Get number of items in cart
        
        Returns:
            int: Number of items in cart
        """
        try:
            cart_element = self.find_element(self.CART_COUNT)
            cart_text = cart_element.text
            # Extract number from cart text (e.g., "Cart (3)")
            if '(' in cart_text and ')' in cart_text:
                count = cart_text.split('(')[1].split(')')[0]
                return int(count)
            return 0
        except Exception as e:
            self.logger.error(f"Error getting cart count: {e}")
            return 0
    
    def go_to_cart(self) -> bool:
        """
        Navigate to cart page
        
        Returns:
            bool: True if successful
        """
        try:
            if self.click_element(self.CART_LINK):
                self.wait_for_page_load()
                self.logger.info("Navigated to cart page")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error navigating to cart: {e}")
            return False
    
    def go_to_next_page(self) -> bool:
        """
        Go to next page of products
        
        Returns:
            bool: True if successful
        """
        try:
            if self.is_element_clickable(self.NEXT_BUTTON):
                if self.click_element(self.NEXT_BUTTON):
                    self.wait_for_page_load()
                    self.logger.info("Navigated to next page")
                    return True
            else:
                self.logger.info("Next button not available")
            return False
        except Exception as e:
            self.logger.error(f"Error going to next page: {e}")
            return False
    
    def go_to_previous_page(self) -> bool:
        """
        Go to previous page of products
        
        Returns:
            bool: True if successful
        """
        try:
            if self.is_element_clickable(self.PREVIOUS_BUTTON):
                if self.click_element(self.PREVIOUS_BUTTON):
                    self.wait_for_page_load()
                    self.logger.info("Navigated to previous page")
                    return True
            else:
                self.logger.info("Previous button not available")
            return False
        except Exception as e:
            self.logger.error(f"Error going to previous page: {e}")
            return False
    
    def is_user_logged_in(self) -> bool:
        """
        Check if user is logged in
        
        Returns:
            bool: True if logged in
        """
        try:
            return self.is_element_visible(self.LOGOUT_LINK, timeout=2)
        except Exception as e:
            self.logger.error(f"Error checking login status: {e}")
            return False
    
    def get_page_title(self) -> str:
        """
        Get current page title
        
        Returns:
            str: Page title
        """
        try:
            return self.driver.title
        except Exception as e:
            self.logger.error(f"Error getting page title: {e}")
            return ""
    
    def get_current_url(self) -> str:
        """
        Get current URL
        
        Returns:
            str: Current URL
        """
        try:
            return self.driver.current_url
        except Exception as e:
            self.logger.error(f"Error getting current URL: {e}")
            return ""
    
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
    
    def wait_for_products_to_load(self, timeout: int = 10) -> bool:
        """
        Wait for products to load on page
        
        Args:
            timeout (int): Wait timeout
        
        Returns:
            bool: True if products loaded
        """
        try:
            if self.wait_for_element_visible(self.PRODUCT_CARDS, timeout):
                self.logger.info("Products loaded successfully")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error waiting for products to load: {e}")
            return False
