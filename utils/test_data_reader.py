"""Test data reader for JSON test data files."""

import json
from pathlib import Path
from typing import Any, Dict


class TestDataReader:
    """Reads test data from JSON files."""
    
    def __init__(self, data_dir: str = "test_data"):
        self.data_dir = Path(__file__).parent.parent / data_dir
    
    def load_json(self, filename: str) -> Dict[str, Any]:
        """Load JSON test data file."""
        file_path = self.data_dir / filename
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    def get_user(self, user_type: str = "valid_user") -> Dict[str, str]:
        """Get user credentials from users.json."""
        data = self.load_json("users.json")
        return data.get(user_type, {})


# Singleton instance
test_data = TestDataReader()