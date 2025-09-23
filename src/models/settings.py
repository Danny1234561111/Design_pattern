from src.models.company_models import CompanyModel
class Settings:
    __company: CompanyModel =  CompanyModel()

    def __init__(self):
        self.__company = CompanyModel()

    @property
    def company(self) -> CompanyModel:
        return self.__company

    @company.setter
    def company(self, value: CompanyModel | None):
        if isinstance(value, CompanyModel) or value is None:
            self.__company = value
        else:
            raise ValueError("Ожидается экземпляр CompanyModel")