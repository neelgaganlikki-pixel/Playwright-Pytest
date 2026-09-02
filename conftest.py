"""Pytest configuration and fixtures."""

import logging
import os

import pytest
from playwright.sync_api import Page

from config.config_reader import config
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from utils.test_data_reader import test_data

logger = logging.getLogger("orangehrm_tests")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)


def pytest_addoption(parser):
    """Add a pytest CLI option to select the environment."""
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help="Select environment: dev, qa, uat, prod",
    )


@pytest.fixture(scope="session", autouse=True)
def configure_environment(request):
    """Apply the environment selected through pytest CLI."""
    selected_env = request.config.getoption("--env")
    if selected_env:
        config.set_environment(selected_env)
        os.environ["TEST_ENV"] = config.current_env
    return config


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Configure launcher args for a visible, controllable browser session."""
    return {
        "headless": False,
        "slow_mo": int(os.getenv("SLOW_MO", "0")),
    }


@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    """Provide LoginPage instance."""
    return LoginPage(page)


@pytest.fixture(scope="function")
def dashboard_page(page: Page) -> DashboardPage:
    """Provide DashboardPage instance."""
    return DashboardPage(page)


@pytest.fixture(scope="function")
def logged_in_page(page: Page, login_page: LoginPage, dashboard_page: DashboardPage, valid_user: dict) -> Page:
    """Return a page already authenticated for tests that need a logged-in state."""
    logger.info("Logging in user: %s", valid_user["username"])
    login_page.navigate(config.base_url)
    login_page.login(valid_user["username"], valid_user["password"])
    dashboard_page.verify_dashboard()
    return page


@pytest.fixture(scope="session")
def valid_user():
    """Provide valid user credentials."""
    return test_data.get_user("valid_user")


@pytest.fixture(scope="session")
def invalid_user():
    """Provide invalid user credentials."""
    return test_data.get_user("invalid_user")


@pytest.fixture(autouse=True)
def capture_screenshot_on_failure(request, page: Page):
    """Capture a screenshot only when a test fails."""
    yield

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshot_path = f"test-results/screenshots/{request.node.name}.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"\nScreenshot saved: {screenshot_path}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test result for screenshot fixture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Log the start of each test for debugging visibility."""
    logger.info("Starting test: %s", item.nodeid)
