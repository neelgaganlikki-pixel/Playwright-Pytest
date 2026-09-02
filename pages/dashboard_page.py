"""Dashboard Page Object for OrangeHRM."""

import re
from playwright.sync_api import Page, expect


class DashboardPage:
    """Page Object for OrangeHRM Dashboard page."""
    
    def __init__(self, page: Page):
        self.page = page
        self.dashboard_heading = page.get_by_role("heading", name="Dashboard")
        self.user_dropdown = page.locator(".oxd-userdropdown-img").first
        self.logout_link = page.get_by_role("menuitem", name="Logout")
        # Alternative logout locator
        self.logout_link_alt = page.locator(".oxd-userdropdown-link:has-text('Logout')")
    
    def verify_dashboard(self) -> None:
        """Verify dashboard is displayed."""
        expect(self.dashboard_heading).to_be_visible()
        expect(self.page).to_have_url(re.compile(r".*/web/index\.php/dashboard/index"))
    
    def open_user_menu(self) -> None:
        """Open user profile dropdown menu."""
        self.user_dropdown.click()
    
    def logout(self) -> None:
        """Perform logout."""
        self.open_user_menu()
        # Try primary locator first, fallback to alternative
        try:
            self.logout_link.click()
        except Exception:
            self.logout_link_alt.click()
    
    def verify_logout(self) -> None:
        """Verify user is logged out (back on login page)."""
        expect(self.page).to_have_url(re.compile(r".*/web/index\.php/auth/login"))