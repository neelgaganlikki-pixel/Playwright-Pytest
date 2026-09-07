
"""Buzz post creation and deletion tests for OrangeHRM."""

import pytest

from playwright.sync_api import Page

from pages.buzz_page import BuzzPage

from utils.test_data_reader import test_data


@pytest.mark.smoke
@pytest.mark.buzz
class BuzzpostTest:

    """Test suite for Buzz post creation and deletion."""

    def test_create_buzz_post(

        self,

        logged_in_page: Page,

    ):

        """Create, verify, delete, and verify deletion of a Buzz post."""

        buzz_post = test_data.load_json("buzz.json")["post_text"]

        page = logged_in_page

        buzz_page = BuzzPage(page)

        buzz_page.open_buzz()

        buzz_page.create_post(buzz_post)

        buzz_page.verify_post_created(buzz_post)

        buzz_page.delete_post(buzz_post)

        buzz_page.verify_post_deleted(buzz_post)

        print(f"pytest buzz result: {buzz_post}")
