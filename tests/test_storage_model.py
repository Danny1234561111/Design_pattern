import unittest
from src.models.storage_model import StorageModel


class TestStorageModel(unittest.TestCase):
    
    # Проверка на сравнение двух разных моделей склада
    def test_storagemodel_eq_compare_models_not_returns_false(self):
        # Подготовка
        storage1 = StorageModel()
        storage2 = StorageModel()
        # Проверка
        assert storage1 != storage2

    # Проверка на сравнение двух моделей склада с одинаковым ID
    def test_storagemodel_eq_compare_models_with_same_id_returns_true(self):
        # Подготовка
        storage1 = StorageModel()
        storage2 = StorageModel()
        storage2.unique_code = storage1.unique_code
        # Проверка
        assert storage1 == storage2


if __name__ == "__main__":
    unittest.main()
