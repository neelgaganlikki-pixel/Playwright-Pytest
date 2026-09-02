# OrangeHRM Playwright Python Automation Framework

## Project Overview

This is a **production-style web automation framework** built with **Python + Playwright + pytest** for the **OrangeHRM** web application. The framework follows industry best practices including Page Object Model, environment-specific configuration, secure credential handling, and comprehensive reporting.

**Author**: Senior SDET / Automation Architect  
**Experience**: 5.9 years QA & Automation Testing  
**Status**: ✅ Login + Logout working | Ready for extension

---

## Application Under Test

| Property | Value |
|----------|-------|
| **Application** | OrangeHRM (Open Source HRMS) |
| **Demo URL** | https://opensource-demo.orangehrmlive.com |
| **Version** | OrangeHRM OS 5.9 |
| **Initial Scope** | Login → Dashboard → Logout |

---

## Technology Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.14+ | Programming language |
| Playwright | 1.62.0 | Browser automation |
| pytest | 9.1.1 | Test framework |
| pytest-playwright | 0.9.0 | Playwright integration for pytest |
| python-dotenv | 1.2.3 | Environment variable management |

---

## Project Structure

```
orangehrm-playwright-python/
│
├── .env                          # Environment variables (gitignored)
├── .gitignore                    # Git ignore rules
├── pytest.ini                    # Pytest configuration
├── requirements.txt              # Python dependencies
├── README.md                     # Comprehensive documentation
├── readme_python.md              # This file - ChatGPT-ready context
├── conftest.py                   # Pytest fixtures & hooks
│
├── config/
│   └── config_reader.py          # Environment config loader
│
├── test_data/
│   └── users.json                # Test credentials (placeholders)
│
├── utils/
│   └── test_data_reader.py       # JSON test data reader
│
├── pages/
│   ├── login_page.py             # Login Page Object
│   └── dashboard_page.py         # Dashboard Page Object
│
├── fixtures/
│   └── (empty - pytest-playwright provides browser fixtures)
│
├── tests/
│   └── login/
│       └── test_login_logout.py  # Login/Logout test suite
│
└── .venv/                        # Virtual environment (gitignored)
```

---

## Framework Architecture

```
                    ORANGEHRM
                        │
                        ▼
               PLAYWRIGHT + PYTHON
                        │
             ┌──────────┼──────────┐
             │          │          │
            POM      FIXTURES   TEST DATA
             │          │          │
             └──────────┼──────────┘
                        │
                 ENVIRONMENT CONFIG
                        │
             ┌──────────┼──────────┐
             │          │          │
            DEV        QA         UAT
             │          │          │
             └──────────┼──────────┘
                        │
                     TESTS
                        │
                  LOGIN / LOGOUT
```

---

## Prerequisites

- Python 3.10+
- Git
- Virtual environment (recommended)

---

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd orangehrm-playwright-python

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

---

## Environment Configuration

The framework supports multiple environments through `.env` file:

```bash
# Environment: dev, qa, uat, prod
TEST_ENV=dev

# Base URLs for different environments
DEV_BASE_URL=https://opensource-demo.orangehrmlive.com
QA_BASE_URL=https://opensource-demo.orangehrmlive.com
UAT_BASE_URL=https://opensource-demo.orangehrmlive.com
PROD_BASE_URL=https://opensource-demo.orangehrmlive.com

# Credentials (use placeholders in .env, real values in local .env only)
DEV_USERNAME=Admin
DEV_PASSWORD=admin123
QA_USERNAME=Admin
QA_PASSWORD=admin123
UAT_USERNAME=Admin
UAT_PASSWORD=admin123
PROD_USERNAME=Admin
PROD_PASSWORD=admin123

# Browser settings
BROWSER=chromium
HEADLESS=false
SLOW_MO=0

# Reporting
SCREENSHOT_ON_FAILURE=true
VIDEO_ON_FAILURE=true
TRACE_ON_FAILURE=true
```

### Running Tests Against Different Environments

```bash
# Run against dev (default)
TEST_ENV=dev pytest tests/login/test_login_logout.py

# Run against QA
TEST_ENV=qa pytest tests/login/test_login_logout.py

# Run against UAT
TEST_ENV=uat pytest tests/login/test_login_logout.py

# Run against PROD
TEST_ENV=prod pytest tests/login/test_login_logout.py
```

---

## Test Data

Test data is stored in JSON files under `test_data/`:

```json
{
    "valid_user": {
        "username": "Admin",
        "password": "admin123"
    },
    "invalid_user": {
        "username": "invalid_user",
        "password": "invalid_password"
    }
}
```

**Important**: Never commit real credentials to version control. Use `.env` for sensitive data.

---

## Page Object Model

### LoginPage (`pages/login_page.py`)

**Responsibilities**:
- Username locator
- Password locator
- Login button
- Login action
- Login page validation
- Error message validation

**Usage**:
```python
login_page.navigate(config.base_url)
login_page.login(username, password)
login_page.verify_login_page()
login_page.verify_login_error("Invalid credentials")
```

**Locators (validated against real OrangeHRM)**:
```python
self.username_input = page.get_by_placeholder("Username")
self.password_input = page.get_by_placeholder("Password")
self.login_button = page.get_by_role("button", name="Login")
self.forgot_password_link = page.get_by_text("Forgot your password?")
```

### DashboardPage (`pages/dashboard_page.py`)

**Responsibilities**:
- Dashboard validation
- User/profile menu
- Logout action
- Logout validation

**Usage**:
```python
dashboard_page.verify_dashboard()
dashboard_page.logout()
dashboard_page.verify_logout()
```

**Locators (validated against real OrangeHRM)**:
```python
self.dashboard_heading = page.get_by_role("heading", name="Dashboard")
self.user_dropdown = page.locator(".oxd-userdropdown-img").first
self.logout_link = page.get_by_role("menuitem", name="Logout")
self.logout_link_alt = page.locator(".oxd-userdropdown-link:has-text('Logout')")
```

---

## Pytest Fixtures

Defined in `conftest.py`:

| Fixture | Scope | Description |
|---------|-------|-------------|
| `login_page` | function | LoginPage instance |
| `dashboard_page` | function | DashboardPage instance |
| `valid_user` | session | Valid user credentials from test data |
| `invalid_user` | session | Invalid user credentials from test data |
| `page` | function | Playwright page (from pytest-playwright) |

**Hook**: `pytest_runtest_makereport` - captures test result for screenshot-on-failure

---

## Login Workflow

```text
Open OrangeHRM
      ↓
Enter valid username
      ↓
Enter valid password
      ↓
Click Login
      ↓
Verify successful login (Dashboard displayed)
```

**Implementation**:
```python
def test_valid_login_logout(self, page, login_page, dashboard_page, valid_user):
    login_page.navigate(config.base_url)
    login_page.verify_login_page()
    login_page.login(valid_user["username"], valid_user["password"])
    dashboard_page.verify_dashboard()
    dashboard_page.logout()
    dashboard_page.verify_logout()
    login_page.verify_login_page()
```

---

## Logout Workflow

```text
Dashboard
   ↓
Open user/profile menu
   ↓
Click Logout
   ↓
Verify user is returned to Login page
```

**Implementation**:
```python
def logout(self):
    self.open_user_menu()
    try:
        self.logout_link.click()
    except Exception:
        self.logout_link_alt.click()

def verify_logout(self):
    expect(self.page).to_have_url(re.compile(r".*/web/index\.php/auth/login"))
```

---

## Test Execution

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/login/test_login_logout.py -v
```

### Run with Markers

```bash
# Run only smoke tests
pytest -m smoke -v

# Run only login tests
pytest -m login -v

# Run only dashboard tests
pytest -m dashboard -v
```

### Run with Specific Browser

```bash
# Run with Firefox
pytest --browser=firefox

# Run with WebKit
pytest --browser=webkit

# Run headless
pytest --headed=false
```

### Run with Parallel Execution

```bash
pytest -n auto
```

---

## Reporting

The framework generates the following artifacts on test failure:

- **Screenshots**: `test-results/screenshots/`
- **Videos**: `test-results/videos/`
- **Traces**: Available via Playwright trace viewer

### View Playwright Report

```bash
# Generate and open HTML report
pytest --html=report.html --self-contained-html
```

### View Trace

```bash
playwright show-trace test-results/traces/trace.zip
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Browser not found | Run `playwright install` |
| DNS resolution errors | Check network connectivity to OrangeHRM demo site |
| Timeout errors | Increase timeout or check `SLOW_MO` setting |
| Fixture scope errors | Ensure page object fixtures are function-scoped |

### Debug Mode

```bash
# Run with debug output
pytest -v --tb=long

# Run with Playwright debug
PWDEBUG=1 pytest tests/login/test_login_logout.py
```

---

## Interview Explanations

### Why Playwright?

> "Playwright provides reliable auto-waiting, cross-browser support (Chromium, Firefox, WebKit), and excellent debugging tools like trace viewer. It handles modern web apps with Shadow DOM, iframes, and dynamic content better than Selenium. The API is clean and the test execution is faster."

### Why Python?

> "Python has excellent readability, a rich ecosystem for testing (pytest, hypothesis), and great CI/CD integration. It's widely adopted in the QA community and has strong typing support with type hints."

### Why pytest?

> "pytest is the de facto standard for Python testing. It has powerful fixtures for dependency injection, parametrization for data-driven tests, excellent plugin ecosystem (pytest-playwright, pytest-html), and clean assertion introspection."

### Why Page Object Model?

> "POM separates test logic from page implementation. It reduces code duplication, improves maintainability, and makes tests readable. When UI changes, you only update the page object, not every test."

### Why fixtures?

> "Fixtures provide dependency injection with automatic setup/teardown. They're scoped (session, function, class, module) so you can share expensive resources like browser instances while keeping tests isolated."

### How do you handle environments?

> "Environment-specific config lives in `.env` loaded via python-dotenv. A ConfigReader class reads the active environment (TEST_ENV) and exposes base_url, credentials, browser settings. Tests use `config.base_url` instead of hardcoded URLs."

### How do you handle credentials?

> "Never hardcode credentials. Use `.env` file (gitignored) with python-dotenv. In CI/CD, inject secrets via environment variables. Test data JSON files use placeholders; real values come from `.env` at runtime."

### How does Login work in your framework?

> "LoginPage encapsulates all login interactions. Test calls `login_page.login(username, password)` which fills fields and clicks submit. Then DashboardPage verifies successful login by checking for the Dashboard heading and URL."

### How do you handle Logout?

> "DashboardPage has `logout()` method that clicks the user dropdown (`.oxd-userdropdown-img`) then clicks the Logout menu item. It verifies logout by asserting the URL returns to the login page."

### How do you debug a failed test?

> "1. Check screenshot in `test-results/screenshots/`. 2. Watch video in `test-results/videos/`. 3. Open trace with `playwright show-trace`. 4. Run with `PWDEBUG=1` for step-by-step debugging. 5. Check console logs and network requests in trace."

---

## Key Implementation Details

### URL Patterns (Regex for Playwright)

```python
# Login page
re.compile(r".*/web/index\.php/auth/login")

# Dashboard page
re.compile(r".*/web/index\.php/dashboard/index")
```

### Locator Strategy Priority

1. `page.get_by_role()` - Most accessible, stable
2. `page.get_by_label()` - Form labels
3. `page.get_by_placeholder()` - Input placeholders
4. `page.get_by_text()` - Visible text
5. `page.get_by_test_id()` - data-testid attributes
6. CSS selectors - When above not available
7. XPath - Last resort only

### Synchronization

- **NO** `page.wait_for_timeout()` - Anti-pattern
- **YES** Playwright auto-waiting (built-in)
- **YES** Condition-based: `expect(locator).to_be_visible()`
- **YES** URL assertions: `expect(page).to_have_url(regex)`

### Assertions

- Validate **business outcomes**, not implementation details
- ✅ Dashboard is displayed
- ✅ Login page is displayed after logout
- ❌ Button was clicked (meaningless)

---

## Future Enhancements (Roadmap)

- [ ] Employee Management (PIM module)
- [ ] Leave Management
- [ ] Admin Module
- [ ] API Testing Integration
- [ ] Parallel Execution Configuration
- [ ] Retry Mechanism for Flaky Tests
- [ ] Docker Support
- [ ] Jenkins/GitHub Actions CI/CD Pipeline
- [ ] Advanced Reporting (Allure, ReportPortal)

---

## License

MIT License - Feel free to use and modify for your projects.

---

## Quick Reference for ChatGPT

When extending this framework:

1. **Reuse existing**: Config, fixtures, login, page objects, utils
2. **Add new**: Page Object only if new page/module, test data only if new data needed
3. **Follow pattern**: `pages/new_page.py` → `tests/module/test_new.py`
4. **Run**: `pytest tests/module/test_new.py -v`
5. **Update**: This README with new functionality

**Framework is production-ready for Login/Logout. Extend incrementally.**