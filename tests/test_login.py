import pytest
import os
from pages.login_page import LoginPage
from utils.webdriver_setup import get_driver

@pytest.fixture
def driver():
    """Setup WebDriver for the test and close after execution"""
    driver = get_driver()
    yield driver
    driver.quit()

def test_login_without_credentials(driver):
    """Verify error messages when clicking Login without entering credentials"""
    login_page = LoginPage(driver)
    
    # Open the login page
    login_page.open_login_page()
    
    # Handle the popup modal
    login_page.close_modal_if_present()
    
    # Click the Login button
    login_page.click_login_button()
    
    # Get and print error messages
    errors = login_page.get_error_messages()
    for field, message in errors.items():
        print(f"Error message for {field}: {message}")

    # Assertions
    assert errors["id_number"] != "", "ID Number field error message is missing!"
    assert errors["username"] != "", "Username field error message is missing!"
    assert errors["password"] != "", "Password field error message is missing!"

def test_apply_reset_password_credit_card(driver):
    """Verify that clicking 'Go Now' for credit card users redirects to the Online Banking page"""
    login_page = LoginPage(driver)

    # Open the login page
    login_page.open_login_page()
    
    # Handle the popup modal
    login_page.close_modal_if_present()

    # Click Apply/Reset Password
    login_page.click_apply_reset_password()

    # Click "Go Now" in the Credit Card section
    login_page.click_go_now_credit_card()

    # Verify if redirected to Online Banking - CUBE page
    assert login_page.verify_online_banking_page(), "Failed to reach Online Application for Online Banking - CUBE page"

    print("Successfully redirected to Online Banking application page.")

def test_capture_screenshot(driver):
    """Open website and capture a screenshot as 'Cathaybk.png'"""
    login_page = LoginPage(driver)

    # Open the website
    login_page.open_login_page()

    # Capture Screenshot
    login_page.capture_screenshot("Cathaybk.png")

    # Assert if screenshot exists
    assert os.path.exists("Cathaybk.png"), "Screenshot file was not saved!"

    print("Test passed: Screenshot successfully captured and saved.")