
import unittest
import json
import os
import shutil
import tempfile
from datetime import date
from unittest.mock import patch, MagicMock

# Для тестирования FastAPI приложения, используя TestClient
from fastapi.testclient import TestClient

# Импортируем ваше FastAPI приложение и зависимости
from main import app, service_instance, settings_manager_instance, settings_file, Repository
from src.singletons.repository import StockItem # Если у вас есть такой класс в репозитории

class TestFastAPIApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Выполняется один раз перед всеми тестами в этом классе
        # Инициализируем сервисы, как это делается в main.py
        # settings_manager_instance.load(settings_file) # Может быть не нужно для юнит-тестов
        # service_instance.start(settings_file) # Это может загрузить реальные данные, мокируйте если нужно
        
        # Мы используем TestClient для FastAPI, он запускает приложение в памяти
        cls.client = TestClient(app)

        # Создаем временную директорию для экспорта данных
        cls.temp_dir = tempfile.mkdtemp()
        # Патчим Path("data_exports") так, чтобы она указывала на нашу временную директорию
        cls.patch_path = patch('main.Path', new=lambda p: Path(cls.temp_dir) / p)
        cls.patch_path.start()


    @classmethod
    def tearDownClass(cls):
        # Выполняется один раз после всех тестов в этом классе
        # Удаляем временную директорию
        shutil.rmtree(cls.temp_dir)
        cls.patch_path.stop()


    def setUp(self):
        # Выполняется перед каждым тестом
        # Сбросим состояние репозитория или мокируем его для каждого теста
        # Это важно для изоляции тестов
        
        # Мокируем `repository.data` для каждого теста
        self.mock_repo_data = {
            Repository.recipes_key: {
                "recipe1": {"id": "recipe1", "name": "Тестовый Рецепт 1"},
                "recipe2": {"id": "recipe2", "name": "Тестовый Рецепт 2"},
            },
            Repository.measure_units_key: {
                "unit1": {"id": "unit1", "name": "шт."},
                "unit2": {"id": "unit2", "name": "кг"},
            },
            Repository.nomenclatures_key: {
                "nom1": {"id": "nom1", "name": "Товар А"},
                "nom2": {"id": "nom2", "name": "Товар Б"},
            },
            Repository.nomenclature_groups_key: {
                "group1": {"id": "group1", "name": "Группа 1"},
            },
            "model_type_A": {"itemA": {"value": 1}},
            "model_type_B": {"itemB": {"value": 2}},
        }
        
        # Мокируем `Repository.keys()`
        self.patch_repo_keys = patch('main.Repository.keys', return_value=list(self.mock_repo_data.keys()))
        self.patch_repo_keys.start()

        # Мокируем `service_instance.repository.data`
        self.patch_service_repo_data = patch('main.service_instance.repository.data', new=self.mock_repo_data)
        self.patch_service_repo_data.start()

        # Мокируем `service_instance.repository.get`
        self.mock_get_method = MagicMock(side_effect=lambda unique_code: self._mock_repository_get(unique_code))
        self.patch_service_repo_get = patch('main.service_instance.repository.get', new=self.mock_get_method)
        self.patch_service_repo_get.start()

        # Мокируем `service_instance.repository.get_stock_data`
        self.mock_get_stock_data = MagicMock(return_value=[
            StockItem(initial_balance=10.0, nomenclature="Апельсины", measure_unit="кг", income=5.0, expense=2.0, final_balance=13.0),
            StockItem(initial_balance=20.0, nomenclature="Яблоки", measure_unit="шт", income=10.0, expense=5.0, final_balance=25.0),
        ])
        self.patch_service_repo_get_stock_data = patch('main.service_instance.repository.get_stock_data', new=self.mock_get_stock_data)
        self.patch_service_repo_get_stock_data.start()


    def tearDown(self):
        # Выполняется после каждого теста
        # Останавливаем все патчи
        self.patch_repo_keys.stop()
        self.patch_service_repo_data.stop()
        self.patch_service_repo_get.stop()
        self.patch_service_repo_get_stock_data.stop()


    def _mock_repository_get(self, unique_code: str):
        # Вспомогательная функция для мокирования get()
        for data_dict in self.mock_repo_data.values():
            if unique_code in data_dict:
                return data_dict[unique_code]
        return None

    # --- Тесты для /api/status ---
    def test_status(self):
        response = self.client.get("/api/status")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "success")

    # --- Тесты для /api/responses/formats ---
    def test_get_response_formats(self):
        response = self.client.get("/api/responses/formats")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertIn("json", response.json())

    # --- Тесты для /api/responses/models ---
    def test_get_response_models(self):
        response = self.client.get("/api/responses/models")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertIn(Repository.recipes_key, response.json())
        self.assertIn(Repository.measure_units_key, response.json())

    # --- Тесты для /api/responses/build ---
    def test_build_response_success(self):
        response = self.client.get("/api/responses/build?format=json&model=model_type_A")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertIn({"value": 1}, response.json()) # Предполагаем, что build возвращает список данных

    def test_build_response_invalid_format(self):
        response = self.client.get("/api/responses/build?format=invalid&model=model_type_A")
        self.assertEqual(response.status_code, 400)
        self.assertIn("not such format 'invalid'", response.json()["detail"])

    def test_build_response_invalid_model(self):
        response = self.client.get("/api/responses/build?format=json&model=invalid_model")
        self.assertEqual(response.status_code, 400)
        self.assertIn("not such model 'invalid_model'", response.json()["detail"])

    # --- Тесты для /api/recipes ---
    def test_get_recipes_success(self):
        response = self.client.get("/api/recipes")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 2) # Ожидаем 2 рецепта из мока
        self.assertEqual(response.json()[0]["id"], "recipe1")

    # --- Тесты для /api/recipes/{unique_code} ---
    def test_get_recipe_success(self):
        response = self.client.get("/api/recipes/recipe1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], "recipe1")

    def test_get_recipe_not_found(self):
        response = self.client.get("/api/recipes/non_existent_recipe")
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])

    # --- Тесты для /api/osv ---
    def test_get_osv_success(self):
        response = self.client.get("/api/osv?start_date=2023-01-01&end_date=2023-01-31&storage=MainWarehouse")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]["nomenclature"], "Апельсины")
        self.mock_get_stock_data.assert_called_once_with("MainWarehouse", date(2023, 1, 1), date(2023, 1, 31))

    def test_get_osv_invalid_date_format(self):
        response = self.client.get("/api/osv?start_date=invalid-date&end_date=2023-01-31&storage=MainWarehouse")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid date format", response.json()["detail"])

    def test_get_osv_no_data(self):
        self.mock_get_stock_data.return_value = [] # Мокируем, чтобы метод вернул пустой список
        response = self.client.get("/api/osv?start_date=2023-01-01&end_date=2023-01-31&storage=EmptyWarehouse")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    # --- Тесты для /api/data/save ---
    def test_save_data_to_file_success(self):
        test_filename = "test_output.json"
        expected_filepath = Path(self.temp_dir) / "data_exports" / test_filename
        
        response = self.client.post(f"/api/data/save?filename={test_filename}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], f"Data saved successfully to {expected_filepath}")

        self.assertTrue(expected_filepath.exists())
        with open(expected_filepath, 'r', encoding='utf-8') as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, self.mock_repo_data) # Проверяем, что сохранились мокнутые данные

    def test_save_data_to_file_invalid_extension(self):
        response = self.client.post("/api/data/save?filename=test.txt")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Filename must end with .json", response.json()["detail"])

    # --- Тесты для /api/directories ---
    def test_get_directories_success(self):
        response = self.client.get("/api/directories")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(response.json()["measure_units"], self.mock_repo_data[Repository.measure_units_key])
        self.assertEqual(response.json()["nomenclatures"], self.mock_repo_data[Repository.nomenclatures_key])

    def test_get_directories_missing_key(self):
        # Мокируем, что одного из ключей нет
        del self.mock_repo_data[Repository.measure_units_key]
        
        response = self.client.get("/api/directories")
        self.assertEqual(response.status_code, 200) # get().get(key, {}) обрабатывает отсутствие
        self.assertEqual(response.json()["measure_units"], {}) # Ожидаем пустой словарь


if __name__ == '__main__':
    unittest.main()

