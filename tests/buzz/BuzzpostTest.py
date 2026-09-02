"""Buzz post creation tests for OrangeHRM."""

import pytest

from playwright.sync_api import Page

from config.config_reader import config
from pages.buzz_page import BuzzPage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from utils.test_data_reader import test_data


@pytest.mark.smoke
@pytest.mark.buzz
class BuzzpostTest:
    """Test suite for Buzz post creation."""

    def test_create_buzz_post(
        self,
        page: Page,
        login_page: LoginPage,
        dashboard_page: DashboardPage,
        valid_user: dict,
    ):
        """Create a new Buzz post and verify it appears in the feed."""

        buzz_post = test_data.load_json("buzz.json")["post_text"]

        login_page.navigate(config.base_url)
        login_page.verify_login_page()
        login_page.login(
            valid_user["username"],
            valid_user["password"]
        )

        dashboard_page.verify_dashboard()

        buzz_page = BuzzPage(page)

        buzz_page.open_buzz()
        buzz_page.create_post(buzz_post)
        buzz_page.verify_post_created(buzz_post)
        print(f"pytest buzz result: {buzz_post}")