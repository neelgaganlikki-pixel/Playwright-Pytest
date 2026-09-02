"""Login Page Object for OrangeHRM."""

import re
from playwright.sync_api import Page, expect


class LoginPage:
    """Page Object for OrangeHRM Login page."""
    
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.forgot_password_link = page.get_by_text("Forgot your password?")
    
    def navigate(self, base_url: str) -> None:
        """Navigate to login page."""
        self.page.goto(f"{base_url}/web/index.php/auth/login")
    
    def login(self, username: str, password: str) -> None:
        """Perform login with credentials."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
    
    def verify_login_page(self) -> None:
        """Verify login page is displayed."""
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.login_button).to_be_visible()
        expect(self.page).to_have_url(re.compile(r".*/web/index\.php/auth/login"))
    
    def verify_login_error(self, expected_message: str) -> None:
        """Verify login error message."""
        # OrangeHRM shows error in a specific element
        error_locator = self.page.locator(".oxd-alert-content-text")
        expect(error_locator).to_be_visible()
        expect(error_locator).to_contain_text(expected_message)