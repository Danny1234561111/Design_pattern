import unittest
from Src.Core.common import common
from Src.reposity import reposity

class TestReposity(unittest.TestCase):

    def setUp(self):
        self.repo = reposity()
        self.repo.initialize()

    def test_initialization_creates_keys(self):
        # Проверяем, что после инициализации все ключи присутствуют в __data
        self.assertIn(reposity.range_key(), self.repo.data)
        self.assertIn(reposity.group_key(), self.repo.data)
        self.assertIn(reposity.nomenclature_key(), self.repo.data)
        self.assertIn(reposity.receipt_key(), self.repo.data)

    def test_keys_method_returns_correct_keys(self):
        # Проверяем, что метод keys возвращает правильные ключи
        expected_keys = [
            reposity.group_key(),
            reposity.nomenclature_key(),
            reposity.range_key(),
            reposity.receipt_key()
        ]
        self.assertListEqual(reposity.keys(), expected_keys)

    def test_data_initialization_empty_lists(self):
        # Проверяем, что после инициализации все списки в __data пусты
        for key in reposity.keys():
            self.assertEqual(self.repo.data[key], [])

if __name__ == '__main__':
    unittest.main()