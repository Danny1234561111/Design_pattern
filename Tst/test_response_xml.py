import unittest
from Src.Logics.response_xml import response_xml
from Src.Models.group_model import group_model

class TestResponseXML(unittest.TestCase):

    def test_response_xml_create_from_items(self):
        response = response_xml()
        entity = group_model.create("Test group")
        data = [entity]
        result = response.create("xml", data)
        self.assertIsNotNone(result)
        self.assertIn("<name>Test group</name>", result)  # Ищем правильный XML-тег

    def test_response_xml_to_dict(self):
        response = response_xml()
        entity = group_model.create("Test group")
        data = [entity]
        dict_result = response.to_dict(data)
        self.assertEqual(len(dict_result), 1)

if __name__ == '__main__':
    unittest.main()

