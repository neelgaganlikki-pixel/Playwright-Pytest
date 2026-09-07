"""Buzz Page Object for OrangeHRM."""

import re
from pathlib import Path

from playwright.sync_api import (
    Page,
    TimeoutError as PlaywrightTimeoutError,
    expect,
)

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

        self.created_post_card = None

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

        print("Post creation started.")
        print(f"Creating Buzz post: {post_text}")

        expect(self.post_editor).to_be_visible(
            timeout=10000
        )

        self.post_editor.click()

        self.post_editor.fill(
            post_text
        )

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

        print("Post created.")

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

            self.created_post_card = post.locator(
                "xpath=ancestor::*[.//li//button][1]"
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

            post = self.page.get_by_text(
                expected_post,
                exact=True
            ).first

            expect(post).to_be_visible(
                timeout=10000
            )

            self.created_post_card = post.locator(
                "xpath=ancestor::*[.//li//button][1]"
            )

            print(
                f"Buzz post created and verified after retry: "
                f"{expected_post}"
            )

            self.save_post_to_file(
                expected_post
            )

    def delete_post(self, post_text: str) -> None:
        """
        Delete the Buzz post that contains exactly ``post_text``.

        The post is located by its text, then the action menu button
        inside that same post card is opened so the Delete option can
        never come from another post.
        """

        print("Delete action started.")

        print(
            f"Locating Buzz post to delete: {post_text}"
        )

        post_text_locator = self.page.get_by_text(
            post_text,
            exact=True
        ).first

        expect(post_text_locator).to_be_visible(
            timeout=15000
        )

        post_card = (
            self.created_post_card
            or post_text_locator.locator("xpath=..")
        )

        action_menu_button = post_card.locator(
            "li button"
        ).first

        expect(action_menu_button).to_be_visible(
            timeout=10000
        )

        print(
            "Correct post/menu selected for deletion."
        )

        action_menu_button.click()

        delete_option = self.page.get_by_role(
            "menu"
        ).get_by_text(
            "Delete Post",
            exact=True
        )

        expect(delete_option).to_be_visible(
            timeout=10000
        )

        print(
            "Delete option selected from the post menu."
        )

        delete_option.click()

        self._handle_delete_confirmation()

        print("Post deleted.")

    def _handle_delete_confirmation(self) -> None:
        """Accept the OrangeHRM delete confirmation dialog if shown."""

        print(
            "Delete confirmation dialog handling started."
        )

        confirm_dialog = self.page.get_by_role(
            "dialog"
        )

        try:
            expect(confirm_dialog).to_be_visible(
                timeout=5000
            )

            print(
                "Delete confirmation dialog is visible."
            )

            yes_delete_button = confirm_dialog.get_by_role(
                "button",
                name="Yes, Delete"
            )

            expect(yes_delete_button).to_be_visible(
                timeout=5000
            )

            yes_delete_button.click()

            print(
                "Delete confirmation handled."
            )

        except PlaywrightTimeoutError:
            print(
                "No delete confirmation dialog appeared; "
                "assuming the post was deleted directly."
            )

    def verify_post_deleted(self, post_text: str) -> None:
        """
        Verify the post is gone from the Buzz feed.

        The specific delete success toast is checked first,
        then the deleted post is asserted to be hidden.
        """

        print(
            f"Verifying Buzz post deletion: {post_text}"
        )

        delete_toast = self.page.get_by_text(
            "Successfully Deleted",
            exact=True
        )

        try:
            expect(delete_toast).to_be_visible(
                timeout=10000
            )

            print(
                "Delete success toast verified."
            )

        except PlaywrightTimeoutError:
            print(
                "Delete success toast was not visible; "
                "continuing with post visibility check."
            )

        deleted_post = self.created_post_card

        if deleted_post is None:
            deleted_post = (
                self.page.get_by_text(
                    post_text,
                    exact=True
                )
                .first
                .locator(
                    "xpath=ancestor::*[.//li//button][1]"
                )
            )

        expect(deleted_post).to_be_hidden(
            timeout=15000
        )

        print(
            f"Buzz post no longer visible: {post_text}"
        )

        self.save_post_to_file(
            f"DELETED: {post_text}"
        )