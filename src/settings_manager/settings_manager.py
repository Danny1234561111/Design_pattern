from src.models.settings import Settings
from src.models.settings import CompanyModel
import os
import json


class SettingsManager:
    __file_name: str = ""
    def __new__(cls, file_name: str):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SettingsManager, cls).__new__(cls)

        return cls.instance

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.__settings = Settings()
        self.default_settings()

    @property
    def settings(self) -> Settings:
        return self.__settings

    @property
    def file_name(self) -> str:
        return self.__file_name

    @file_name.setter
    def file_name(self, value: str):
        if value.strip() == "":
            return

        if os.path.exists(value):
            self.__file_name = value.strip()

    def load(self):
        if self.__file_name.strip == "":
            raise FileNotFoundError("Не найден файл настроек!")

        try:
            with open(self.__file_name, "r", encoding="utf-8") as f:
                data = json.load(f)

            return self.convert(data)
        except Exception as error:
            print(error)
            return False

    def convert(self, data: dict) -> bool:
        if "company" in data:
            company_data = data["company"]
            self.__settings.company.name = company_data["name"]
            self.__settings.company.account = company_data["account"]
            self.__settings.company.correspondent_account = company_data["correspondent_account"]
            self.__settings.company.BIK = company_data["BIK"]
            self.__settings.company.ownership_type = company_data["ownership_type"]
            self.__settings.company.INN = company_data["INN"]

            return True

        return False

    def default_settings(self):
        self.__settings.company.name = "Киви"
        self.__settings.company.inn = "111122223333"
        self.__settings.company.account = "40702810000"
        self.__settings.company.correspondent_account ="33301719999"
        self.__settings.company.bic = "123456111"
        self.__settings.company.type_of_ownership = "ООО"