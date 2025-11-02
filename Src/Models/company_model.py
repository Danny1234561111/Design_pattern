from typing import Optional
from src.core.abstract_model import AbstractModel
from src.core.validator import Validator as vld


"""Модель компании

Предназначена для хранения данных об организации
"""
class CompanyModel(AbstractModel):
    # Наименование организации (наследуется от AbstractModel)

    # ИНН (12 символов)
    __inn: Optional[int] = None

    # Счёт (11 символов)
    __account: Optional[int] = None

    # Корреспондентский счет (11 символов)
    __corr_account: Optional[int] = None

    # БИК (9 символов)
    __bic: Optional[int] = None

    # Вид собственности (5 символов)
    __ownership: str = ""

    def __init__(self):
        super().__init__()
    
    """ИНН организации"""
    @property
    def inn(self) -> Optional[int]:
        return self.__inn
    
    @inn.setter
    def inn(self, value: Optional[int]):
        vld.is_positive_int(value=value,
                            field_name="inn",
                            could_be_none=True,
                            len_=12,
                            strictly_len=True)
        self.__inn = value

    """Номер счёта компании"""
    @property
    def account(self) -> Optional[int]:
        return self.__account
    
    @account.setter
    def account(self, value: Optional[int]):
        vld.is_positive_int(value=value,
                            field_name="account",
                            could_be_none=True,
                            len_=11,
                            strictly_len=True)
        self.__account = value

    """Корреспондентский счёт"""
    @property
    def corr_account(self) -> Optional[int]:
        return self.__corr_account
    
    @corr_account.setter
    def corr_account(self, value: Optional[int]):
        vld.is_positive_int(value=value,
                            field_name="corr_account",
                            could_be_none=True,
                            len_=11,
                            strictly_len=True)
        self.__corr_account = value

    """БИК компании"""
    @property
    def bic(self) -> Optional[int]:
        return self.__bic
    
    @bic.setter
    def bic(self, value: Optional[int]):
        vld.is_positive_int(value=value,
                            field_name="bic",
                            could_be_none=True,
                            len_=9,
                            strictly_len=True)
        self.__bic = value

    """Вид собственности"""
    @property
    def ownership(self) -> str:
        return self.__ownership
    
    @ownership.setter
    def ownership(self, value: str):
        vld.is_str(value, "ownership", len_=5)
        self.__ownership = value
