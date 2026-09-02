"""Buzz Page Object for OrangeHRM."""

import re
from pathlib import Path

from playwright.sync_api import Page, expect

from config.config_reader import config


class BuzzPage:
    """Page Object for OrangeHRM Buzz module."""

    __test__ = False

    def __init__(self, page: Page):
        self.page = page

        self.output_file = (
            Path(__file__).resolve().parent.parent
            / "tests"
            / "buzz"
            / "buzz_post_output.txt"
        )

        self.buzz_nav_link = page.get_by_role("link", name="Buzz")
        self.buzz_header = page.get_by_role("heading", name="Buzz")

        self.post_editor = page.locator(
            "textarea, "
            "[contenteditable='true'], "
            "[role='textbox'], "
            "[placeholder*='post'], "
            "[placeholder*='message'], "
            "[placeholder*='share']"
        ).first

        self.post_button = (
            page.locator("button")
            .filter(has_text="Post")
            .first
        )

    def open_buzz(self) -> None:
        """Navigate to the Buzz module using the application URL."""

        self.page.goto(
            f"{config.base_url}/web/index.php/buzz/viewBuzz"
        )

        expect(self.page).to_have_url(
            re.compile(r".*/web/index\.php/buzz/.*")
        )

        expect(self.page.locator("body")).to_contain_text("Buzz")

    def create_post(self, post_text: str) -> None:
        """Type a post and submit it."""

        expect(self.post_editor).to_be_visible()

        self.post_editor.click()
        self.post_editor.fill(post_text)

        expect(self.post_button).to_be_visible()
        self.post_button.click()

    def save_post_to_file(self, post_text: str) -> None:
        """Persist the posted message in a TXT file inside the buzz folder."""

        self.output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.output_file.write_text(
            post_text,
            encoding="utf-8"
        )

        print(
            f"Buzz result saved to: {self.output_file}"
        )

    def verify_post_created(self, expected_post: str) -> None:
        """Validate the new post appears in the Buzz feed."""

        post = self.page.get_by_text(
            expected_post,
            exact=True
        ).first

        expect(post).to_be_visible(timeout=10000)

        print(
            f"Buzz post created and verified: {expected_post}"
        )

        self.save_post_to_file(expected_post)