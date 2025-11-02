import unittest
from src.core.abstract_model import AbstractModel


class TestAbstractModel(unittest.TestCase):

    # Инициализация абстрактной модели
    def test_abstractmodel_init_init_abstract_model_raise_type_error(self):
        # Проверка
        with self.assertRaises(TypeError):
            AbstractModel()


if __name__ == "__main__":
    unittest.main()
