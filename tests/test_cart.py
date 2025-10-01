"""
Test cases for Shopping Cart functionality
"""

import pytest
import logging
from config.config import Config


class TestCart:
    """Test class for cart functionality"""
    
    def test_cart_page_loading(self, driver, cart_page):
        """
        Test: Cart page loading
        
        Verifies that the cart page loads correctly.
        """
        logging.info("Starting cart page loading test")
        
        # Navigate to cart
        driver.get(f"{Config.BASE_URL}/cart.html")
        
        # Verify page is loaded
        assert cart_page.is_cart_page_loaded(), "Cart page should load correctly"
        
        # Verify main elements
        assert cart_page.is_element_present(cart_page.CART_TITLE), "Cart title should be present"
        
        logging.info("Cart page loading test completed")
    
    def test_empty_cart_display(self, driver, cart_page):
        """
        Test: Empty cart display
        
        Verifies that empty cart is displayed correctly.
        """
        logging.info("Starting empty cart test")
        
        # Navigate to cart
        driver.get(f"{Config.BASE_URL}/cart.html")
        
        # Verify cart is empty
        assert cart_page.is_cart_empty(), "Cart should be empty initially"
        
        # Verify no products
        products = cart_page.get_cart_products()
        assert len(products) == 0, "Should have no products in empty cart"
        
        # Verify count
        cart_count = cart_page.get_cart_count()
        assert cart_count == 0, f"Cart count should be 0, got {cart_count}"
        
        logging.info("Empty cart test completed")
    
    def test_add_products_to_cart_and_verify(self, driver, home_page, cart_page):
        """
        Test: Add products to cart and verify
        
        Verifies that products can be added to cart and displayed correctly.
        """
        logging.info("Starting add products to cart test")
        
        # Add one product to cart
        driver.get(Config.BASE_URL)
        home_page.wait_for_products_to_load()
        all_products = home_page.get_products_on_page()
        
        # Add first product
        product_name = all_products[0]['title']
        logging.info(f"Adding product: {product_name}")
        
        # Add product to cart
        assert home_page.add_product_to_cart(product_name), f"Should add product: {product_name}"
        
        # Navigate to cart
        assert home_page.go_to_cart(), "Should navigate to cart"
        
        # Verify products in cart
        cart_products = cart_page.get_cart_products()
        assert len(cart_products) >= 1, f"Should have at least 1 product in cart, got {len(cart_products)}"
        
        # Verify cart contains the product we added
        cart_titles = [product['title'] for product in cart_products]
        assert product_name in cart_titles, f"Cart should contain {product_name}, got {cart_titles}"
        
        logging.info("Add products to cart test completed")
    
    def test_cart_product_information(self, driver, home_page, cart_page):
        """
        Test: Cart product information
        
        Verifies that product information is displayed correctly in cart.
        """
        logging.info("Starting cart product information test")
        
        # Add a product to cart
        driver.get(Config.BASE_URL)
        home_page.wait_for_products_to_load()
        
        # Add first product to cart
        assert home_page.add_first_product_to_cart(), "Should add first product to cart"
        
        # Navigate to cart
        assert home_page.go_to_cart(), "Should navigate to cart"
        
        # Verify product information in cart
        cart_products = cart_page.get_cart_products()
        assert len(cart_products) > 0, "Should have products in cart"
        
        cart_product = cart_products[0]
        assert cart_product['title'], "Product should have a title"
        assert cart_product['price'], "Product should have a price"
        assert cart_product['delete_button'], "Product should have a delete button"
        
        logging.info("Cart product information test completed")
    
    def test_delete_product_from_cart(self, driver, home_page, cart_page):
        """
        Test: Delete product from cart
        
        Verifies that products can be deleted from cart.
        """
        logging.info("Starting delete product from cart test")
        
        # Add products to cart
        driver.get(Config.BASE_URL)
        home_page.wait_for_products_to_load()
        
        # Add first product
        assert home_page.add_first_product_to_cart(), "Should add first product to cart"
        
        # Navigate to cart
        assert home_page.go_to_cart(), "Should navigate to cart"
        
        # Get initial count
        initial_count = cart_page.get_cart_count()
        assert initial_count > 0, "Should have products in cart"
        
        # Delete first product
        assert cart_page.delete_product(0), "Should delete first product"
        
        # Verify count decreased
        new_count = cart_page.get_cart_count()
        assert new_count == initial_count - 1, f"Cart count should decrease from {initial_count} to {new_count}"
        
        logging.info("Delete product from cart test completed")
    
    def test_delete_product_by_name(self, driver, home_page, cart_page):
        """
        Test: Delete product by name
        
        Verifies that products can be deleted by name.
        """
        logging.info("Starting delete product by name test")
        
        # Add specific product to cart
        driver.get(Config.BASE_URL)
        home_page.wait_for_products_to_load()
        
        # Get first product name
        products = home_page.get_products_on_page()
        assert len(products) > 0, "Should have products on page"
        
        product_name = products[0]['title']
        
        # Add to cart
        assert home_page.add_product_to_cart(product_name), f"Should add product: {product_name}"
        
        # Navigate to cart
        assert home_page.go_to_cart(), "Should navigate to cart"
        
        # Verify product is in cart
        cart_products = cart_page.get_cart_products()
        assert len(cart_products) > 0, "Should have products in cart"
        
        # Delete by name
        assert cart_page.delete_product_by_name(product_name), f"Should delete product: {product_name}"
        
        # Verify product is deleted
        new_cart_products = cart_page.get_cart_products()
        assert len(new_cart_products) == 0, "Cart should be empty after deletion"
        
        logging.info("Delete product by name test completed")
    
    def test_cart_total_calculation(self, driver, home_page, cart_page):
        """
        Test: Cart total calculation
        
        Verifies that cart total is calculated correctly.
        """
        logging.info("Starting cart total calculation test")
        
        # Add one product to cart
        driver.get(Config.BASE_URL)
        home_page.wait_for_products_to_load()
        
        # Add first product
        assert home_page.add_first_product_to_cart(), "Should add first product to cart"
        
        # Navigate to cart
        assert home_page.go_to_cart(), "Should navigate to cart"
        
        # Get cart products
        cart_products = cart_page.get_cart_products()
        assert len(cart_products) > 0, "Should have products in cart"
        
        # Calculate expected total
        expected_total = cart_page.calculate_expected_total(cart_products)
        
        # Verify total
        assert cart_page.verify_total_price(expected_total), f"Cart total should be {expected_total}"
        
        logging.info("Cart total calculation test completed")
    
    def test_clear_cart(self, driver, home_page, cart_page):
        """
        Test: Clear cart
        
        Verifies that cart can be cleared completely.
        """
        logging.info("Starting clear cart test")
        
        # Add products to cart
        driver.get(Config.BASE_URL)
        home_page.wait_for_products_to_load()
        
        # Add multiple products
        for i in range(3):
            assert home_page.add_first_product_to_cart(), f"Should add product {i+1}"
        
        # Navigate to cart
        assert home_page.go_to_cart(), "Should navigate to cart"
        
        # Verify products are in cart
        initial_count = cart_page.get_cart_count()
        assert initial_count > 0, "Should have products in cart"
        
        # Clear cart
        assert cart_page.clear_cart(), "Should clear cart"
        
        # Verify cart is empty
        assert cart_page.is_cart_empty(), "Cart should be empty after clearing"
        
        final_count = cart_page.get_cart_count()
        assert final_count == 0, f"Cart count should be 0, got {final_count}"
        
        logging.info("Clear cart test completed")
    
    def test_place_order_button(self, driver, home_page, cart_page):
        """
        Test: Place order button
        
        Verifies that place order button is present and clickable.
        """
        logging.info("Starting place order button test")
        
        # Add product to cart
        driver.get(Config.BASE_URL)
        home_page.wait_for_products_to_load()
        assert home_page.add_first_product_to_cart(), "Should add product to cart"
        
        # Navigate to cart
        assert home_page.go_to_cart(), "Should navigate to cart"
        
        # Verify place order button is present
        assert cart_page.is_element_present(cart_page.PLACE_ORDER_BUTTON), "Place order button should be present"
        
        # Verify button is clickable
        assert cart_page.is_element_clickable(cart_page.PLACE_ORDER_BUTTON), "Place order button should be clickable"
        
        # Click place order button
        assert cart_page.place_order(), "Should be able to click place order button"
        
        logging.info("Place order button test completed")
    
    def test_cart_navigation(self, driver, cart_page):
        """
        Test: Cart navigation
        
        Verifies navigation from cart page.
        """
        logging.info("Starting cart navigation test")
        
        # Navigate to cart
        driver.get(f"{Config.BASE_URL}/cart.html")
        
        # Verify cart page loaded
        assert cart_page.is_cart_page_loaded(), "Cart page should load"
        
        # Navigate to home
        assert cart_page.go_to_home(), "Should navigate to home from cart"
        
        # Verify home page loaded
        current_url = cart_page.get_current_url()
        assert Config.BASE_URL in current_url, f"Should be on home page, current URL: {current_url}"
        
        logging.info("Cart navigation test completed")
    
    def test_cart_summary(self, driver, home_page, cart_page):
        """
        Test: Cart summary
        
        Verifies that cart summary provides correct information.
        """
        logging.info("Starting cart summary test")
        
        # Add products to cart
        driver.get(Config.BASE_URL)
        home_page.wait_for_products_to_load()
        
        # Add multiple products
        for i in range(2):
            assert home_page.add_first_product_to_cart(), f"Should add product {i+1}"
        
        # Navigate to cart
        assert home_page.go_to_cart(), "Should navigate to cart"
        
        # Get cart summary
        summary = cart_page.get_cart_summary()
        
        # Verify summary information
        assert summary['product_count'] > 0, "Should have products in summary"
        assert summary['total'] > 0, "Should have total price in summary"
        assert not summary['is_empty'], "Cart should not be empty"
        
        logging.info(f"Cart summary: {summary['product_count']} products, total: {summary['total']}")
        logging.info("Cart summary test completed")
    
    def test_cart_page_elements_visibility(self, driver, cart_page):
        """
        Test: Cart page elements visibility
        
        Verifies that all cart page elements are visible.
        """
        logging.info("Starting cart page elements visibility test")
        
        # Navigate to cart
        driver.get(f"{Config.BASE_URL}/cart.html")
        
        # Verify main elements are visible
        main_elements = [
            cart_page.CART_TITLE,
            cart_page.PLACE_ORDER_BUTTON
        ]
        
        for element in main_elements:
            assert cart_page.is_element_visible(element), f"Element should be visible: {element}"
        
        logging.info("Cart page elements visibility test completed")
    
    def test_cart_with_no_products(self, driver, cart_page):
        """
        Test: Cart with no products
        
        Verifies cart behavior when empty.
        """
        logging.info("Starting cart with no products test")
        
        # Navigate to cart
        driver.get(f"{Config.BASE_URL}/cart.html")
        
        # Verify cart is empty
        assert cart_page.is_cart_empty(), "Cart should be empty"
        
        # Verify no products
        products = cart_page.get_cart_products()
        assert len(products) == 0, "Should have no products"
        
        # Verify total is 0
        total = cart_page.get_cart_total_numeric()
        assert total == 0, f"Total should be 0, got {total}"
        
        logging.info("Cart with no products test completed")
    
    def test_cart_persistence(self, driver, home_page, cart_page):
        """
        Test: Cart persistence
        
        Verifies that cart contents persist across page navigation.
        """
        logging.info("Starting cart persistence test")
        
        # Add product to cart
        driver.get(Config.BASE_URL)
        home_page.wait_for_products_to_load()
        assert home_page.add_first_product_to_cart(), "Should add product to cart"
        
        # Navigate to cart
        assert home_page.go_to_cart(), "Should navigate to cart"
        
        # Verify product is in cart
        cart_products = cart_page.get_cart_products()
        assert len(cart_products) > 0, "Should have products in cart"
        
        # Navigate back to home
        assert cart_page.go_to_home(), "Should navigate to home"
        
        # Navigate back to cart
        assert home_page.go_to_cart(), "Should navigate to cart again"
        
        # Verify product is still in cart
        cart_products_after = cart_page.get_cart_products()
        assert len(cart_products_after) > 0, "Product should persist in cart"
        
        logging.info("Cart persistence test completed")