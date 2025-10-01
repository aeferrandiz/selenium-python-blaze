# QA Automation Framework for DemoBlaze

A comprehensive test automation framework for the DemoBlaze e-commerce site using Python, Selenium, and the Page Object Model (POM) pattern.

## 🚀 Key Features

- **Page Object Model (POM)** for better maintainability
- **Multi-browser support** (Chrome and Firefox)
- **Headless execution** for CI/CD
- **Advanced reporting** with pytest-html and Allure
- **CI/CD integration** with GitHub Actions
- **Robust wait handling** and exception management
- **Centralized test data**
- **Detailed logging** for debugging
- **Automatic screenshots** on failures
- **Parallel test execution**
- **Docker support** for containerized testing

## 📋 System Requirements

- Python 3.12 or higher
- Chrome or Firefox installed
- Git for version control
- 4GB RAM minimum (8GB recommended)
- Docker (optional, for containerized execution)

## 🛠️ Quick Start

### Installation

#### Option 1: Quick Installation
```bash
# Clone repository
git clone <repository-url>
cd qa-automation-framework

# Run installation script
./install.sh
```

#### Option 2: Manual Installation
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p reports/screenshots reports/allure-results
```

#### Option 3: Docker Installation
```bash
# Build Docker image
docker build -t qa-automation .

# Run tests in container
docker run qa-automation test
```

### Run Tests

#### Using Makefile (Recommended)
```bash
# See all available commands
make help

# Run all tests
make test

# Run with specific browser
make test-chrome
make test-firefox

# Run in visible mode
make test-visible

# Run specific test suite
make test-login
make test-products
make test-cart
make test-checkout

# Development commands
make lint          # Code linting
make format        # Code formatting
make type-check    # Type checking
make clean         # Clean temporary files
```

#### Using Python Scripts
```bash
# Activate environment
source venv/bin/activate

# Run all tests
python scripts/run_tests.py

# Run with specific browser
python scripts/run_tests.py --browser=firefox

# Run in visible mode
python scripts/run_tests.py --no-headless

# Run specific test suite
python scripts/run_tests.py --test-suite=login

# Setup environment
python scripts/setup_environment.py
```

#### Using pytest directly
```bash
# Activate environment
source venv/bin/activate

# Run all tests
pytest tests/ --browser=chrome --headless

# Run specific test
pytest tests/test_login.py::TestLogin::test_successful_login -v

# Run in parallel
pytest tests/ -n auto

# Run with reports
pytest tests/ --html=reports/report.html --self-contained-html
```

#### Using Docker Compose
```bash
# Run all tests
docker-compose up qa-automation

# Run with Chrome
docker-compose up qa-chrome

# Run with Firefox
docker-compose up qa-firefox

# Run smoke tests
docker-compose up qa-smoke

# Generate reports
docker-compose up qa-report

# Serve reports
docker-compose up qa-serve
```

## 🏗️ Project Structure

```
qa-automation-framework/
├── config/                 # Configuration files
│   ├── __init__.py
│   └── config.py          # Main configuration
├── pages/                  # Page Object classes
│   ├── __init__.py
│   ├── base_page.py       # Base page class
│   ├── login_page.py      # Login functionality
│   ├── home_page.py       # Home page
│   ├── product_page.py    # Product pages
│   ├── cart_page.py       # Shopping cart
│   └── checkout_page.py   # Checkout process
├── tests/                  # Test cases
│   ├── __init__.py
│   ├── conftest.py        # Pytest configuration
│   ├── test_login.py      # Login tests
│   ├── test_products.py   # Product tests
│   ├── test_cart.py       # Cart tests
│   └── test_checkout.py   # Checkout tests
├── utils/                  # Utility functions
│   ├── __init__.py
│   ├── driver_factory.py  # WebDriver factory
│   └── test_data.py       # Test data management
├── scripts/                # Helper scripts
│   ├── run_tests.py       # Test runner
│   └── setup_environment.py # Environment setup
├── reports/                # Test reports and screenshots
│   ├── screenshots/       # Screenshots on failures
│   └── allure-results/    # Allure test results
├── requirements.txt        # Python dependencies
├── pytest.ini            # Pytest configuration
├── Makefile              # Build commands
├── install.sh            # Installation script
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose services
├── .dockerignore         # Docker ignore file
└── README.md             # This file
```

## 🧪 Test Execution

### Writing Tests

#### Basic Test Structure
```python
def test_successful_login(self, driver, login_page):
    """Test: Successful login with valid credentials"""
    # Arrange
    username = "test"
    password = "test"
    
    # Act
    assert login_page.login(username, password)
    
    # Assert
    assert login_page.is_logged_in()
```

#### Using Fixtures
```python
def test_cart_functionality(self, driver, cart_page, cart_with_products):
    """Test that requires products in cart"""
    # The cart_with_products fixture prepares the cart
    assert cart_page.get_cart_count() > 0
```

#### Test Data Management
```python
from utils.test_data import TestData

# Get user data
user = TestData.get_user("valid_user")

# Get products
products = TestData.get_products("phones", count=3)

# Get checkout data
checkout_data = TestData.get_checkout_data("valid")
```

## 📊 Reporting

### HTML Reports
Reports are automatically generated in `reports/pytest_report.html`

```bash
# Generate HTML report
pytest tests/ --html=reports/report.html --self-contained-html

# View report
open reports/report.html
```

### Allure Reports
```bash
# Generate Allure report
allure generate reports/allure-results --clean -o reports/allure-report

# Serve report locally
allure serve reports/allure-results

# Using Docker
docker-compose up qa-report
```

## 🔧 Configuration

### Environment Variables
```bash
export BROWSER=chrome
export HEADLESS=true
export BASE_URL=https://www.demoblaze.com
export TEST_SUITE=all
```

### Configuration File
Edit `config/config.py` for custom settings:

```python
# URLs
BASE_URL = "https://www.demoblaze.com"

# Credentials
TEST_USER = {
    "username": "test",
    "password": "test"
}

# Timeouts
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 20
```

## 🧩 Page Objects

### BasePage
Common methods for all pages:
- `find_element()` - Find elements with wait
- `click_element()` - Click with error handling
- `send_keys()` - Send text to elements
- `wait_for_element_visible()` - Wait for visibility
- `take_screenshot()` - Capture screenshots
- `scroll_to_element()` - Scroll to element
- `get_element_text()` - Get element text safely

### Specific Pages
- **LoginPage** - Login modal functionality
- **HomePage** - Main page navigation and product browsing
- **ProductPage** - Product details and actions
- **CartPage** - Shopping cart management
- **CheckoutPage** - Checkout process and form handling

## 🐛 Debugging

### Debug Mode
```bash
# Run test in visible mode
python scripts/run_tests.py --no-headless

# Run specific test with debug
pytest tests/test_login.py::TestLogin::test_successful_login -v -s --tb=long

# Using Makefile
make debug-test TEST=test_login.py::TestLogin::test_successful_login
```

### Logs
Logs are automatically generated:
- `reports/pytest.log` - General execution log
- `reports/test_*.log` - Individual test logs
- Console output with detailed information

### Screenshots
Screenshots are taken automatically:
- At the start of each test
- At the end of each test
- On test failures
- Stored in `reports/screenshots/`

### Common Issues
1. **Driver not found** - Drivers install automatically via webdriver-manager
2. **Intermittent failures** - Increase timeouts in config
3. **Elements not found** - Check selectors in Page Objects
4. **Timeout errors** - Adjust wait times in configuration

## 🚀 CI/CD

### GitHub Actions
The project includes GitHub Actions workflow for:
- Multi-browser testing (Chrome and Firefox)
- Automatic report generation
- GitHub Pages deployment
- Notification system
- Parallel test execution

### Docker Integration
```bash
# Build image
docker build -t qa-automation .

# Run tests
docker run qa-automation test

# Run with specific browser
docker run qa-automation test-chrome

# Interactive shell
docker run -it qa-automation shell
```

## 🔍 Best Practices

### Writing Tests
1. Use descriptive test names that explain what is being tested
2. One test, one functionality
3. Use appropriate fixtures for setup and teardown
4. Handle test data properly with centralized data management
5. Follow AAA pattern (Arrange, Act, Assert)

### Maintaining Page Objects
1. One Page Object per page or major component
2. Methods should represent user actions, not technical operations
3. Locators as constants at the top of the class
4. Robust error handling and meaningful error messages
5. Use explicit waits instead of implicit waits

### Code Quality
1. Follow PEP 8 style guidelines
2. Use type hints for better code documentation
3. Document functions and classes with docstrings
4. Write clean, readable, and maintainable code
5. Regular code reviews and refactoring

## 📚 Resources

- [Selenium Python Documentation](https://selenium-python.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [Allure Framework](https://docs.qameta.io/allure/)
- [Page Object Model](https://martinfowler.com/bliki/PageObject.html)
- [Docker Documentation](https://docs.docker.com/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure everything works (`make test`)
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
