"""
Pytest configuration and global fixtures
"""

import pytest
import logging
import os
from selenium.webdriver import Chrome, Firefox
from utils.driver_factory import driver_factory
from config.config import Config
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def pytest_configure(config):
    """Initial pytest configuration"""
    # Create necessary directories
    os.makedirs(Config.REPORTS_DIR, exist_ok=True)
    os.makedirs(Config.SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(Config.ALLURE_RESULTS_DIR, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format=Config.LOG_FORMAT,
        handlers=[
            logging.FileHandler('reports/test_execution.log'),
            logging.StreamHandler()
        ]
    )


def pytest_addoption(parser):
    """Add command line options for pytest"""
    parser.addoption(
        "--browser",
        action="store",
        default=Config.DEFAULT_BROWSER,
        help="Browser to use for tests (chrome, firefox)"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run in headless mode"
    )
    parser.addoption(
        "--base-url",
        action="store",
        default=Config.BASE_URL,
        help="Base URL for tests"
    )


@pytest.fixture(scope="session")
def browser(request):
    """Browser fixture for session scope"""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless(request):
    """Headless mode fixture for session scope"""
    return request.config.getoption("--headless")


@pytest.fixture(scope="session")
def base_url(request):
    """Base URL fixture for session scope"""
    return request.config.getoption("--base-url")


@pytest.fixture(scope="function")
def driver(request, browser, headless):
    """WebDriver fixture for each test"""
    # Get test name for logging
    test_name = request.node.name
    
    # Create driver
    driver = driver_factory.create_driver(
        browser=browser,
        headless=headless,
        window_size=Config.WINDOW_SIZE
    )
    
    # Navigate to base URL
    driver.get(Config.BASE_URL)
    
    # Take initial screenshot
    if Config.SCREENSHOT_ON_SUCCESS:
        driver.save_screenshot(f"{Config.SCREENSHOTS_DIR}/{test_name}_start.png")
    
    yield driver
    
    # Cleanup
    try:
        # Take final screenshot
        if Config.SCREENSHOT_ON_SUCCESS:
            driver.save_screenshot(f"{Config.SCREENSHOTS_DIR}/{test_name}_end.png")
    except Exception as e:
        logging.error(f"Error taking final screenshot: {e}")
    finally:
        driver_factory.quit_driver()


@pytest.fixture(scope="function")
def login_page(driver):
    """Login page fixture"""
    return LoginPage(driver)


@pytest.fixture(scope="function")
def home_page(driver):
    """Home page fixture"""
    return HomePage(driver)


@pytest.fixture(scope="function")
def cart_page(driver):
    """Cart page fixture"""
    return CartPage(driver)


@pytest.fixture(scope="function")
def checkout_page(driver):
    """Checkout page fixture"""
    return CheckoutPage(driver)


@pytest.fixture(autouse=True)
def configure_logging(request):
    """Configure logging for each test"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Create handler for test-specific log file
    test_name = request.node.name
    test_log_file = f"reports/test_{test_name}.log"
    file_handler = logging.FileHandler(test_log_file)
    file_handler.setLevel(logging.DEBUG)
    
    # Format for file
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    logger.addHandler(file_handler)
    
    yield
    
    # Clean up handler after test
    logger.removeHandler(file_handler)


@pytest.fixture(autouse=True)
def test_setup(request, driver):
    """Setup for each test"""
    test_name = request.node.name
    logging.info(f"Starting test: {test_name}")
    
    yield
    
    logging.info(f"Finishing test: {test_name}")


@pytest.fixture(scope="function")
def logged_in_user(login_page):
    """Fixture for logged in user"""
    # Perform login
    if login_page.login():
        yield login_page
        # Logout after test
        login_page.logout()
    else:
        pytest.fail("Failed to login user")


@pytest.fixture(scope="function")
def cart_with_products(home_page, cart_page):
    """Fixture for cart with products"""
    # Add products to cart
    products = Config.TEST_DATA["products"][:2]  # Add first 2 products
    
    for product in products:
        if home_page.add_product_to_cart(product):
            logging.info(f"Added {product} to cart")
        else:
            logging.warning(f"Failed to add {product} to cart")
    
    yield cart_page


@pytest.fixture(scope="function")
def checkout_data():
    """Fixture for checkout test data"""
    return Config.TEST_DATA["shipping"]


def pytest_runtest_setup(item):
    """Setup before each test runs"""
    # Add markers based on test file
    if "test_login" in item.nodeid:
        item.add_marker(pytest.mark.login)
    elif "test_cart" in item.nodeid:
        item.add_marker(pytest.mark.cart)
    elif "test_checkout" in item.nodeid:
        item.add_marker(pytest.mark.checkout)
    elif "test_products" in item.nodeid:
        item.add_marker(pytest.mark.product)


def pytest_runtest_teardown(item, nextitem):
    """Teardown after each test runs"""
    # Take screenshot on failure
    if hasattr(item, 'rep_call') and item.rep_call.failed:
        test_name = item.name
        try:
            # This would need access to driver, so we'll handle it in the driver fixture
            pass
        except Exception as e:
            logging.error(f"Error taking failure screenshot: {e}")


def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    # Add smoke marker to login tests
    for item in items:
        if "test_login" in item.nodeid and "test_successful_login" in item.nodeid:
            item.add_marker(pytest.mark.smoke)


def pytest_configure(config):
    """Configure pytest"""
    # Register custom markers
    config.addinivalue_line(
        "markers", "login: Tests related to login functionality"
    )
    config.addinivalue_line(
        "markers", "cart: Tests related to cart functionality"
    )
    config.addinivalue_line(
        "markers", "checkout: Tests related to checkout functionality"
    )
    config.addinivalue_line(
        "markers", "product: Tests related to product functionality"
    )
    config.addinivalue_line(
        "markers", "smoke: Smoke tests"
    )
    config.addinivalue_line(
        "markers", "regression: Regression tests"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take a long time to execute"
    )