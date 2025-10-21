from Src.Core.validator import validator
from Src.Core.entity_model import entity_model

###############################################
# Модель организации
class company_model(entity_model):
    __inn: int = 0
    __bic: int = 0
    __corr_account: int = 0
    __account: int = 0
    __ownership: str = ""

    # ИНН : 12 симв
    # Счет 11 симв
    # Корреспондентский счет 11 симв
    # БИК 9 симв
    # Наименование
    # Вид собственности 5 симв

    # ИНН
    @property
    def inn(self) -> int:
        return self.__inn

    @inn.setter
    def inn(self, value: int):
        if isinstance(value, int):
            validator.validate(value, int, 12)
            self.__inn = value
        else:
            raise ValueError("ИНН должно быть целым числом")

    # КПП (опечатка, должно быть КПП, а не БИК)
    @property
    def bic(self) -> int:
        return self.__bic

    @bic.setter
    def bic(self, value: int):
        if isinstance(value, int):
            validator.validate(value, int, 9)
            self.__bic = value
        else:
            raise ValueError("БИК должно быть целым числом")

    # Корреспондентский счет
    @property
    def corr_account(self) -> int:
        return self.__corr_account

    @corr_account.setter
    def corr_account(self, value: int):
        if isinstance(value, int):
            validator.validate(value, int, 11)
            self.__corr_account = value
        else:
            raise ValueError("Корр. счет должен быть целым числом")

    @property
    def account(self) -> int:
        return self.__account

    @account.setter
    def account(self, value: int):
        if isinstance(value, int):
            validator.validate(value, int, 11)
            self.__account = value
        else:
            raise ValueError("Счет должно быть целым числом")

    @property
    def ownership(self) -> str:
        return self.__ownership

    @ownership.setter
    def ownership(self, value: str):
        if isinstance(value, str):
            validator.validate(value, str, 5)
            self.__ownership = value.strip()
        else:
            raise ValueError("Вид собственности должен быть строкой")
