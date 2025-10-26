import unittest
from Src.Logics.response_csv import response_csv
from Src.Models.group_model import group_model
from Src.Core.common import common

class TestResponseCSV(unittest.TestCase):

    def test_response_csv_create_from_items(self):
        response = response_csv()
        entity = group_model.create("Test group")
        data = [entity]
        result = response.create("csv", data)
        self.assertIsNotNone(result)
        self.assertIn("Test group", result)

    def test_response_csv_to_dict(self):
        response = response_csv()
        entity = group_model.create("Test group")
        data = [entity]
        dict_result = response.to_dict(data)
        self.assertEqual(len(dict_result), 1)

if __name__ == '__main__':
    unittest.main()