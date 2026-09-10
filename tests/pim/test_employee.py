"""End-to-end OrangeHRM PIM employee automation."""

import logging

import pytest
from playwright.sync_api import Page

from pages.employee_page import EmployeePage
from utils.employee_data_generator import generate_employee_data, write_user_data


logger = logging.getLogger("orangehrm_tests")


@pytest.mark.smoke
@pytest.mark.pim
class TestEmployee:
    """Test suite for creating, verifying, and deleting an employee."""

    def test_create_verify_delete_employee(self, logged_in_page: Page):
        """Complete the PIM employee lifecycle with one runtime data object."""
        page = logged_in_page
        employee_page = EmployeePage(page)
        runtime_data = generate_employee_data()
        employee = runtime_data["employee"]
        employee_login = runtime_data["employee_login"]
        employee_created = False

        logger.info("Starting PIM employee creation test.")
        logger.info("Opening PIM and Add Employee.")

        try:
            employee_page.open_pim()
            employee_page.open_employee_list()
            employee_page.open_add_employee()

            employee_page.fill_employee_name(
                employee["first_name"],
                employee["middle_name"],
                employee["last_name"],
            )
            employee_page.fill_employee_id(employee["employee_id"])
            employee_page.upload_employee_photo(runtime_data["photo"]["path"])
            employee_page.enable_create_login_details()
            employee_page.fill_employee_login(
                employee_login["username"],
                employee_login["status"],
                employee_login["password"],
            )

            logger.info("Saving employee.")
            employee_page.save_employee()
            employee_created = True
            logger.info("Employee creation success toast verified.")

            logger.info("Filling Personal Details and Custom Fields.")
            employee_page.fill_personal_details(employee)
            employee_page.fill_custom_fields(runtime_data["custom_fields"])

            # Persist the actual live dropdown selections and all other values
            # before continuing with verification and deletion.
            write_user_data(runtime_data)

            employee_page.save_personal_details()
            logger.info("Personal Details success toast verified.")

            employee_page.return_to_employee_list()
            employee_page.search_employee(employee["employee_id"])
            employee_page.verify_employee(runtime_data["employee"])
            logger.info("Employee verified successfully.")

            logger.info("Starting employee deletion.")
            employee_page.delete_employee(employee["employee_id"])
            logger.info("Delete success toast verified.")

            employee_page.return_to_employee_list()
            search_id = employee_page._field("Employee Id").first
            search_id.fill(employee["employee_id"])
            page.get_by_role("button", name="Search", exact=True).click()
            employee_page.verify_employee_not_present(employee["employee_id"])
            logger.info("Employee deletion verified successfully.")

        finally:
            if employee_created:
                # Keep the original test failure intact. Cleanup is only a
                # best-effort fallback when the normal deletion did not run.
                try:
                    employee_page.return_to_employee_list()
                    search_id = employee_page._field("Employee Id").first
                    search_id.fill(employee["employee_id"])
                    page.get_by_role("button", name="Search", exact=True).click()
                    row = employee_page.employee_row(employee["employee_id"])
                    if row.count() > 0 and row.is_visible():
                        employee_page.delete_employee(employee["employee_id"])
                except Exception:
                    logger.exception("Best-effort employee cleanup failed.")
