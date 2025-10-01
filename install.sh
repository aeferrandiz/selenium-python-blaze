#!/bin/bash
# Simplified installation script for QA Automation Framework

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Installing QA Automation Framework for DemoBlaze${NC}"
echo ""

# Check Python
echo -e "${YELLOW}📋 Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.8+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "${GREEN}✅ Python ${PYTHON_VERSION} detected${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}🔄 Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Upgrade pip
echo -e "${YELLOW}⬆️ Upgrading pip...${NC}"
pip install --upgrade pip
echo -e "${GREEN}✅ Pip upgraded${NC}"

# Install dependencies
echo -e "${YELLOW}📚 Installing dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"

# Create necessary directories
echo -e "${YELLOW}📁 Creating directories...${NC}"
mkdir -p reports/screenshots
mkdir -p reports/allure-results
mkdir -p reports/allure-report
echo -e "${GREEN}✅ Directories created${NC}"

# Verify installation
echo -e "${YELLOW}🔍 Verifying installation...${NC}"
python -c "import selenium, pytest, allure; print('✅ Main dependencies OK')"
python -c "from config.config import Config; print('✅ Configuration OK')"
python -c "from pages.base_page import BasePage; print('✅ Page Objects OK')"
echo -e "${GREEN}✅ Installation verified${NC}"

echo ""
echo -e "${GREEN}🎉 Installation completed successfully!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run tests: make test"
echo "3. Run specific tests: make test-login"
echo "4. Generate report: make report"
echo ""
echo -e "${GREEN}Happy Testing! 🚀${NC}"