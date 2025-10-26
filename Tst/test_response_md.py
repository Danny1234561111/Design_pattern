import unittest
from Src.Logics.response_md import response_md
from Src.Models.group_model import group_model

class TestResponseMD(unittest.TestCase):

    def test_response_md_create_from_items(self):
        response = response_md()
        entity = group_model.create("Test group")
        data = [entity]
        result = response.create("md", data)
        self.assertIsNotNone(result)
        self.assertIn("Test group", result)

    def test_response_md_to_dict(self):
        response = response_md()
        entity = group_model.create("Test group")
        data = [entity]
        dict_result = response.to_dict(data)
        self.assertEqual(len(dict_result), 1)

if __name__ == '__main__':
    unittest.main()