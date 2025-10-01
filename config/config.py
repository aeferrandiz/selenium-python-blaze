"""
Central configuration for the automation framework
"""

import os
from typing import Dict, Any


class Config:
    """Central framework configuration"""
    
    # URLs
    BASE_URL = "https://www.demoblaze.com"
    LOGIN_URL = f"{BASE_URL}/#"
    
    # Test credentials
    TEST_USER = {
        "username": "test",
        "password": "test"
    }
    
    # Timeouts (in seconds)
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    PAGE_LOAD_TIMEOUT = 30
    SCRIPT_TIMEOUT = 30
    
    # Browser configuration
    BROWSERS = ["chrome", "firefox"]
    DEFAULT_BROWSER = "chrome"
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    
    # Window configuration
    WINDOW_SIZE = (1920, 1080)
    
    # Test data for checkout
    TEST_DATA = {
        "shipping": {
            "name": "John Doe",
            "country": "United States",
            "city": "New York",
            "credit_card": "4111111111111111",
            "month": "12",
            "year": "2025"
        },
        "products": [
            "Samsung galaxy s6",
            "Nokia lumia 1520",
            "Nexus 6"
        ]
    }
    
    # Report configuration
    REPORTS_DIR = "reports"
    SCREENSHOTS_DIR = f"{REPORTS_DIR}/screenshots"
    ALLURE_RESULTS_DIR = f"{REPORTS_DIR}/allure-results"
    ALLURE_REPORT_DIR = f"{REPORTS_DIR}/allure-report"
    
    # Logging configuration
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    # Screenshot configuration
    SCREENSHOT_ON_FAILURE = True
    SCREENSHOT_ON_SUCCESS = False
    
    # Retry configuration
    MAX_RETRIES = 3
    RETRY_DELAY = 1
    
    # Parallel execution
    MAX_WORKERS = 4
    
    @classmethod
    def get_browser_config(cls, browser: str) -> Dict[str, Any]:
        """Get browser-specific configuration"""
        configs = {
            "chrome": {
                "browser_name": "chrome",
                "headless": cls.HEADLESS,
                "window_size": cls.WINDOW_SIZE,
                "options": [
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-extensions",
                    "--disable-logging",
                    "--disable-web-security",
                    "--allow-running-insecure-content"
                ]
            },
            "firefox": {
                "browser_name": "firefox",
                "headless": cls.HEADLESS,
                "window_size": cls.WINDOW_SIZE,
                "options": [
                    "--no-sandbox",
                    "--disable-dev-shm-usage"
                ]
            }
        }
        return configs.get(browser, configs["chrome"])
    
    @classmethod
    def get_test_data(cls, data_type: str) -> Dict[str, Any]:
        """Get test data by type"""
        return cls.TEST_DATA.get(data_type, {})
    
    @classmethod
    def get_timeout_config(cls) -> Dict[str, int]:
        """Get timeout configuration"""
        return {
            "implicit_wait": cls.IMPLICIT_WAIT,
            "explicit_wait": cls.EXPLICIT_WAIT,
            "page_load_timeout": cls.PAGE_LOAD_TIMEOUT,
            "script_timeout": cls.SCRIPT_TIMEOUT
        }
    
    @classmethod
    def get_report_config(cls) -> Dict[str, str]:
        """Get report configuration"""
        return {
            "reports_dir": cls.REPORTS_DIR,
            "screenshots_dir": cls.SCREENSHOTS_DIR,
            "allure_results_dir": cls.ALLURE_RESULTS_DIR,
            "allure_report_dir": cls.ALLURE_REPORT_DIR
        }