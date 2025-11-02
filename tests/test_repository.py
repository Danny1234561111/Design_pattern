import unittest
from src.singletons.repository import Repository


class TestRepository(unittest.TestCase):
    
    # Проверка класса Repository на синглтон
    def test_repository_new_init_repository_twice_is_singltone(self):
        # Подготовка
        repo1 = Repository()
        unique_id = "unique value"
        setattr(repo1, "id", unique_id)
        # Действие
        repo2 = Repository()
        # Проверка
        assert repo1 == repo2
        assert getattr(repo1, "id") == getattr(repo2, "id") == unique_id


if __name__ == "__main__":
    unittest.main()
