"""Login and Logout tests for OrangeHRM."""

import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from config.config_reader import config


@pytest.mark.smoke
@pytest.mark.login
class TestLoginLogout:
    """Test suite for Login and Logout functionality."""
    
    def test_valid_login_logout(
        self,
        page: Page,
        login_page: LoginPage,
        dashboard_page: DashboardPage,
        valid_user: dict
    ):
        """Test valid login followed by logout."""
        # Navigate to login page
        login_page.navigate(config.base_url)
        login_page.verify_login_page()
        
        # Perform login
        login_page.login(valid_user["username"], valid_user["password"])
        
        # Verify dashboard
        dashboard_page.verify_dashboard()
        
        # Perform logout
        dashboard_page.logout()
        
        # Verify back on login page
        dashboard_page.verify_logout()
        login_page.verify_login_page()
    
    def test_invalid_login(
        self,
        page: Page,
        login_page: LoginPage,
        invalid_user: dict
    ):
        """Test invalid login shows error."""
        # Navigate to login page
        login_page.navigate(config.base_url)
        login_page.verify_login_page()
        
        # Attempt login with invalid credentials
        login_page.login(invalid_user["username"], invalid_user["password"])
        
        # Verify error message
        login_page.verify_login_error("Invalid credentials")