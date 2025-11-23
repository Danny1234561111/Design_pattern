import time
import json
import random
import os
import unittest
from datetime import date, timedelta
from src.singletons.start_service import StartService
from src.logics.osd_tbs import OsdTbs

def generate_test_data():
    """Генерирует test_data.json с 1000 транзакциями"""
    
    # Создаем фиксированные номенклатуры с их единицами измерения
    nomenlatures = []
    for i in range(1, 51):
        measure_unit = random.choice(["штука", "грамм", "литр"])
        nomenlatures.append({
            "name": f"Товар_{i}_{measure_unit}",  # Добавляем единицу в имя для ясности
            "group": "ингредиенты",
            "measure_unit": measure_unit
        })
    
    test_data = {
        "models": {
            "measure_units": [
                {"name": "штука", "base_unit": None, "coefficient": 1},
                {"name": "грамм", "base_unit": None, "coefficient": 1},
                {"name": "литр", "base_unit": None, "coefficient": 1}
            ],
            "nomenclature_groups": [
                {"name": "ингредиенты"}
            ],
            "nomenlatures": nomenlatures,
            "storages": [
                {"name": "Склад", "address": "г. Тестовый"}
            ],
            "transactions": []
        }
    }
    
    # Создаем словарь для быстрого доступа к единицам измерения номенклатур
    nom_units = {nom["name"]: nom["measure_unit"] for nom in nomenlatures}
    
    # Генерируем транзакции с правильными единицами измерения
    for i in range(1, 1001):
        nom_name = random.choice(list(nom_units.keys()))
        measure_unit = nom_units[nom_name]  # Используем ту же единицу, что и у номенклатуры
        
        transaction = {
            "name": f"Транзакция_{i}",
            "datetime": (date(2024, 1, 1) + timedelta(days=random.randint(0, 364))).strftime("%Y-%m-%d"),
            "nomenclature_name": nom_name,
            "storage_name": "Склад",
            "count": random.randint(-100, 100),
            "measure_unit_name": measure_unit  # Та же единица, что у номенклатуры
        }
        test_data["models"]["transactions"].append(transaction)
    
    file_path = "test_data.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Создано: {len(test_data['models']['transactions'])} транзакций")
    return file_path

class TestPerformance(unittest.TestCase):
    
    def test_calculate_ost_performance(self):
        """Тест времени выполнения calculate_ost с 1000 транзакциями"""
        # Создаем данные
        test_file = generate_test_data()
        
        try:
            # Загружаем сервис
            service = StartService()
            service.start(test_file)
            
            print(f"📊 Загружено транзакций: {len(service.transactions)}")
            
            # Замер времени
            start_time = time.time()
            
            headers, rows, work_trans, data_dict = OsdTbs.calculate_ost(
                block_date=date(2024, 6, 1),
                start_service=service
            )
            
            execution_time = time.time() - start_time
            
            # Вывод результатов
            print(f"✅ Результаты:")
            print(f"⏱️  Время выполнения: {execution_time:.3f} секунд")
            print(f"📊 Получено строк: {len(rows)}")
            print(f"🔄 Обработано транзакций(после даты блокировки): {len(work_trans)}")
            
            # Проверка
            self.assertLess(execution_time, 10.0)
            
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

if __name__ == "__main__":
    unittest.main()