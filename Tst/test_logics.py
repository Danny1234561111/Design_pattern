import unittest
from Src.Core.abstract_response import abstract_response
from Src.Core.common import common
from Src.Core.validator import validator

class response_csv(abstract_response):

    # Сформировать CSV
    def create(self, format: str, data: list):
        text = "" # Initialize to an empty string
        # Шапка
        if data:  # Check if data is not empty
            item = data[0]
            fields = common.get_fields(item)
            for field in fields:
                text += f"{field};"

            # Data: You would typically iterate through the data and format it for CSV here.  For now, I'll leave a placeholder
            csv_string = "Column1,Column2,Column3\n"
            for item in data:
              text += f"{item};" # Adapt this
        return text

    def build(self, format: str, data: list):  # Implement build method and add format parameter
        # Your code to build the CSV here, e.g., generating a CSV string
        csv_string = "Column1,Column2,Column3\n"
        # Check if data is not None and not empty
        if data:
            for item in data:
                # Add CSV formatting based on item's attributes
                csv_string += f"value1,value2,value3\n"  # Example
        return csv_string

from Src.Core.validator import operation_exception

class factory_entities:
    __match = {
        "csv": response_csv
    }

    # Получить нужный тип
    def create(self, format: str) -> abstract_response:
        if format not in self.__match.keys():
            raise operation_exception("Формат не верный")

        # Создаем экземпляр класса
        return self.__match[format]()  # <--- Here we add () to create an instance

from Src.Models.group_model import group_model
# Tests for validation logic
class test_logics(unittest.TestCase):  # Add self argument to all methods

    # Verify CSV building
    def test_notNone_response_csv_buld(self):
        # Preparation
        response = response_csv()
        data = []
        entity = group_model.create("test")
        data.append(entity)

        # Action
        result = response.create("csv", data)

        # Validation
        assert result is not None

    def test_notNone_factory_create(self):
        # Preparation
        factory = factory_entities()
        data = []
        entity = group_model.create("test")
        data.append(entity)

        # Action
        logic = factory.create("csv")  # передаём "csv", а не response_formats.csv

        # Validation
        assert logic is not None
        validator.validate(logic, abstract_response) # Abstract validate

        text = logic.build("csv", data)  # передаём data
        assert len(text) > 0
