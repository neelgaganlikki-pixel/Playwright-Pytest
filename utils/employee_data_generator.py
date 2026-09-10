"""Random employee test data generator for OrangeHRM PIM tests.

This module is the SOURCE of random employee values.

It generates realistic fictional test data at runtime, stores the
generated values in a single runtime structure, and writes the ACTUAL
values used during the execution to ``test_data/user_data1.json``.

``user_data1.json`` is an OUTPUT/STORAGE file only. It is never read
back as the source of random values during the same execution.
"""

import json
import random
import string
from datetime import date, timedelta
from pathlib import Path

# ------------------------------------------------------------------
# Controlled synthetic first-name pools.
#
# Gender is derived from the pool the first name is picked from, so
# the selected gender always matches the generated first name.
# ------------------------------------------------------------------

MALE_FIRST_NAMES = [
    "David",
    "Robert",
    "Michael",
    "James",
    "Daniel",
    "Matthew",
    "Andrew",
    "Christopher",
    "Joshua",
    "William",
    "Ethan",
    "Alexander",
]

FEMALE_FIRST_NAMES = [
    "Emily",
    "Sarah",
    "Jessica",
    "Laura",
    "Emma",
    "Olivia",
    "Sophia",
    "Isabella",
    "Charlotte",
    "Amelia",
    "Mia",
    "Harper",
]

MIDDLE_NAMES = [
    "Michael",
    "James",
    "Robert",
    "William",
    "David",
    "Joseph",
    "Thomas",
    "Charles",
    "Daniel",
    "Matthew",
    "Marie",
    "Ann",
    "Louise",
    "Grace",
    "Rose",
    "Jane",
    "Lynn",
    "Nicole",
]

LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Lopez",
    "Wilson",
    "Anderson",
    "Thomas",
    "Taylor",
    "Moore",
    "Jackson",
]

# ------------------------------------------------------------------
# JSON storage helpers
# ------------------------------------------------------------------

DATA_DIR = Path(__file__).resolve().parent.parent / "test_data"
USER_DATA_FILE = DATA_DIR / "user_data1.json"


def _random_alphanumeric(length: int) -> str:
    """Return a random alphanumeric string of the given length."""
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def _random_employee_username() -> str:
    """Return a fresh username that fits the OrangeHRM username field."""
    return f"JkAuto{random.randint(10000, 99999)}"


def _random_future_date(max_years: int = 10) -> str:
    """Return a random future date formatted for OrangeHRM."""
    days_ahead = random.randint(30, max_years * 365)
    future = date.today() + timedelta(days=days_ahead)
    return future.strftime("%Y-%m-%d")


def _random_past_date(min_age: int = 20, max_age: int = 60) -> str:
    """Return a random past date formatted for OrangeHRM."""
    days_back = random.randint(min_age * 365, max_age * 365)
    past = date.today() - timedelta(days=days_back)
    return past.strftime("%Y-%m-%d")


def generate_employee_data() -> dict:
    """Generate a complete runtime employee test-data structure.

    The values are generated ONCE and returned inside a single dict.
    The same dict must be reused for creation, personal details,
    verification, search, and deletion.
    """
    # Gender is derived from the first-name pool, never randomized
    # independently.
    if random.choice([True, False]):
        first_name = random.choice(MALE_FIRST_NAMES)
        gender = "Male"
    else:
        first_name = random.choice(FEMALE_FIRST_NAMES)
        gender = "Female"

    employee_id = f"{random.randint(1000, 9999)}"

    data = {
        "login": {
            "username": "Admin",
            "password": "admin123",
        },
        "employee": {
            "first_name": first_name,
            "middle_name": random.choice(MIDDLE_NAMES),
            "last_name": random.choice(LAST_NAMES),
            "employee_id": employee_id,
            "gender": gender,
            "other_id": _random_alphanumeric(6),
            "driver_license_number": _random_alphanumeric(8),
            "license_expiry_date": _random_future_date(),
            "nationality": None,  # filled from the live dropdown
            "marital_status": None,  # filled from the live dropdown
            "date_of_birth": _random_past_date(),
        },
        "employee_login": {
            "create_login_details": True,
            "username": _random_employee_username(),
            "status": "Enabled",
            "password": "JkAuto2026X9m4",
            "confirm_password": "JkAuto2026X9m4",
        },
        "custom_fields": {
            "blood_type": None,  # filled from the live dropdown
            "test_field": _random_alphanumeric(7),
        },
        "photo": {
            "path": "test_data/employee_photo.png",
        },
    }

    return data


def write_user_data(data: dict) -> None:
    """Write the ACTUAL runtime test data to user_data1.json.

    The file is an OUTPUT/STORAGE file. It is overwritten on every
    execution with the real values used by that execution.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    USER_DATA_FILE.write_text(
        json.dumps(data, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )
