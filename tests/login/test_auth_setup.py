
"""Create and save an authenticated Playwright session."""

import os

import pytest

from playwright.sync_api import Page

from config.config_reader import config

from pages.dashboard_page import DashboardPage

from pages.login_page import LoginPage


AUTH_STATE_PATH = os.path.join(

    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),

    "auth",

    "auth_state.json",

)


@pytest.mark.login
def test_create_authenticated_session(

    page: Page,

    login_page: LoginPage,

    dashboard_page: DashboardPage,

    valid_user: dict,

):

    """Login to OrangeHRM and save the authenticated browser state."""

    # Create the auth folder if it does not exist

    os.makedirs(os.path.dirname(AUTH_STATE_PATH), exist_ok=True)

    # Navigate to login page

    login_page.navigate(config.base_url)

    login_page.verify_login_page()

    # Perform login

    login_page.login(

        valid_user["username"],

        valid_user["password"],

    )

    # Verify successful login

    dashboard_page.verify_dashboard()

    # Save authenticated session

    page.context.storage_state(path=AUTH_STATE_PATH)

    print(f"\nAuthenticated session saved to: {AUTH_STATE_PATH}")
