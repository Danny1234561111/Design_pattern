from Src.Core.abstract_dto import abstact_dto

class category_dto(abstact_dto):
    def create(self, data) -> "category_dto":
        super().create(data)  # Вызов метода родителя для установки атрибутов
        return self