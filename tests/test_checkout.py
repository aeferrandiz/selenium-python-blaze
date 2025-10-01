"""
Test cases for Checkout functionality
"""

import pytest
import logging
from selenium.webdriver.common.by import By
from config.config import Config


class TestCheckout:
    """Test class for checkout functionality"""
    
    def test_checkout_modal_loading(self, driver, checkout_page, cart_with_products):
        """
        Test: Checkout modal loading
        
        Verifies that checkout modal opens correctly when proceeding from cart.
        """
        logging.info("Starting checkout modal loading test")
        
        # Navigate to cart
        driver.get(f"{Config.BASE_URL}/cart.html")
        
        # Proceed to checkout
        assert checkout_page.proceed_to_checkout(), "Should be able to proceed to checkout"
        
        # Verify modal is visible
        assert checkout_page.is_checkout_modal_visible(), "Checkout modal should be visible"
        
        # Verify form elements
        form_elements = [
            checkout_page.NAME_INPUT,
            checkout_page.COUNTRY_INPUT,
            checkout_page.CITY_INPUT,
            checkout_page.CREDIT_CARD_INPUT,
            checkout_page.MONTH_INPUT,
            checkout_page.YEAR_INPUT,
            checkout_page.PURCHASE_BUTTON
        ]
        
        for element in form_elements:
            assert checkout_page.is_element_present(element), f"Form element should be present: {element}"
        
        logging.info("Checkout modal loading test completed")
    
    def test_checkout_form_validation(self, driver, checkout_page, cart_with_products):
        """
        Test: Checkout form validation
        
        Verifies that checkout form validates required fields correctly.
        """
        logging.info("Starting checkout form validation test")
        
        # Navigate to cart and proceed to checkout
        driver.get(f"{Config.BASE_URL}/cart.html")
        assert checkout_page.proceed_to_checkout(), "Should proceed to checkout"
        
        # Try to submit empty form
        assert checkout_page.click_purchase(), "Should be able to click purchase button"
        
        # Verify form validation is working
        assert checkout_page.verify_form_validation(), "Form validation should work"
        
        logging.info("Checkout form validation test completed")
    
    def test_checkout_form_filling(self, driver, checkout_page, cart_with_products):
        """
        Test: Checkout form filling
        
        Verifies that checkout form can be filled correctly.
        """
        logging.info("Starting checkout form filling test")
        
        # Navigate to cart and proceed to checkout
        driver.get(f"{Config.BASE_URL}/cart.html")
        assert checkout_page.proceed_to_checkout(), "Should proceed to checkout"
        
        # Fill form with test data
        form_data = Config.TEST_DATA["shipping"]
        assert checkout_page.fill_checkout_form(form_data), "Should fill checkout form"
        
        # Verify form is complete
        assert checkout_page.is_form_complete(), "Form should be complete"
        
        logging.info("Checkout form filling test completed")
    
    def test_checkout_complete_purchase(self, driver, checkout_page, cart_with_products):
        """
        Test: Complete purchase process
        
        Verifies that complete purchase process works correctly.
        """
        logging.info("Starting complete purchase test")
        
        # Navigate to cart and proceed to checkout
        driver.get(f"{Config.BASE_URL}/cart.html")
        assert checkout_page.proceed_to_checkout(), "Should proceed to checkout"
        
        # Complete purchase
        assert checkout_page.complete_purchase(), "Should complete purchase"
        
        # Verify confirmation modal appears
        assert checkout_page.wait_for_confirmation_modal(), "Confirmation modal should appear"
        
        # Verify confirmation details
        confirmation_title = checkout_page.get_confirmation_title()
        assert confirmation_title, "Should have confirmation title"
        
        confirmation_message = checkout_page.get_confirmation_message()
        assert confirmation_message, "Should have confirmation message"
        
        logging.info("Complete purchase test completed")
    
    def test_checkout_order_details(self, driver, checkout_page, cart_with_products):
        """
        Test: Order details display
        
        Verifies that order details are displayed correctly.
        """
        logging.info("Starting order details test")
        
        # Navigate to cart and proceed to checkout
        driver.get(f"{Config.BASE_URL}/cart.html")
        assert checkout_page.proceed_to_checkout(), "Should proceed to checkout"
        
        # Complete purchase
        assert checkout_page.complete_purchase(), "Should complete purchase"
        
        # Wait for confirmation
        assert checkout_page.wait_for_confirmation_modal(), "Confirmation modal should appear"
        
        # Get order details
        order_details = checkout_page.get_order_details()
        
        # Verify order details
        assert order_details.get('id'), "Should have order ID"
        assert order_details.get('amount'), "Should have order amount"
        assert order_details.get('name'), "Should have order name"
        assert order_details.get('card'), "Should have order card"
        assert order_details.get('date'), "Should have order date"
        
        logging.info(f"Order details: {order_details}")
        logging.info("Order details test completed")
    
    def test_checkout_form_individual_fields(self, driver, checkout_page, cart_with_products):
        """
        Test: Individual form fields
        
        Verifies that individual form fields work correctly.
        """
        logging.info("Starting individual form fields test")
        
        # Navigate to cart and proceed to checkout
        driver.get(f"{Config.BASE_URL}/cart.html")
        assert checkout_page.proceed_to_checkout(), "Should proceed to checkout"
        
        # Test each field individually
        test_data = Config.TEST_DATA["shipping"]
        
        # Test name field
        assert checkout_page.fill_name(test_data['name']), "Should fill name field"
        
        # Test country field
        assert checkout_page.fill_country(test_data['country']), "Should fill country field"
        
        # Test city field
        assert checkout_page.fill_city(test_data['city']), "Should fill city field"
        
        # Test credit card field
        assert checkout_page.fill_credit_card(test_data['credit_card']), "Should fill credit card field"
        
        # Test month field
        assert checkout_page.fill_month(test_data['month']), "Should fill month field"
        
        # Test year field
        assert checkout_page.fill_year(test_data['year']), "Should fill year field"
        
        logging.info("Individual form fields test completed")
    
    def test_checkout_modal_close(self, driver, checkout_page, cart_with_products):
        """
        Test: Checkout modal close
        
        Verifies that checkout modal can be closed after completing purchase.
        """
        logging.info("Starting checkout modal close test")
        
        # Navigate to cart and proceed to checkout
        driver.get(f"{Config.BASE_URL}/cart.html")
        assert checkout_page.proceed_to_checkout(), "Should proceed to checkout"
        
        # Verify modal is visible
        assert checkout_page.is_checkout_modal_visible(), "Modal should be visible"
        
        # Complete purchase to get to the confirmation modal
        assert checkout_page.complete_purchase(), "Should complete purchase"
        
        # Wait for confirmation modal and click OK
        assert checkout_page.wait_for_confirmation_modal(), "Confirmation modal should appear"
        assert checkout_page.click_confirmation_ok(), "Should click OK on confirmation"
        
        # Now close the checkout modal
        assert checkout_page.close_checkout_modal(), "Should close modal"
        
        # Verify modal is closed
        assert not checkout_page.is_checkout_modal_visible(), "Modal should be closed"
        
        logging.info("Checkout modal close test completed")
    
    def test_checkout_error_handling(self, driver, checkout_page, cart_with_products):
        """
        Test: Checkout error handling
        
        Verifies that checkout handles errors correctly.
        """
        logging.info("Starting checkout error handling test")
        
        # Navigate to cart and proceed to checkout
        driver.get(f"{Config.BASE_URL}/cart.html")
        assert checkout_page.proceed_to_checkout(), "Should proceed to checkout"
        
        # Try to submit empty form
        assert checkout_page.click_purchase(), "Should click purchase button"
        
        # Handle any errors
        error_message = checkout_page.handle_checkout_error()
        if error_message:
            logging.info(f"Error handled: {error_message}")
        
        logging.info("Checkout error handling test completed")
    
    def test_checkout_form_clear(self, driver, checkout_page, cart_with_products):
        """
        Test: Checkout form clear
        
        Verifies that checkout form can be cleared.
        """
        logging.info("Starting checkout form clear test")
        
        # Navigate to cart and proceed to checkout
        driver.get(f"{Config.BASE_URL}/cart.html")
        assert checkout_page.proceed_to_checkout(), "Should proceed to checkout"
        
        # Fill form
        form_data = Config.TEST_DATA["shipping"]
        assert checkout_page.fill_checkout_form(form_data), "Should fill form"
        
        # Verify form is filled
        assert checkout_page.is_form_complete(), "Form should be complete"
        
        # Clear form
        assert checkout_page.clear_form(), "Should clear form"
        
        # Verify form is empty
        assert not checkout_page.is_form_complete(), "Form should be empty after clearing"
        
        logging.info("Checkout form clear test completed")
    
    def test_checkout_confirmation_ok(self, driver, checkout_page, cart_with_products):
        """
        Test: Checkout confirmation OK
        
        Verifies that confirmation OK button works.
        """
        logging.info("Starting checkout confirmation OK test")
        
        # Navigate to cart and proceed to checkout
        driver.get(f"{Config.BASE_URL}/cart.html")
        assert checkout_page.proceed_to_checkout(), "Should proceed to checkout"
        
        # Complete purchase
        assert checkout_page.complete_purchase(), "Should complete purchase"
        
        # Wait for confirmation
        assert checkout_page.wait_for_confirmation_modal(), "Confirmation modal should appear"
        
        # Click OK
        assert checkout_page.click_confirmation_ok(), "Should click confirmation OK"
        
        logging.info("Checkout confirmation OK test completed")
    
    def test_checkout_with_different_data(self, driver, checkout_page, cart_with_products):
        """
        Test: Checkout with different data
        
        Verifies that checkout works with different form data.
        """
        logging.info("Starting checkout with different data test")
        
        # Navigate to cart and proceed to checkout
        driver.get(f"{Config.BASE_URL}/cart.html")
        assert checkout_page.proceed_to_checkout(), "Should proceed to checkout"
        
        # Test with different data
        different_data = {
            'name': 'Jane Smith',
            'country': 'Canada',
            'city': 'Toronto',
            'credit_card': '5555555555554444',
            'month': '06',
            'year': '2026'
        }
        
        # Fill form with different data
        assert checkout_page.fill_checkout_form(different_data), "Should fill form with different data"
        
        # Complete purchase
        assert checkout_page.complete_purchase(), "Should complete purchase with different data"
        
        # Verify confirmation
        assert checkout_page.wait_for_confirmation_modal(), "Confirmation should appear"
        
        logging.info("Checkout with different data test completed")
    
    def test_checkout_form_required_fields(self, driver, checkout_page, cart_with_products):
        """
        Test: Checkout form required fields
        
        Verifies that all required fields are present and functional.
        """
        logging.info("Starting checkout form required fields test")
        
        # Navigate to cart and proceed to checkout
        driver.get(f"{Config.BASE_URL}/cart.html")
        assert checkout_page.proceed_to_checkout(), "Should proceed to checkout"
        
        # Verify all required fields are present
        required_fields = [
            checkout_page.NAME_INPUT,
            checkout_page.COUNTRY_INPUT,
            checkout_page.CITY_INPUT,
            checkout_page.CREDIT_CARD_INPUT,
            checkout_page.MONTH_INPUT,
            checkout_page.YEAR_INPUT
        ]
        
        for field in required_fields:
            assert checkout_page.is_element_present(field), f"Required field should be present: {field}"
            assert checkout_page.is_element_visible(field), f"Required field should be visible: {field}"
        
        logging.info("Checkout form required fields test completed")
    
    def test_checkout_modal_elements_visibility(self, driver, checkout_page, cart_with_products):
        """
        Test: Checkout modal elements visibility
        
        Verifies that all modal elements are visible.
        """
        logging.info("Starting checkout modal elements visibility test")
        
        # Navigate to cart and proceed to checkout
        driver.get(f"{Config.BASE_URL}/cart.html")
        assert checkout_page.proceed_to_checkout(), "Should proceed to checkout"
        
        # Verify modal elements are visible
        modal_elements = [
            checkout_page.MODAL_TITLE,
            checkout_page.NAME_INPUT,
            checkout_page.COUNTRY_INPUT,
            checkout_page.CITY_INPUT,
            checkout_page.CREDIT_CARD_INPUT,
            checkout_page.MONTH_INPUT,
            checkout_page.YEAR_INPUT,
            checkout_page.PURCHASE_BUTTON
        ]
        
        for element in modal_elements:
            assert checkout_page.is_element_visible(element), f"Modal element should be visible: {element}"
        
        # Check if close button is present (may not be visible immediately)
        close_button_present = checkout_page.is_element_present(checkout_page.CLOSE_BUTTON)
        logging.info(f"Close button present: {close_button_present}")
        
        # Also check for X button as alternative
        x_button_present = checkout_page.is_element_present((By.XPATH, "//div[@id='orderModal']//button[@class='close']"))
        logging.info(f"X button present: {x_button_present}")
        
        # At least one close mechanism should be present
        assert close_button_present or x_button_present, "At least one close button should be present"
        
        logging.info("Checkout modal elements visibility test completed")
    
    def test_checkout_purchase_button_functionality(self, driver, checkout_page, cart_with_products):
        """
        Test: Purchase button functionality
        
        Verifies that purchase button works correctly.
        """
        logging.info("Starting purchase button functionality test")
        
        # Navigate to cart and proceed to checkout
        driver.get(f"{Config.BASE_URL}/cart.html")
        assert checkout_page.proceed_to_checkout(), "Should proceed to checkout"
        
        # Fill form
        form_data = Config.TEST_DATA["shipping"]
        assert checkout_page.fill_checkout_form(form_data), "Should fill form"
        
        # Verify purchase button is clickable
        assert checkout_page.is_element_clickable(checkout_page.PURCHASE_BUTTON), "Purchase button should be clickable"
        
        # Click purchase button
        assert checkout_page.click_purchase(), "Should click purchase button"
        
        logging.info("Purchase button functionality test completed")
    
    def test_checkout_complete_flow(self, driver, checkout_page, cart_with_products):
        """
        Test: Complete checkout flow
        
        Verifies the complete checkout flow from start to finish.
        """
        logging.info("Starting complete checkout flow test")
        
        # Navigate to cart and proceed to checkout
        driver.get(f"{Config.BASE_URL}/cart.html")
        assert checkout_page.proceed_to_checkout(), "Should proceed to checkout"
        
        # Verify modal is visible
        assert checkout_page.is_checkout_modal_visible(), "Modal should be visible"
        
        # Fill form
        form_data = Config.TEST_DATA["shipping"]
        assert checkout_page.fill_checkout_form(form_data), "Should fill form"
        
        # Complete purchase
        assert checkout_page.complete_purchase(), "Should complete purchase"
        
        # Wait for confirmation
        assert checkout_page.wait_for_confirmation_modal(), "Confirmation should appear"
        
        # Get order details
        order_details = checkout_page.get_order_details()
        assert order_details, "Should have order details"
        
        # Click OK to complete
        assert checkout_page.click_confirmation_ok(), "Should click OK"
        
        logging.info("Complete checkout flow test completed")
