import unittest
import json
import os
from unittest.mock import patch, mock_open

from Src.Core.response_format import ResponseFormat
from Src.Models.settings_model import settings_model
from Src.Models.company_model import company_model
from Src.settings_manager import settings_manager
from Src.Core.validator import operation_exception

class TestSettingsManager(unittest.TestCase):

    def setUp(self):
        # Create a settings manager instance for each test
        self.settings_manager = settings_manager.new() #Fixed: Use the singleton getter
        self.settings_manager.__instance = None  # Resetting the singleton, careful!

    def tearDown(self):
        # Clean up after each test (e.g., remove temporary files)
        if hasattr(self, 'temp_file_path') and os.path.exists(self.temp_file_path):
            os.remove(self.temp_file_path)
        settings_manager.__instance = None #Clean up singleton

    def test_file_name_setter_valid(self):
        # Create a temporary file
        self.temp_file_path = "temp_settings.json"
        with open(self.temp_file_path, "w") as f:
            json.dump({}, f)

        # Set the file name
        self.settings_manager.file_name = self.temp_file_path

        # Assert that the file name is set correctly
        self.assertEqual(self.settings_manager.file_name, self.temp_file_path)

    def test_file_name_setter_invalid(self):
        # Assert that FileNotFoundError is raised when the file does not exist
        with self.assertRaises(FileNotFoundError):
            self.settings_manager.file_name = "nonexistent_file.json"

    def test_settings_setter_valid(self):
        # Create a valid settings_model instance
        valid_settings = settings_model(response_format=ResponseFormat.JSON)

        # Set the settings
        self.settings_manager.settings = valid_settings

        # Assert that the settings are set correctly
        self.assertEqual(self.settings_manager.settings, valid_settings)

    def test_load_valid_file(self):
        # Create a temporary settings file with valid JSON data
        self.temp_file_path = "temp_settings.json"
        valid_settings = {"company": {"name": "Test Company", "industry": "Software"}}
        with open(self.temp_file_path, "w") as f:
            json.dump(valid_settings, f)

        # Load the settings from the file
        result = self.settings_manager.load(self.temp_file_path)

        # Assert that the loading was successful