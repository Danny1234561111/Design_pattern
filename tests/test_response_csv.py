import unittest
from src.core.exceptions import ParamException, WrongTypeException
from src.logics.response_csv import ResponseCsv
from src.models.measure_unit_model import MeasureUnitModel
from src.models.nomenclature_group_model import NomenclatureGroupModel
from src.utils import get_properties


class TestResponseCsv(unittest.TestCase):

    # Проверка формирования CSV из модели группы номенклатуры
    def test_responsecsv_build_create_csv_from_nomenclaturegroup_model_not_none(self):
        # Подготовка
        response = ResponseCsv()
        entity = NomenclatureGroupModel("test")
        data = [entity]
        # Действие
        result = response.build(data)
        # Проверка
        assert result is not None

        rows = result.split("\n")
        head = rows[0]
        props = get_properties(entity)
        props_head = ResponseCsv.delimitter.join(props)
        assert head == props_head
    
    # Проверка формирования CSV из нескольких моделей единиц измерения
    def test_responsecsv_build_create_csv_from_measureunit_models_not_none(self):
        # Подготовка
        response = ResponseCsv()
        data = [MeasureUnitModel(1, "гр"), MeasureUnitModel(1, "мл")]
        # Действие
        result = response.build(data)
        # Проверка
        assert result is not None
        
        rows = result.split("\n")
        assert len(rows) == len(data) + 1
    
    # Метод build() выбрасывает исключение при передаче пустого списка
    def test_responsecsv_build_build_from_empty_list_raises_param_exception(self):
        # Подготовка
        response = ResponseCsv()
        data = []
        # Действие и проверка
        with self.assertRaises(ParamException):
            response.build(data)

    # Метод build() выбрасывает исключение при передаче списка из моделей
    # разных типов
    def test_responsecsv_build_build_from_different_models_raises_wrongtype(self):
        # Подготовка
        response = ResponseCsv()
        data = [MeasureUnitModel(1, "гр"), NomenclatureGroupModel("группа")]
        # Действие и проверка
        with self.assertRaises(WrongTypeException):
            response.build(data)


if __name__ == "__main__":
    unittest.main()
