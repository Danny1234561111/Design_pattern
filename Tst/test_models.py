# import unittest
# import os
# import json
# import uuid
# from Src.settings_manager import settings_manager
# from Src.Models.company_model import company_model
# from Src.Models.storage_model import storage_model
# from Src.Models.nomenclature_model import nomenclature_model
# from Src.Core.validator import argument_exception  # Добавляем импорт исключения


# class TestModels(unittest.TestCase):

#     def setUp(self):
#         """Настройка перед каждым тестом."""
#         self.test_file_path = os.path.join("./Tst", "test_settings.json")
#         self.manager = settings_manager()

#     def tearDown(self):
#         """Очистка после каждого теста."""
#         if os.path.exists(self.test_file_path):
#             os.remove(self.test_file_path)

#     def create_test_file(self, content):
#         """Создает временный файл с настройками."""
#         os.makedirs("./Tst", exist_ok=True)
#         with open(self.test_file_path, "w") as f:
#             json.dump(content, f)

#     # Провери создание основной модели
#     # Данные после создания должны быть пустыми
#     def test_empty_createmodel_companymodel(self):
#         # Подготовка
#         model = company_model()

#         # Проверки
#         self.assertEqual(model.name, "", "Имя компании должно быть пустым при создании")

#     # Проверить создание основной модели
#     # Данные меняем. Данные должны быть
#     def test_notEmpty_createmodel_companymodel(self):
#         # Подготовка
#         model = company_model()

#         # Действие
#         model.name = "test"

#         # Проверки
#         self.assertNotEqual(model.name, "", "Имя компании не должно быть пустым после изменения")

#     # Проверить создание основной модели
#     # Данные загружаем через json настройки
#     def test_load_createmodel_companymodel(self):
#         # Подготовка
#         test_settings = {"company": {"name": "Test Company", "inn": 123}}
#         self.create_test_file(test_settings)

#         self.manager.file_name = self.test_file_path

#         # Действие
#         result = self.manager.load()

#         # Проверки
#         self.assertTrue(result, "Загрузка настроек должна быть успешной")
#         self.assertEqual(self.manager.settings.company.name, "Test Company", "Имя компании должно быть загружено из файла")
#         self.assertEqual(self.manager.settings.company.inn, 123, "ИНН должен быть загружен из файла")

#     # Тесты для response_format
#     def test_load_response_format(self):
#         test_settings = {
#             "company": {"name": "Test Company"},            "response_format": "Markdown"  # Допустим, есть фабрика для Markdown
#         }
#         self.create_test_file(test_settings)
#         self.manager.file_name = self.test_file_path
#         self.manager.load()
#         self.assertEqual(self.manager.settings.response_format, "MARKDOWN", "Формат ответа должен быть загружен из файла")

    
#     def test_default_response_format(self):
#         self.assertEqual(self.manager.settings.response_format, "CSV", "Формат ответа по умолчанию должен быть CSV")

#     # Проверка на сравнение двух по значению одинаковых моделей
#     def test_equals_storage_model_create(self):
#         # Подготовка
#         id = uuid.uuid4().hex
#         storage1 = storage_model()
#         storage1.unique_code = id
#         storage2 = storage_model()
#         storage2.unique_code = id

#         # Действие
#         # Проверки
#         self.assertEqual(storage1, storage2, "Две модели хранилища с одинаковым unique_code должны быть равны")

#     # Проверить создание номенклатуры и присвоение уникального кода
#     def test_equals_nomenclature_model_create(self):
#         # Подготовка
#         id = uuid.uuid4().hex
#         item1 = nomenclature_model()
#         item1.unique_code = id
#         item2 = nomenclature_model()
#         item2.unique_code = id

#         # Действие
#         # Проверки
#         self.assertEqual(item1, item2, "Две модели номенклатуры с одинаковым unique_code должны быть равны")


# if __name__ == '__main__':
#     unittest.main()