import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """Page Object Model for Cathay United Bank Login Page"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Locators
    LOGIN_BUTTON = (By.XPATH, "(//button[contains(text(), '登入')])[1]")  # Selecting the first button

    ID_FIELD = (By.XPATH, "//input[@placeholder='身分證字號']")
    USERNAME_FIELD = (By.XPATH, "//input[@placeholder='用戶代號']")
    PASSWORD_FIELD = (By.XPATH, "//input[@placeholder='網銀密碼']")

    ID_ERROR = (By.XPATH, "//input[@id='CustID']/following-sibling::div[@class='msg-wrapper']/p")
    USERNAME_ERROR = (By.XPATH, "//input[@id='UserIdKeyin']/ancestor::div[@class='controls']/div[@class='msg-wrapper']/p")
    PASSWORD_ERROR = (By.XPATH, "//input[@id='PasswordKeyin']/ancestor::div[@class='controls']/div[@class='msg-wrapper']/p")

    MODAL_CONTENT = (By.CLASS_NAME, "modal-content")  # Popup container
    MODAL_CLOSE_BUTTON = (By.XPATH, "(//button[contains(text(), '我知道了')])[2]")  # "I Understand" button

    ENGLISH_LANGUAGE_BUTTON = (By.XPATH, "//a[@href='/MyBank/Quicklinks/Home/SetMultiLanguage?Culture=en-US']")  # Language switch

    APPLY_RESET_PASSWORD_BUTTON = (By.XPATH, "//a[contains(text(), '申請/重設網銀密碼') and @onclick='ShowApplyResetMsg()']") # "Apply/Reset Password" button
    GO_NOW_BUTTON = (By.XPATH, "(//button[contains(text(), '立即前往')])[2]") # "Go Now" button for "I only have a credit card"

    def open_login_page(self):
        """Navigate to the website"""
        self.driver.get("https://www.cathaybk.com.tw/mybank/")

    def close_modal_if_present(self):
        """Close the popup modal if it appears"""
        try:
            modal_popup = self.wait.until(EC.presence_of_element_located(self.MODAL_CONTENT))
            if modal_popup:
                print("Popup detected! Closing it...")
                self.wait.until(EC.element_to_be_clickable(self.MODAL_CLOSE_BUTTON)).click()
                WebDriverWait(self.driver, 3).until(EC.invisibility_of_element(modal_popup))
                print("Popup closed.")
        except Exception as e:
            print("No popup detected or failed to close it:", e)

    def switch_to_english(self):
        """Click the language switch button to change to English"""
        try:
            english_button = self.wait.until(EC.element_to_be_clickable(self.ENGLISH_LANGUAGE_BUTTON))
            english_button.click()
            WebDriverWait(self.driver, 3).until(EC.url_contains("Culture=en-US"))
            print("Switched to English successfully.")
        except Exception as e:
            print("Failed to switch to English:", e)

    def click_login_button(self):
        """Click the Login button without entering credentials"""
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()

    def click_apply_reset_password(self):
        """Click the Apply/Reset Password button"""
        self.wait.until(EC.element_to_be_clickable(self.APPLY_RESET_PASSWORD_BUTTON)).click()
        print("Navigated to Apply/Reset Password section.")

    def click_go_now_credit_card(self):
        """Click the 'Go Now' button under 'I only have a credit card' section"""
        self.wait.until(EC.element_to_be_clickable(self.GO_NOW_BUTTON)).click()
        print("Clicked 'Go Now' under credit card section.")
    
    def verify_online_banking_page(self):
        """Switch to the new tab and verify 'Online Application for Online Banking - CUBE' page"""
        expected_url = "https://www.cathaybk.com.tw/MyBank/Quicklinks/Outer/CPIN_Apply_Inp"
        expected_h2_text = "線上申辦CUBE網銀"
        try:
            # Wait for a new tab to open
            WebDriverWait(self.driver, 5).until(lambda d: len(d.window_handles) > 1)

            # Switch to the newly opened tab
            new_tab = self.driver.window_handles[-1]  # Get the last opened tab
            self.driver.switch_to.window(new_tab)
            print("Switched to the new tab.")

            # Wait for the correct URL
            WebDriverWait(self.driver, 10).until(lambda d: d.current_url.strip() == expected_url)
            current_url = self.driver.current_url.strip()
            print(f"Current URL: {current_url}")

            # Verify the URL is correct
            is_correct_url = current_url == expected_url
            print(f"URL verification result: {is_correct_url}")
            assert is_correct_url, f"Expected URL '{expected_url}', but got '{current_url}'"

            # Wait for the <h2> header to load and verify its text
            h2_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), '線上申辦CUBE網銀')]"))
            )
            h2_text = h2_element.text.strip()
            print(f"H2 Header Found: {h2_text}")

            # Verify exact match with expected <h2> text
            is_correct_h2 = h2_text == expected_h2_text
            print(f"H2 header verification result: {is_correct_h2}")
            assert is_correct_h2, f"Expected H2 header '{expected_h2_text}', but got '{h2_text}'"

            # Close the new tab and switch back to the original tab
            self.driver.close()
            original_tab = self.driver.window_handles[0]  # Get the original tab
            self.driver.switch_to.window(original_tab)
            print("Switched back to the original tab.")

            return is_correct_url and is_correct_h2
        except Exception as e:
            print("Failed to verify Online Banking page:", e)
            return False
        
    def capture_screenshot(self, filename="Cathaybk.png"):
        """Capture a screenshot and save it."""
        screenshot_path = os.path.join(os.getcwd(), filename)
        self.driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved at: {screenshot_path}")

    def get_error_messages(self):
        """Capture and return error messages for all fields"""
        return {
            "id_number": self.wait.until(EC.presence_of_element_located(self.ID_ERROR)).text,
            "username": self.wait.until(EC.presence_of_element_located(self.USERNAME_ERROR)).text,
            "password": self.wait.until(EC.presence_of_element_located(self.PASSWORD_ERROR)).text
        }