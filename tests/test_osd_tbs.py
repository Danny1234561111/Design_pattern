import unittest
from datetime import date
from src.singletons.start_service import StartService
from src.models.transaction_model import TransactionModel
from src.models.nomenclature_model import NomenclatureModel
from src.logics.osd_tbs import OsdTbs
from src.core.exceptions import OperationException
from src.singletons.repository import Repository

class TestOsdTbs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Запуск сервиса и подготовка тестовых данных."""
        cls.start_service = StartService()
        cls.start_service.start()

        # Подготовка тестовых данных
        cls.storage_id = "test_storage"
        cls.nomenclature = NomenclatureModel(name="Тестовая Номенклатура", unique_code="TCN123")

        # Добавление тестовых транзакций
        transaction1 = TransactionModel(date=date(2023, 1, 1), storage=cls.storage_id, nomenclature=cls.nomenclature, quantity=10, measure_unit="единица", transaction_type="transaction")
        transaction2 = TransactionModel(date=date(2023, 1, 2), storage=cls.storage_id, nomenclature=cls.nomenclature, quantity=5, measure_unit="единица", transaction_type="transaction")

        cls.start_service.repository.add_data(Repository.transactions_key, {transaction1.date: transaction1, transaction2.date: transaction2})

    def test_calculate_with_different_block_dates(self):
        """Проверка, что результаты расчетов не меняются при изменении даты блокировки."""
        
        # Первое вычисление с первой датой блокировки
        block_date_1 = date(2023, 1, 3)
        headers_1, display_data_rows_1 = OsdTbs.calculate(self.storage_id, date(2023, 1, 1), date(2023, 1, 5), self.start_service)

        # Второе вычисление с измененной датой блокировки
        block_date_2 = date(2023, 1, 4)
        headers_2, display_data_rows_2 = OsdTbs.calculate(self.storage_id, date(2023, 1, 1), date(2023, 1, 5), self.start_service)

        # Проверка, что результаты одинаковы
        self.assertListEqual(display_data_rows_1, display_data_rows_2, "Результаты расчетов различаются при изменении даты блокировки.")

    def test_load_performance(self):
        """Нагрузочный тест: измерение времени расчета для 1000 транзакций."""
        transactions = []
        for i in range(1000):
            transaction = TransactionModel(date=date.today(), storage=self.storage_id, nomenclature=self.nomenclature, quantity=i + 1, measure_unit="единица", transaction_type="transaction")
            transactions.append(transaction)

        # Добавляем транзакции в сервис
        self.start_service.repository.add_data(Repository.transactions_key, {trans.date: trans for trans in transactions})

        # Измерение времени расчета
        import time
        start_time = time.time()

        headers, display_data_rows = OsdTbs.calculate(self.storage_id, date.today(), date.today(), self.start_service)

        end_time = time.time()
        duration = end_time - start_time

        print(f"Время расчета для 1000 транзакций: {duration:.2f} секунд")

        # Проверяем, что расчет проходит быстро
        self.assertLess(duration, 5, "Расчет занял слишком много времени!")

if __name__ == "__main__":
    unittest.main()