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

        self.buzz_nav_link = page.get_by_role(
            "link",
            name="Buzz"
        )

        self.buzz_header = page.get_by_role(
            "heading",
            name="Buzz"
        )

        self.post_editor = page.get_by_role(
            "textbox",
            name="What's on your mind?"
        )

        self.post_button = page.get_by_role(
            "button",
            name="Post",
            exact=True
        )

    def open_buzz(self) -> None:
        """Navigate to the Buzz module using the application URL."""

        print("Opening Buzz module...")

        self.page.goto(
            f"{config.base_url}/web/index.php/buzz/viewBuzz",
            wait_until="domcontentloaded"
        )

        expect(self.page).to_have_url(
            re.compile(r".*/web/index\.php/buzz/.*")
        )

        expect(self.buzz_header).to_be_visible(
            timeout=10000
        )

        expect(self.post_editor).to_be_visible(
            timeout=10000
        )

        print("Buzz module loaded successfully.")

    def create_post(self, post_text: str) -> None:
        """Type a post and submit it."""

        print(f"Creating Buzz post: {post_text}")

        expect(self.post_editor).to_be_visible(
            timeout=10000
        )

        self.post_editor.click()

        self.post_editor.fill(post_text)

        print("Buzz post text entered successfully.")

        expect(self.post_button).to_be_visible(
            timeout=10000
        )

        expect(self.post_button).to_be_enabled(
            timeout=10000
        )

        print("Post button is visible and enabled.")

        self.post_button.click()

        print("Post button clicked.")

        # Wait for the application to process the post.
        self.page.wait_for_timeout(2000)

        print("Waiting for Buzz feed to update...")

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

        print(
            f"Verifying Buzz post: {expected_post}"
        )

        post = self.page.get_by_text(
            expected_post,
            exact=True
        ).first

        try:
            expect(post).to_be_visible(
                timeout=15000
            )

            print(
                f"Buzz post created and verified: {expected_post}"
            )

            self.save_post_to_file(
                expected_post
            )

        except AssertionError:
            print(
                "Buzz post was not found in the feed."
            )

            print(
                f"Expected post text: {expected_post}"
            )

            print(
                f"Current URL: {self.page.url}"
            )

            # Give the feed additional time in case the application
            # is still processing the post.
            self.page.wait_for_timeout(2000)

            # Retry the exact text once.
            post = self.page.get_by_text(
                expected_post,
                exact=True
            ).first

            expect(post).to_be_visible(
                timeout=10000
            )

            print(
                f"Buzz post created and verified after retry: "
                f"{expected_post}"
            )

            self.save_post_to_file(
                expected_post
            )