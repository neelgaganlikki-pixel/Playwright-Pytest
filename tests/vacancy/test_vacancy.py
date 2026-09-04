"""Vacancy creation tests for OrangeHRM."""

from datetime import datetime

import pytest

from playwright.sync_api import Page

from config.config_reader import config

from pages.vacancy_page import VacancyPage

from utils.test_data_reader import test_data


@pytest.mark.smoke
@pytest.mark.vacancy
class TestVacancy:
    """Test suite for Vacancy creation."""

    def test_create_vacancy(
        self,
        logged_in_page: Page,
    ):
        """Create and delete a vacancy using saved authentication."""

        page = logged_in_page

        vacancy_data = test_data.load_json(
            "vacancy.json"
        )["vacancy"]

        vacancy_data["name"] = (
            f"{vacancy_data['name']}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        )

        config.save_vacancy_name(
            vacancy_data["name"]
        )

        # Create Vacancy Page object
        vacancy_page = VacancyPage(page)

        # Create vacancy
        created_vacancy_name = (
            vacancy_page.create_vacancy(
                vacancy_data
            )
        )

        # Delete vacancy
        vacancy_page.delete_vacancy(
            created_vacancy_name
        )

        print(
            f"pytest vacancy result: "
            f"{created_vacancy_name}"
        )
        