#!/usr/bin/env python3
"""
Script to run QA automation framework tests
"""

import argparse
import sys
import os
import subprocess
import logging
from pathlib import Path

# Add root directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import Config


def setup_logging():
    """Setup logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('reports/test_execution.log')
        ]
    )


def run_tests(browser='chrome', headless=True, test_suite='all', parallel=False, verbose=True):
    """
    Run tests with specified options
    
    Args:
        browser (str): Browser to use
        headless (bool): Whether to run in headless mode
        test_suite (str): Test suite to run
        parallel (bool): Whether to run in parallel
        verbose (bool): Whether to show detailed output
    """
    try:
        # Create necessary directories
        os.makedirs(Config.REPORTS_DIR, exist_ok=True)
        os.makedirs(Config.SCREENSHOTS_DIR, exist_ok=True)
        os.makedirs(Config.ALLURE_RESULTS_DIR, exist_ok=True)
        
        # Build pytest command
        cmd = ['python', '-m', 'pytest']
        
        # Add options
        if verbose:
            cmd.append('-v')
        
        # Add browser options
        cmd.extend(['--browser', browser])
        if headless:
            cmd.append('--headless')
        
        # Add test suite
        if test_suite == 'all':
            cmd.append('tests/')
        else:
            cmd.append(f'tests/test_{test_suite}.py')
        
        # Add parallel execution
        if parallel:
            cmd.extend(['-n', 'auto'])
        
        # Add reporting
        cmd.extend([
            '--html=reports/pytest_report.html',
            '--self-contained-html',
            '--junitxml=reports/junit.xml',
            '--alluredir=reports/allure-results'
        ])
        
        # Execute command
        logging.info(f"Executing command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=False)
        
        if result.returncode == 0:
            logging.info("✅ Tests completed successfully")
        else:
            logging.error("❌ Tests failed")
        
        return result.returncode == 0
        
    except Exception as e:
        logging.error(f"Error running tests: {e}")
        return False


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Run QA automation tests')
    
    parser.add_argument(
        '--browser',
        choices=['chrome', 'firefox'],
        default='chrome',
        help='Browser to use for tests'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run in headless mode'
    )
    
    parser.add_argument(
        '--no-headless',
        action='store_true',
        help='Run in visible mode (overrides --headless)'
    )
    
    parser.add_argument(
        '--test-suite',
        choices=['all', 'login', 'products', 'cart', 'checkout'],
        default='all',
        help='Test suite to run'
    )
    
    parser.add_argument(
        '--parallel',
        action='store_true',
        help='Run tests in parallel'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Run in quiet mode'
    )
    
    parser.add_argument(
        '--generate-report',
        action='store_true',
        help='Generate Allure report after tests'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    
    # Determine headless mode
    headless = args.headless and not args.no_headless
    
    # Run tests
    success = run_tests(
        browser=args.browser,
        headless=headless,
        test_suite=args.test_suite,
        parallel=args.parallel,
        verbose=not args.quiet
    )
    
    # Generate report if requested
    if args.generate_report and success:
        try:
            subprocess.run(['allure', 'generate', 'reports/allure-results', '--clean', '-o', 'reports/allure-report'])
            logging.info("Allure report generated")
        except Exception as e:
            logging.error(f"Error generating Allure report: {e}")
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()