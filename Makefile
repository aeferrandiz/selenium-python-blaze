# Makefile for QA Automation Framework

.PHONY: help install test test-chrome test-firefox test-headless test-parallel clean setup lint format

# Variables
PYTHON := python
PIP := pip
BROWSER := chrome
HEADLESS := true

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show help
	@echo "$(GREEN)QA Automation Framework for DemoBlaze$(NC)"
	@echo ""
	@echo "$(YELLOW)Available commands:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	@echo "$(YELLOW)Installing dependencies...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

quick-install: ## Quick installation with script
	@echo "$(YELLOW)Running quick installation...$(NC)"
	./install.sh
	@echo "$(GREEN)✅ Quick installation completed$(NC)"

setup: ## Setup complete environment
	@echo "$(YELLOW)Setting up environment...$(NC)"
	$(PYTHON) scripts/setup_environment.py
	@echo "$(GREEN)✅ Environment configured$(NC)"

test: ## Run all tests
	@echo "$(YELLOW)Running tests...$(NC)"
	$(PYTHON) scripts/run_tests.py --browser=$(BROWSER) --headless
	@echo "$(GREEN)✅ Tests completed$(NC)"

test-chrome: ## Run tests with Chrome
	@echo "$(YELLOW)Running tests with Chrome...$(NC)"
	$(PYTHON) scripts/run_tests.py --browser=chrome --headless
	@echo "$(GREEN)✅ Chrome tests completed$(NC)"

test-firefox: ## Run tests with Firefox
	@echo "$(YELLOW)Running tests with Firefox...$(NC)"
	$(PYTHON) scripts/run_tests.py --browser=firefox --headless
	@echo "$(GREEN)✅ Firefox tests completed$(NC)"

test-headless: ## Run tests in headless mode
	@echo "$(YELLOW)Running tests in headless mode...$(NC)"
	$(PYTHON) scripts/run_tests.py --browser=$(BROWSER) --headless
	@echo "$(GREEN)✅ Headless tests completed$(NC)"

test-visible: ## Run tests in visible mode
	@echo "$(YELLOW)Running tests in visible mode...$(NC)"
	$(PYTHON) scripts/run_tests.py --browser=$(BROWSER) --no-headless
	@echo "$(GREEN)✅ Visible tests completed$(NC)"

test-parallel: ## Run tests in parallel
	@echo "$(YELLOW)Running tests in parallel...$(NC)"
	$(PYTHON) scripts/run_tests.py --browser=$(BROWSER) --headless --parallel
	@echo "$(GREEN)✅ Parallel tests completed$(NC)"

test-smoke: ## Run smoke tests
	@echo "$(YELLOW)Running smoke tests...$(NC)"
	$(PYTHON) scripts/run_tests.py --test-suite=login --browser=$(BROWSER) --headless
	@echo "$(GREEN)✅ Smoke tests completed$(NC)"

test-login: ## Run login tests
	@echo "$(YELLOW)Running login tests...$(NC)"
	$(PYTHON) scripts/run_tests.py --test-suite=login --browser=$(BROWSER) --headless
	@echo "$(GREEN)✅ Login tests completed$(NC)"

test-products: ## Run product tests
	@echo "$(YELLOW)Running product tests...$(NC)"
	$(PYTHON) scripts/run_tests.py --test-suite=products --browser=$(BROWSER) --headless
	@echo "$(GREEN)✅ Product tests completed$(NC)"

test-cart: ## Run cart tests
	@echo "$(YELLOW)Running cart tests...$(NC)"
	$(PYTHON) scripts/run_tests.py --test-suite=cart --browser=$(BROWSER) --headless
	@echo "$(GREEN)✅ Cart tests completed$(NC)"

test-checkout: ## Run checkout tests
	@echo "$(YELLOW)Running checkout tests...$(NC)"
	$(PYTHON) scripts/run_tests.py --test-suite=checkout --browser=$(BROWSER) --headless
	@echo "$(GREEN)✅ Checkout tests completed$(NC)"

test-specific: ## Run specific test (use TEST=test_name)
	@echo "$(YELLOW)Running specific test: $(TEST)$(NC)"
	$(PYTHON) -m pytest tests/$(TEST) --browser=$(BROWSER) --headless -v
	@echo "$(GREEN)✅ Specific test completed$(NC)"

lint: ## Run linting
	@echo "$(YELLOW)Running linting...$(NC)"
	$(PYTHON) -m flake8 pages/ utils/ tests/ --max-line-length=120 --ignore=E501,W503
	@echo "$(GREEN)✅ Linting completed$(NC)"

format: ## Format code
	@echo "$(YELLOW)Formatting code...$(NC)"
	$(PYTHON) -m black pages/ utils/ tests/ --line-length=120
	$(PYTHON) -m isort pages/ utils/ tests/ --profile=black
	@echo "$(GREEN)✅ Code formatted$(NC)"

type-check: ## Check types
	@echo "$(YELLOW)Checking types...$(NC)"
	$(PYTHON) -m mypy pages/ utils/ --ignore-missing-imports
	@echo "$(GREEN)✅ Type checking completed$(NC)"

coverage: ## Run tests with coverage
	@echo "$(YELLOW)Running tests with coverage...$(NC)"
	$(PYTHON) -m pytest tests/ --browser=$(BROWSER) --headless=true --cov=pages --cov=utils --cov-report=html --cov-report=term
	@echo "$(GREEN)✅ Coverage generated$(NC)"

report: ## Generate Allure report
	@echo "$(YELLOW)Generating Allure report...$(NC)"
	allure generate reports/allure-results --clean -o reports/allure-report
	@echo "$(GREEN)✅ Allure report generated$(NC)"

serve-report: ## Serve Allure report locally
	@echo "$(YELLOW)Serving Allure report...$(NC)"
	allure serve reports/allure-results

clean: ## Clean temporary files
	@echo "$(YELLOW)Cleaning temporary files...$(NC)"
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf reports/screenshots/*
	rm -rf reports/allure-results/*
	rm -rf reports/*.html
	rm -rf reports/*.xml
	rm -rf reports/*.log
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "$(GREEN)✅ Cleanup completed$(NC)"

clean-reports: ## Clean only reports
	@echo "$(YELLOW)Cleaning reports...$(NC)"
	rm -rf reports/screenshots/*
	rm -rf reports/allure-results/*
	rm -rf reports/*.html
	rm -rf reports/*.xml
	rm -rf reports/*.log
	@echo "$(GREEN)✅ Reports cleaned$(NC)"

validate: ## Validate configuration
	@echo "$(YELLOW)Validating configuration...$(NC)"
	$(PYTHON) -c "import selenium, pytest, allure; print('✅ Main dependencies OK')"
	$(PYTHON) -c "from config.config import Config; print('✅ Configuration OK')"
	$(PYTHON) -c "from pages.base_page import BasePage; print('✅ Page Objects OK')"
	@echo "$(GREEN)✅ Validation completed$(NC)"

ci: ## Run CI pipeline
	@echo "$(YELLOW)Running CI pipeline...$(NC)"
	$(MAKE) install
	$(MAKE) lint
	$(MAKE) test-chrome
	$(MAKE) test-firefox
	$(MAKE) report
	@echo "$(GREEN)✅ CI pipeline completed$(NC)"

dev: ## Setup development environment
	@echo "$(YELLOW)Setting up development environment...$(NC)"
	$(MAKE) install
	$(MAKE) setup
	$(MAKE) validate
	@echo "$(GREEN)✅ Development environment ready$(NC)"

# Debug commands
debug-test: ## Run test in debug mode
	@echo "$(YELLOW)Running test in debug mode...$(NC)"
	$(PYTHON) -m pytest tests/$(TEST) --browser=$(BROWSER) --headless=false -v -s --tb=long
	@echo "$(GREEN)✅ Debug completed$(NC)"

debug-login: ## Debug login
	@echo "$(YELLOW)Debugging login...$(NC)"
	$(MAKE) debug-test TEST=test_login.py::TestLogin::test_successful_login

debug-cart: ## Debug cart
	@echo "$(YELLOW)Debugging cart...$(NC)"
	$(MAKE) debug-test TEST=test_cart.py::TestCart::test_add_products_to_cart_and_verify

# Information commands
info: ## Show project information
	@echo "$(GREEN)QA Automation Framework for DemoBlaze$(NC)"
	@echo ""
	@echo "$(YELLOW)Project information:$(NC)"
	@echo "  Python: $(shell python --version)"
	@echo "  Pip: $(shell pip --version)"
	@echo "  Directory: $(shell pwd)"
	@echo "  Browser: $(BROWSER)"
	@echo "  Headless: $(HEADLESS)"
	@echo ""
	@echo "$(YELLOW)Structure:$(NC)"
	@echo "  📁 pages/ - Page Objects"
	@echo "  📁 tests/ - Test Cases"
	@echo "  📁 utils/ - Utilities"
	@echo "  📁 config/ - Configuration"
	@echo "  📁 reports/ - Reports"
	@echo ""
	@echo "$(YELLOW)Useful commands:$(NC)"
	@echo "  make help - Show help"
	@echo "  make setup - Setup environment"
	@echo "  make test - Run tests"
	@echo "  make report - Generate report"
	@echo "  make clean - Clean files"

status: ## Show project status
	@echo "$(YELLOW)Project status:$(NC)"
	@echo "  Tests executed: $(shell find reports -name "*.html" | wc -l)"
	@echo "  Screenshots: $(shell find reports/screenshots -name "*.png" | wc -l)"
	@echo "  Logs: $(shell find reports -name "*.log" | wc -l)"
	@echo "  Last execution: $(shell ls -la reports/ | head -2 | tail -1)"