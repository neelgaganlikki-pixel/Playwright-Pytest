
"""Buzz post creation tests for OrangeHRM."""

import pytest

from playwright.sync_api import Page

from pages.buzz_page import BuzzPage

from utils.test_data_reader import test_data


@pytest.mark.smoke
@pytest.mark.buzz
class BuzzpostTest:

    """Test suite for Buzz post creation."""

    def test_create_buzz_post(

        self,

        logged_in_page: Page,

    ):

        """Create a new Buzz post and verify it appears in the feed."""

        buzz_post = test_data.load_json("buzz.json")["post_text"]

        page = logged_in_page

        buzz_page = BuzzPage(page)

        buzz_page.open_buzz()

        buzz_page.create_post(buzz_post)

        buzz_page.verify_post_created(buzz_post)

        print(f"pytest buzz result: {buzz_post}")
