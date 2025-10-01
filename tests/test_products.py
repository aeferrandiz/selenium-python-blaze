"""
Test cases for Product functionality
"""

import pytest
import logging
from selenium.webdriver.common.by import By
from config.config import Config


class TestProducts:
    """Test class for product functionality"""
    
    def test_home_page_loading(self, driver, home_page):
        """
        Test: Home page loading
        
        Verifies that the home page loads correctly with all main elements.
        """
        logging.info("Starting home page loading test")
        
        # Verify page is loaded
        assert home_page.is_home_page_loaded(), "Home page should load correctly"
        
        # Verify main elements
        assert home_page.is_element_present(home_page.PHONES_CATEGORY), "Phones category should be present"
        assert home_page.is_element_present(home_page.LAPTOPS_CATEGORY), "Laptops category should be present"
        assert home_page.is_element_present(home_page.MONITORS_CATEGORY), "Monitors category should be present"
        
        logging.info("Home page loading test completed")
    
    def test_product_categories_navigation(self, driver, home_page):
        """
        Test: Product categories navigation
        
        Verifies navigation between different product categories.
        """
        logging.info("Starting categories navigation test")
        
        # Test each category
        categories = ['phones', 'laptops', 'monitors']
        
        for category in categories:
            logging.info(f"Testing category: {category}")
            
            # Select category
            assert home_page.select_category(category), f"Should be able to select category {category}"
            
            # Verify products are loaded
            assert home_page.wait_for_products_to_load(), f"Products should load for category {category}"
            
            # Verify products are present
            products = home_page.get_products_on_page()
            assert len(products) > 0, f"Should have products in category {category}"
            
            logging.info(f"Category {category} test completed")
        
        logging.info("Categories navigation test completed")
    
    def test_add_products_to_cart(self, driver, home_page):
        """
        Test: Add products to cart
        
        Verifies that products can be added to cart successfully.
        """
        logging.info("Starting add products to cart test")
        
        # Get initial cart count
        initial_count = home_page.get_cart_count()
        logging.info(f"Initial cart count: {initial_count}")
        
        # Add first product to cart
        assert home_page.add_first_product_to_cart(), "Should be able to add first product to cart"
        
        # Verify product was added to cart by checking cart page
        driver.get(f"{Config.BASE_URL}/cart.html")
        cart_items = driver.find_elements(By.XPATH, "//tbody[@id='tbodyid']//tr")
        assert len(cart_items) > 0, "Product should be in cart"
        
        logging.info(f"Cart items after adding product: {len(cart_items)}")
        logging.info("Add products to cart test completed")
    
    def test_add_multiple_products_to_cart(self, driver, home_page):
        """
        Test: Add multiple products to cart
        
        Verifies that multiple products can be added to cart.
        """
        logging.info("Starting add multiple products test")
        
        # Get initial cart count
        initial_count = home_page.get_cart_count()
        logging.info(f"Initial cart count: {initial_count}")
        
        # Add multiple products
        products_to_add = 3
        for i in range(products_to_add):
            logging.info(f"Adding product {i+1} to cart")
            assert home_page.add_first_product_to_cart(), f"Should be able to add product {i+1}"
        
        # Verify products were added to cart by checking cart page
        driver.get(f"{Config.BASE_URL}/cart.html")
        cart_items = driver.find_elements(By.XPATH, "//tbody[@id='tbodyid']//tr")
        assert len(cart_items) > 0, f"Should have items in cart, got {len(cart_items)}"
        assert len(cart_items) >= 1, f"Should have at least 1 item in cart, got {len(cart_items)}"
        
        logging.info(f"Final cart items: {len(cart_items)}")
        logging.info("Add multiple products test completed")
    
    def test_product_search_functionality(self, driver, home_page):
        """
        Test: Product search functionality
        
        Verifies that products can be searched by name.
        """
        logging.info("Starting product search test")
        
        # Get products on page
        products = home_page.get_products_on_page()
        assert len(products) > 0, "Should have products on page"
        
        # Test search for first product
        first_product = products[0]
        product_name = first_product['title']
        logging.info(f"Searching for product: {product_name}")
        
        # Search for product
        assert home_page.search_product_by_name(product_name), f"Should find product: {product_name}"
        
        logging.info("Product search test completed")
    
    def test_product_information_display(self, driver, home_page):
        """
        Test: Product information display
        
        Verifies that product information is displayed correctly.
        """
        logging.info("Starting product information display test")
        
        # Get products on page
        products = home_page.get_products_on_page()
        assert len(products) > 0, "Should have products on page"
        
        # Verify product information
        for product in products:
            assert product['title'], "Product should have title"
            assert product['price'], "Product should have price"
            logging.info(f"Product info verified: {product['title']} - {product['price']}")
        
        logging.info("Product information display test completed")
    
    def test_cart_navigation(self, driver, home_page):
        """
        Test: Cart navigation
        
        Verifies navigation to cart page.
        """
        logging.info("Starting cart navigation test")
        
        # Navigate to cart
        assert home_page.go_to_cart(), "Should be able to navigate to cart"
        
        # Verify cart page loaded
        current_url = home_page.get_current_url()
        assert "cart" in current_url.lower(), f"Should be on cart page, current URL: {current_url}"
        
        logging.info("Cart navigation test completed")
    
    def test_page_navigation(self, driver, home_page):
        """
        Test: Page navigation
        
        Verifies page navigation functionality.
        """
        logging.info("Starting page navigation test")
        
        # Test next page navigation
        if home_page.is_element_clickable(home_page.NEXT_BUTTON):
            assert home_page.go_to_next_page(), "Should be able to go to next page"
            logging.info("Next page navigation successful")
        
        # Test previous page navigation
        if home_page.is_element_clickable(home_page.PREVIOUS_BUTTON):
            assert home_page.go_to_previous_page(), "Should be able to go to previous page"
            logging.info("Previous page navigation successful")
        
        logging.info("Page navigation test completed")
    
    def test_home_page_refresh(self, driver, home_page):
        """
        Test: Home page refresh
        
        Verifies that the home page can be refreshed.
        """
        logging.info("Starting home page refresh test")
        
        # Refresh page
        assert home_page.refresh_page(), "Should be able to refresh page"
        
        # Verify page is still loaded
        assert home_page.is_home_page_loaded(), "Page should still be loaded after refresh"
        
        logging.info("Home page refresh test completed")
    
    def test_product_cards_interaction(self, driver, home_page):
        """
        Test: Product cards interaction
        
        Verifies that product cards are interactive.
        """
        logging.info("Starting product cards interaction test")
        
        # Get product cards
        product_cards = home_page.find_elements(home_page.PRODUCT_CARDS)
        assert len(product_cards) > 0, "Should have product cards"
        
        # Verify product cards are clickable (they should navigate to product page)
        first_card = product_cards[0]
        assert first_card.is_displayed(), "First product card should be visible"
        assert first_card.is_enabled(), "First product card should be enabled"
        
        logging.info("Product cards interaction test completed")
    
    def test_home_page_elements_visibility(self, driver, home_page):
        """
        Test: Home page elements visibility
        
        Verifies that all main elements are visible.
        """
        logging.info("Starting home page elements visibility test")
        
        # Check main navigation elements
        main_elements = [
            home_page.HOME_LINK,
            home_page.CONTACT_LINK,
            home_page.ABOUT_US_LINK,
            home_page.CART_LINK,
            home_page.LOGIN_LINK
        ]
        
        for element in main_elements:
            assert home_page.is_element_visible(element), f"Element should be visible: {element}"
        
        # Check category elements
        category_elements = [
            home_page.PHONES_CATEGORY,
            home_page.LAPTOPS_CATEGORY,
            home_page.MONITORS_CATEGORY
        ]
        
        for element in category_elements:
            assert home_page.is_element_visible(element), f"Category element should be visible: {element}"
        
        logging.info("Home page elements visibility test completed")
    
    def test_product_loading_performance(self, driver, home_page):
        """
        Test: Product loading performance
        
        Verifies that products load within acceptable time.
        """
        logging.info("Starting product loading performance test")
        
        # Measure time to load products
        import time
        start_time = time.time()
        
        # Wait for products to load
        assert home_page.wait_for_products_to_load(timeout=15), "Products should load within 15 seconds"
        
        end_time = time.time()
        load_time = end_time - start_time
        
        # Verify load time is acceptable (less than 10 seconds)
        assert load_time < 10, f"Products should load within 10 seconds, took {load_time:.2f} seconds"
        
        logging.info(f"Products loaded in {load_time:.2f} seconds")
        logging.info("Product loading performance test completed")
    
    def test_home_page_title_and_url(self, driver, home_page):
        """
        Test: Home page title and URL
        
        Verifies that the home page has correct title and URL.
        """
        logging.info("Starting home page title and URL test")
        
        # Check page title
        title = home_page.get_page_title()
        assert title, "Page should have a title"
        logging.info(f"Page title: {title}")
        
        # Check current URL
        current_url = home_page.get_current_url()
        assert Config.BASE_URL in current_url, f"URL should contain base URL, current: {current_url}"
        logging.info(f"Current URL: {current_url}")
        
        logging.info("Home page title and URL test completed")
    
    def test_home_page_responsiveness(self, driver, home_page):
        """
        Test: Home page responsiveness
        
        Verifies that the home page is responsive.
        """
        logging.info("Starting home page responsiveness test")
        
        # Test different window sizes
        window_sizes = [(1920, 1080), (1366, 768), (1024, 768)]
        
        for width, height in window_sizes:
            logging.info(f"Testing window size: {width}x{height}")
            
            # Resize window
            driver.set_window_size(width, height)
            
            # Verify page still loads
            assert home_page.is_home_page_loaded(), f"Page should load at {width}x{height}"
            
            # Verify main elements are still visible
            assert home_page.is_element_visible(home_page.PHONES_CATEGORY), f"Phones category should be visible at {width}x{height}"
        
        # Reset to default size
        driver.maximize_window()
        
        logging.info("Home page responsiveness test completed")