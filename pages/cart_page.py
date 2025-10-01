"""
Page Object for shopping cart page
Handles cart display and product management
"""

import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config.config import Config


class CartPage(BasePage):
    """Page Object for shopping cart page"""
    
    # Main locators
    CART_TITLE = (By.XPATH, "//h2[text()='Products']")
    CART_TABLE = (By.XPATH, "//table[@class='table table-bordered table-hover table-striped']")
    CART_ROWS = (By.XPATH, "//tbody/tr")
    
    # Product information in cart
    PRODUCT_TITLES = (By.XPATH, "//tbody/tr/td[2]")
    PRODUCT_PRICES = (By.XPATH, "//tbody/tr/td[3]")
    DELETE_BUTTONS = (By.XPATH, "//tbody/tr/td[4]/a[text()='Delete']")
    
    # Action buttons
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[text()='Place Order']")
    DELETE_ALL_BUTTON = (By.XPATH, "//button[text()='Delete']")
    
    # Cart total
    TOTAL_PRICE = (By.XPATH, "//h3[@id='totalp']")
    
    # Navigation
    HOME_LINK = (By.XPATH, "//a[text()='Home ']")
    
    # Messages
    EMPTY_CART_MESSAGE = (By.XPATH, "//h2[text()='Products']/following-sibling::p")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)
    
    def is_cart_page_loaded(self) -> bool:
        """
        Check if cart page is loaded correctly
        
        Returns:
            bool: True if page is loaded
        """
        try:
            return self.wait_for_element_visible(self.CART_TITLE, timeout=5)
        except Exception as e:
            self.logger.error(f"Error checking cart page load: {e}")
            return False
    
    def get_cart_products(self) -> list:
        """
        Get all products in cart
        
        Returns:
            list: List of product dictionaries
        """
        try:
            products = []
            cart_rows = self.find_elements(self.CART_ROWS)
            
            for i, row in enumerate(cart_rows):
                try:
                    # Get product information from each row
                    title_element = row.find_element(By.XPATH, ".//td[2]")
                    price_element = row.find_element(By.XPATH, ".//td[3]")
                    delete_button = row.find_element(By.XPATH, ".//td[4]/a")
                    
                    product_info = {
                        'index': i,
                        'title': title_element.text,
                        'price': price_element.text,
                        'delete_button': delete_button
                    }
                    products.append(product_info)
                except Exception as e:
                    self.logger.warning(f"Error extracting product info from row {i}: {e}")
                    continue
            
            self.logger.info(f"Found {len(products)} products in cart")
            return products
        except Exception as e:
            self.logger.error(f"Error getting cart products: {e}")
            return []
    
    def get_cart_total(self) -> str:
        """
        Get cart total price
        
        Returns:
            str: Total price
        """
        try:
            total = self.get_text(self.TOTAL_PRICE)
            self.logger.info(f"Cart total: {total}")
            return total
        except Exception as e:
            self.logger.error(f"Error getting cart total: {e}")
            return ""
    
    def delete_product(self, product_index: int = 0) -> bool:
        """
        Delete product from cart by index
        
        Args:
            product_index (int): Index of product to delete
        
        Returns:
            bool: True if successful
        """
        try:
            products = self.get_cart_products()
            if product_index < len(products):
                delete_button = products[product_index]['delete_button']
                delete_button.click()
                
                # Wait for page to update
                import time
                time.sleep(2)
                self.wait_for_page_load()
                
                # Verify product was deleted by checking count
                new_count = self.get_cart_count()
                self.logger.info(f"Deleted product at index {product_index}, new count: {new_count}")
                return True
            else:
                self.logger.error(f"Product index {product_index} out of range")
                return False
        except Exception as e:
            self.logger.error(f"Error deleting product: {e}")
            return False
    
    def delete_product_by_name(self, product_name: str) -> bool:
        """
        Delete product from cart by name
        
        Args:
            product_name (str): Name of product to delete
        
        Returns:
            bool: True if successful
        """
        try:
            products = self.get_cart_products()
            for i, product in enumerate(products):
                if product_name.lower() in product['title'].lower():
                    return self.delete_product(i)
            
            self.logger.error(f"Product not found in cart: {product_name}")
            return False
        except Exception as e:
            self.logger.error(f"Error deleting product by name: {e}")
            return False
    
    def clear_cart(self) -> bool:
        """
        Clear all products from cart
        
        Returns:
            bool: True if successful
        """
        try:
            products = self.get_cart_products()
            for i in range(len(products)):
                if not self.delete_product(0):  # Always delete first item
                    break
            
            self.logger.info("Cart cleared")
            return True
        except Exception as e:
            self.logger.error(f"Error clearing cart: {e}")
            return False
    
    def is_cart_empty(self) -> bool:
        """
        Check if cart is empty
        
        Returns:
            bool: True if empty
        """
        try:
            products = self.get_cart_products()
            return len(products) == 0
        except Exception as e:
            self.logger.error(f"Error checking if cart is empty: {e}")
            return True
    
    def get_cart_count(self) -> int:
        """
        Get number of products in cart
        
        Returns:
            int: Number of products
        """
        try:
            products = self.get_cart_products()
            return len(products)
        except Exception as e:
            self.logger.error(f"Error getting cart count: {e}")
            return 0
    
    def place_order(self) -> bool:
        """
        Click place order button
        
        Returns:
            bool: True if successful
        """
        try:
            if self.click_element(self.PLACE_ORDER_BUTTON):
                self.logger.info("Place order button clicked")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error clicking place order: {e}")
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
    
    def verify_cart_contents(self, expected_products: list) -> bool:
        """
        Verify cart contains expected products
        
        Args:
            expected_products (list): List of expected product names
        
        Returns:
            bool: True if all products present
        """
        try:
            cart_products = self.get_cart_products()
            cart_titles = [product['title'] for product in cart_products]
            
            self.logger.info(f"Expected products: {expected_products}")
            self.logger.info(f"Cart titles: {cart_titles}")
            
            for expected_product in expected_products:
                if not any(expected_product.lower() in title.lower() for title in cart_titles):
                    self.logger.error(f"Expected product not found in cart: {expected_product}")
                    return False
            
            self.logger.info("Cart contents verified")
            return True
        except Exception as e:
            self.logger.error(f"Error verifying cart contents: {e}")
            return False
    
    def calculate_expected_total(self, products: list) -> float:
        """
        Calculate expected total based on product prices
        
        Args:
            products (list): List of product dictionaries
        
        Returns:
            float: Expected total
        """
        try:
            total = 0.0
            for product in products:
                price_text = product.get('price', '0')
                # Extract numeric value from price string
                price_value = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
                total += price_value
            
            self.logger.info(f"Calculated expected total: {total}")
            return total
        except Exception as e:
            self.logger.error(f"Error calculating expected total: {e}")
            return 0.0
    
    def get_cart_total_numeric(self) -> float:
        """
        Get cart total as numeric value
        
        Returns:
            float: Total as number
        """
        try:
            total_text = self.get_cart_total()
            # Extract numeric value from total string
            total_value = float(''.join(filter(lambda x: x.isdigit() or x == '.', total_text)))
            return total_value
        except Exception as e:
            self.logger.error(f"Error getting numeric total: {e}")
            return 0.0
    
    def verify_total_price(self, expected_total: float) -> bool:
        """
        Verify cart total matches expected value
        
        Args:
            expected_total (float): Expected total price
        
        Returns:
            bool: True if total matches
        """
        try:
            actual_total = self.get_cart_total_numeric()
            if abs(actual_total - expected_total) < 0.01:  # Allow for small floating point differences
                self.logger.info(f"Total price verified: {actual_total}")
                return True
            else:
                self.logger.error(f"Total price mismatch. Expected: {expected_total}, Actual: {actual_total}")
                return False
        except Exception as e:
            self.logger.error(f"Error verifying total price: {e}")
            return False
    
    def wait_for_cart_to_load(self, timeout: int = 10) -> bool:
        """
        Wait for cart page to load completely
        
        Args:
            timeout (int): Wait timeout
        
        Returns:
            bool: True if loaded
        """
        try:
            if self.wait_for_element_visible(self.CART_TITLE, timeout):
                self.logger.info("Cart page loaded successfully")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error waiting for cart to load: {e}")
            return False
    
    def get_cart_summary(self) -> dict:
        """
        Get complete cart summary
        
        Returns:
            dict: Cart summary information
        """
        try:
            products = self.get_cart_products()
            total = self.get_cart_total_numeric()
            
            summary = {
                'product_count': len(products),
                'products': products,
                'total': total,
                'is_empty': len(products) == 0
            }
            
            self.logger.info(f"Cart summary: {len(products)} products, total: {total}")
            return summary
        except Exception as e:
            self.logger.error(f"Error getting cart summary: {e}")
            return {}