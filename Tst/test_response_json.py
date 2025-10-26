import unittest
import json
from Src.Logics.response_json import response_json
from Src.Models.group_model import group_model
from Src.Core.common import common


class TestResponseJSON(unittest.TestCase):

    def test_response_json_create_from_items(self):
        response = response_json()
        entity = group_model.create("Test group")
        data = [entity]
        result = response.create("json", data)
        self.assertIsNotNone(result)
        json_data = json.loads(result)
        self.assertIsInstance(json_data, list)
        self.assertEqual(len(json_data), 1)
        self.assertIsInstance(json_data[0], dict)  # Проверяем, что элемент списка - словарь
        self.assertIn("name", json_data[0])       # Проверяем, что есть поле "name"
        self.assertEqual(json_data[0]["name"], "Test group") # Проверяем значение "name"

    def test_response_json_to_dict(self):
        response = response_json()
        entity = group_model.create("Test group")
        data = [entity]
        dict_result = response.to_dict(data)  # Получаем dict напрямую
        self.assertIsInstance(dict_result, list)
        self.assertEqual(len(dict_result), 1) # Проверяем длину Python-объекта (списка)
        self.assertIsInstance(dict_result[0], dict)  # Проверяем, что элемент списка - словарь
        self.assertIn("name", dict_result[0])       # Проверяем, что есть поле "name"
        self.assertEqual(dict_result[0]["name"], "Test group") # Проверяем значение "name"

if __name__ == '__main__':
    unittest.main()
