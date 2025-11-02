import unittest
from src.core.exceptions import InvalidValueException, WrongTypeException
from src.models.company_model import CompanyModel


class TestCompanyModel(unittest.TestCase):
    
    # Пустые поля модели компании при инициализации
    def test_companymodel_init_no_fields_sets_fields_empty(self):
        # Подготовка
        model = CompanyModel()
        # Проверка
        assert model.name == ""
        assert model.inn is None
        assert model.account is None
        assert model.corr_account is None
        assert model.bic is None
        assert model.ownership == ""

    # Присваивание полю name невалидных или пустных значений
    def test_companymodel_name_set_name_with_spaces_invalid_value(self):
        # Подготовка
        model = CompanyModel()
        # Проверка
        with self.assertRaises(InvalidValueException):
            model.name = None
        with self.assertRaises(InvalidValueException):
            model.name = " "
        with self.assertRaises(WrongTypeException):
            model.name = 123
    
    # Присваивание полю name валидного значения
    def test_companymodel_name_set_valid_value_name_is_set(self):
        # Подготовка
        model = CompanyModel()
        name = "Danny"
        # Действие
        model.name = name
        # Проверка
        assert model.name == name
    
    # Присваивание полю inn невалидных и пустых значений
    def test_companymodel_inn_set_invalid_value_raises_exceptions(self):
        # Подготовка
        model = CompanyModel()
        # Проверка
        with self.assertRaises(WrongTypeException):
            # 12 символов
            model.inn = "123123123123"
        with self.assertRaises(WrongTypeException):
            # 12 символов
            model.inn = 123123123123.0
        with self.assertRaises(InvalidValueException):
            # 12 символов, отрицательное
            model.inn = -123123123123
        with self.assertRaises(InvalidValueException):
            # 11 символов
            model.inn = 12312312312

    # Присваивание полю inn валидного значения
    def test_companymodel_inn_set_valid_value_inn_is_set(self):
        # Подготовка
        model = CompanyModel()
        inn = 123123123123
        # Действие
        model.inn = inn
        # Проверка
        assert model.inn is not None
        assert model.inn == inn
        assert type(model.inn) is int
    
    # Присваивание полю account невалидных и пустых значений
    def test_companymodel_account_set_invalid_value_raises_exceptions(self):
        # Подготовка
        model = CompanyModel()
        # Проверка
        with self.assertRaises(WrongTypeException):
            # 11 символов
            model.account = "12312312312"
        with self.assertRaises(WrongTypeException):
            # 11 символов
            model.account = 12312312312.0
        with self.assertRaises(InvalidValueException):
            # 11 символов, отрицательное
            model.account = -12312312312
        with self.assertRaises(InvalidValueException):
            # 10 символов
            model.account = 1231231231

    # Присваивание полю account валидного значения
    def test_companymodel_account_set_valid_value_account_is_set(self):
        # Подготовка
        model = CompanyModel()
        account = 12312312312
        # Действие
        model.account = account
        # Проверка
        assert model.account is not None
        assert model.account == account
        assert type(model.account) is int

    # Присваивание полю corr_account невалидных и пустых значений
    def test_companymodel_corr_account_set_invalid_value_raises_exceptions(self):
        # Подготовка
        model = CompanyModel()
        # Проверка
        with self.assertRaises(WrongTypeException):
            # 11 символов
            model.corr_account = "12312312312"
        with self.assertRaises(WrongTypeException):
            # 11 символов
            model.corr_account = 12312312312.0
        with self.assertRaises(InvalidValueException):
            # 11 символов, отрицательное
            model.corr_account = -12312312312
        with self.assertRaises(InvalidValueException):
            # 10 символов
            model.corr_account = 1231231231

    # Присваивание полю corr_account валидного значения
    def test_companymodel_corr_account_set_valid_value_corr_account_is_set(self):
        # Подготовка
        model = CompanyModel()
        corr_account = 12312312312
        # Действие
        model.corr_account = corr_account
        # Проверка
        assert model.corr_account is not None
        assert model.corr_account == corr_account
        assert type(model.corr_account) is int

    # Присваивание полю bic невалидных и пустых значений
    def test_companymodel_bic_set_invalid_value_raises_exceptions(self):
        # Подготовка
        model = CompanyModel()
        # Проверка
        with self.assertRaises(WrongTypeException):
            # 9 символов
            model.bic = "123123123"
        with self.assertRaises(WrongTypeException):
            # 9 символов
            model.bic = 123123123.0
        with self.assertRaises(InvalidValueException):
            # 9 символов, отрицательное
            model.bic = -123123123
        with self.assertRaises(InvalidValueException):
            # 8 символов
            model.bic = 12312312

    # Присваивание полю bic валидного значения
    def test_companymodel_bic_set_valid_value_bic_is_set(self):
        # Подготовка
        model = CompanyModel()
        bic = 123123123
        # Действие
        model.bic = bic
        # Проверка
        assert model.bic is not None
        assert model.bic == bic
        assert type(model.bic) is int
    
    # Присваивание полю ownership невалидных или пустных значений
    def test_companymodel_ownership_set_ownership_with_spaces_invalid_value(self):
        # Подготовка
        model = CompanyModel()
        # Проверка
        with self.assertRaises(InvalidValueException):
            model.ownership = None
        with self.assertRaises(InvalidValueException):
            model.ownership = " "
        with self.assertRaises(WrongTypeException):
            model.ownership = 123
    
    # Присваивание полю ownership валидного значения
    def test_companymodel_ownership_set_valid_value_ownership_is_set(self):
        # Подготовка
        model = CompanyModel()
        ownership = "ОАО"
        # Действие
        model.ownership = ownership
        # Проверка
        assert model.ownership == ownership


if __name__ == "__main__":
    unittest.main()
