"""Configuration reader for environment-specific settings."""

import os
from pathlib import Path

from dotenv import load_dotenv


class ConfigReader:
    """Reads and provides environment-specific configuration."""

    VALID_ENVIRONMENTS = {"dev", "qa", "uat", "prod"}

    def __init__(self, environment: str | None = None):
        env_path = Path(__file__).parent.parent / ".env"
        load_dotenv(env_path)

        self.env = self._normalize_environment(environment or os.getenv("TEST_ENV", "dev"))
        self._load_config()

    def _normalize_environment(self, env_name: str) -> str:
        """Normalize environment names such as QA or qa to a lowercase identifier."""
        normalized = (env_name or "dev").strip().lower()
        if normalized not in self.VALID_ENVIRONMENTS:
            return "dev"
        return normalized

    def set_environment(self, environment: str) -> None:
        """Update the current environment at runtime."""
        self.env = self._normalize_environment(environment)
        self._load_config()

    def _load_config(self):
        """Load configuration based on current environment."""
        self.env_path = Path(__file__).parent.parent / ".env"
        self.base_url = os.getenv(f"{self.env.upper()}_BASE_URL")
        self.username = os.getenv(f"{self.env.upper()}_USERNAME")
        self.password = os.getenv(f"{self.env.upper()}_PASSWORD")
        self.logged_in_username = os.getenv("LOGGED_IN_USERNAME", "")
        self.vacancy_name = os.getenv("VACANCY_NAME", "Automation QA Vacancy")
        self.browser = os.getenv("BROWSER", "chromium")
        self.headless = os.getenv("HEADLESS", "false").lower() == "true"
        self.slow_mo = int(os.getenv("SLOW_MO", "0"))
        self.screenshot_on_failure = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
        self.video_on_failure = os.getenv("VIDEO_ON_FAILURE", "true").lower() == "true"
        self.trace_on_failure = os.getenv("TRACE_ON_FAILURE", "true").lower() == "true"

    def save_logged_in_username(self, username: str) -> None:
        """Store the latest authenticated profile name in .env."""
        self._save_env_value("LOGGED_IN_USERNAME", username)
        self.logged_in_username = username

    def save_vacancy_name(self, vacancy_name: str) -> None:
        """Store the latest unique vacancy name in .env."""
        self._save_env_value("VACANCY_NAME", vacancy_name)
        self.vacancy_name = vacancy_name

    def _save_env_value(self, key: str, value: str) -> None:
        """Update one environment setting while preserving the .env file."""
        lines = self.env_path.read_text(encoding="utf-8").splitlines()
        setting = f"{key}={value}"

        for index, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[index] = setting
                break
        else:
            lines.append(setting)

        self.env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        os.environ[key] = value

    @property
    def current_env(self) -> str:
        """Return current environment name."""
        return self.env


# Singleton instance
config = ConfigReader()