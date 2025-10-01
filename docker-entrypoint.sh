#!/bin/bash
# Docker container entrypoint script

set -e

# Function to display help information
show_help() {
    echo "QA Automation Framework for DemoBlaze"
    echo ""
    echo "Usage: docker run <image> [command]"
    echo ""
    echo "Available commands:"
    echo "  test          - Run all tests"
    echo "  test-chrome   - Run tests with Google Chrome"
    echo "  test-firefox  - Run tests with Mozilla Firefox"
    echo "  test-smoke    - Run smoke tests"
    echo "  report        - Generate Allure report"
    echo "  serve         - Serve Allure report on port 8080"
    echo "  shell         - Open interactive shell for development"
    echo "  health        - Check container health"
    echo "  help          - Show this help"
    echo ""
    echo "Environment variables:"
    echo "  BROWSER       - Browser to use (chrome/firefox)"
    echo "  HEADLESS      - Headless mode (true/false)"
    echo "  TEST_SUITE    - Test suite (all/login/products/cart/checkout)"
}

# Function to setup virtual display (Xvfb)
setup_display() {
    echo "Setting up virtual display..."
    export DISPLAY=:99
    
    # Start virtual X server in background
    Xvfb :99 -screen 0 1920x1080x24 -ac +extension GLX +render -noreset &
    XVFB_PID=$!
    
    # Wait for X server to be ready
    for i in {1..30}; do
        if xdpyinfo -display :99 >/dev/null 2>&1; then
            echo "Virtual display configured successfully"
            break
        fi
        echo "Waiting for virtual display... ($i/30)"
        sleep 1
    done
    
    # Verify that X server is working correctly
    if ! xdpyinfo -display :99 >/dev/null 2>&1; then
        echo "Error: Could not configure virtual display"
        exit 1
    fi
}

# Function to cleanup processes on exit
cleanup() {
    echo "Cleaning up processes..."
    if [ ! -z "$XVFB_PID" ]; then
        kill $XVFB_PID 2>/dev/null || true
    fi
    pkill -f Xvfb 2>/dev/null || true
}

# Setup trap for automatic cleanup on exit
trap cleanup EXIT

# Main function to run tests
run_tests() {
    local browser=${BROWSER:-chrome}
    local headless=${HEADLESS:-true}
    local test_suite=${TEST_SUITE:-all}
    
    echo "Running tests with the following configuration:"
    echo "  Browser: $browser"
    echo "  Headless mode: $headless"
    echo "  Test suite: $test_suite"
    echo ""
    
    # Setup virtual display only if not in headless mode
    if [ "$headless" = "false" ]; then
        setup_display
    fi
    
    python scripts/run_tests.py \
        --browser="$browser" \
        --headless="$headless" \
        --test-suite="$test_suite"
}

# Function to generate Allure reports
generate_report() {
    echo "Generating Allure report..."
    if [ ! -d "reports/allure-results" ]; then
        echo "Error: No Allure results found"
        exit 1
    fi
    allure generate reports/allure-results --clean -o reports/allure-report
    echo "Report generated successfully in reports/allure-report/"
}

# Function to serve Allure reports
serve_report() {
    echo "Serving Allure report on port 8080..."
    if [ ! -d "reports/allure-results" ]; then
        echo "Error: No Allure results found"
        exit 1
    fi
    allure serve reports/allure-results --port 8080 --host 0.0.0.0
}

# Function to check container health
health_check() {
    echo "Checking container health..."
    python -c "import selenium; print('✅ Selenium OK')"
    python -c "import pytest; print('✅ Pytest OK')"
    python -c "from config.config import Config; print('✅ Config OK')"
    echo "✅ Container healthy"
}

# Process command received as argument
case "${1:-test}" in
    test)
        run_tests
        ;;
    test-chrome)
        BROWSER=chrome run_tests
        ;;
    test-firefox)
        BROWSER=firefox run_tests
        ;;
    test-smoke)
        TEST_SUITE=login run_tests
        ;;
    report)
        generate_report
        ;;
    serve)
        serve_report
        ;;
    shell)
        exec /bin/bash
        ;;
    health)
        health_check
        ;;
    help)
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
