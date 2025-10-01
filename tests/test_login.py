"""
Test cases for Login functionality
"""

import pytest
import logging
from config.config import Config


class TestLogin:
    """Test class for login functionality"""
    
    def test_successful_login(self, driver, login_page):
        """
        Test: Successful login with valid credentials
        
        Verifies that a user can log in successfully with correct credentials.
        """
        logging.info("Starting successful login test")
        
        # Perform login
        assert login_page.login(), "Login should be successful"
        
        # Verify user is logged in
        assert login_page.is_logged_in(), "User should be logged in"
        
        # Verify welcome message
        welcome_message = login_page.get_welcome_message()
        assert Config.TEST_USER["username"] in welcome_message, \
            f"Welcome message should contain username: {Config.TEST_USER['username']}"
        
        logging.info("Successful login test completed")
    
    def test_login_with_invalid_credentials(self, driver, login_page):
        """
        Test: Login with invalid credentials
        
        Verifies that the system handles login attempts with incorrect credentials appropriately.
        """
        logging.info("Starting invalid credentials login test")
        
        # Attempt login with invalid credentials
        error_message = login_page.login_with_invalid_credentials("invalid_user", "invalid_pass")
        
        # Verify an error message was received
        assert error_message, "An error message should be received"
        assert "Wrong password" in error_message, f"Unexpected error message: {error_message}"
        
        # Verify user is not logged in
        assert not login_page.is_logged_in(), "User should not be logged in"
        
        logging.info("Invalid credentials login test completed")
    
    def test_login_modal_functionality(self, driver, login_page):
        """
        Test: Login modal functionality
        
        Verifies that the login modal opens correctly and contains all necessary elements.
        """
        logging.info("Starting login modal functionality test")
        
        # Open login modal
        assert login_page.open_login_modal(), "The login modal should open"
        
        # Verify fields are present
        assert login_page.is_element_present(login_page.USERNAME_INPUT), "Username field should be present"
        assert login_page.is_element_present(login_page.PASSWORD_INPUT), "Password field should be present"
        assert login_page.is_element_present(login_page.LOGIN_BUTTON), "Login button should be present"
        
        # Verify fields are visible
        assert login_page.is_element_visible(login_page.USERNAME_INPUT), "Username field should be visible"
        assert login_page.is_element_visible(login_page.PASSWORD_INPUT), "Password field should be visible"
        assert login_page.is_element_visible(login_page.LOGIN_BUTTON), "Login button should be visible"
        
        logging.info("Login modal functionality test completed")
    
    def test_logout_functionality(self, driver, login_page):
        """
        Test: Logout functionality
        
        Verifies that a logged-in user can log out correctly.
        """
        logging.info("Starting logout functionality test")
        
        # Perform login first
        assert login_page.login(), "Login should be successful"
        assert login_page.is_logged_in(), "User should be logged in"
        
        # Perform logout
        assert login_page.logout(), "Logout should be successful"
        
        # Verify user is no longer logged in
        assert not login_page.is_logged_in(), "User should not be logged in after logout"
        
        logging.info("Logout functionality test completed")
    
    def test_login_with_empty_credentials(self, driver, login_page):
        """
        Test: Login with empty credentials
        
        Verifies that the system handles login attempts with empty credentials.
        """
        logging.info("Starting empty credentials login test")
        
        # Attempt login with empty credentials
        error_message = login_page.login_with_invalid_credentials("", "")
        
        # Verify an error message was received
        assert error_message, "An error message should be received"
        assert "Please fill out Username and Password" in error_message, \
            f"Unexpected error message: {error_message}"
        
        # Verify user is not logged in
        assert not login_page.is_logged_in(), "User should not be logged in"
        
        logging.info("Empty credentials login test completed")
    
    def test_login_with_special_characters(self, driver, login_page):
        """
        Test: Login with special characters
        
        Verifies that the system handles credentials with special characters appropriately.
        """
        logging.info("Starting special characters login test")
        
        # Attempt login with special characters
        error_message = login_page.login_with_invalid_credentials("test@#$", "test!@#")
        
        # Verify it's handled appropriately
        assert error_message, "An error message should be received"
        
        # Verify user is not logged in
        assert not login_page.is_logged_in(), "User should not be logged in"
        
        logging.info("Special characters login test completed")
    
    @pytest.mark.parametrize("username,password,expected_result", [
        (Config.TEST_USER["username"], Config.TEST_USER["password"], True),
        ("invalid", Config.TEST_USER["password"], False),
        (Config.TEST_USER["username"], "invalid", False),
        ("", Config.TEST_USER["password"], False),
        (Config.TEST_USER["username"], "", False),
        ("", "", False)
    ])
    def test_login_parameterized(self, driver, login_page, username, password, expected_result):
        """
        Parameterized Test: Different credential combinations
        
        Verifies multiple credential combinations to ensure correct system behavior.
        """
        logging.info(f"Starting parameterized test: {username}/{password} -> {expected_result}")
        
        # Open login modal
        assert login_page.open_login_modal(), "The login modal should open"
        
        # Enter credentials
        assert login_page.enter_username(username), f"Should be able to enter username: {username}"
        assert login_page.enter_password(password), f"Should be able to enter password: {password}"
        
        # Attempt login
        assert login_page.click_login_button(), "Should be able to click login"
        
        if expected_result:
            # Expected successful login
            assert login_page.wait_for_login_success(), f"Login should be successful for {username}/{password}"
            assert login_page.is_logged_in(), f"User should be logged in: {username}"
            
            # Logout to clean up state
            login_page.logout()
        else:
            # Expected failed login
            error_message = login_page.handle_login_alert()
            assert error_message, f"An error message should be received for {username}/{password}"
            assert not login_page.is_logged_in(), f"User should not be logged in: {username}"
        
        logging.info(f"Parameterized test completed: {username}/{password} -> {expected_result}")
    
    def test_login_session_persistence(self, driver, login_page):
        """
        Test: Login session persistence
        
        Verifies that the login session is maintained during site navigation.
        """
        logging.info("Starting login session persistence test")
        
        # Perform login
        assert login_page.login(), "Login should be successful"
        assert login_page.is_logged_in(), "User should be logged in"
        
        # Navigate to another page and back (e.g., Home page)
        driver.get(Config.BASE_URL)
        driver.refresh()
        
        # Verify session persistence
        assert login_page.is_logged_in(), "User should remain logged in after navigation"
        welcome_message = login_page.get_welcome_message()
        assert Config.TEST_USER["username"] in welcome_message, \
            f"Welcome message should still contain username: {Config.TEST_USER['username']}"
        
        # Logout to clean up
        login_page.logout()
        assert not login_page.is_logged_in(), "User should be logged out after explicit logout"
        
        logging.info("Login session persistence test completed")