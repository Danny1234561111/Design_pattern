import re
class CompanyModel:
    __name:str=""
    __inn:str=""
    __account:str=""
    __correspondent_account: str = ""
    __bic:str =""
    __type_of_ownership:str=""

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if isinstance(value, str):
            if value.strip() != "":
                self.__name = value.strip()
            else:
                raise ValueError("name не должно быть пустым")
        else:
            raise ValueError("name должно быть строкой")

    @property
    def inn(self) -> str:
        return self.__inn

    @inn.setter
    def inn(self, value: str | int):
        if isinstance(value, (str, int)):
            value_str = str(value).strip()
            if len(value_str) == 12:
                if re.match(r"^\d{12}$", value_str):
                    self.__inn = value_str
                else:
                    raise ValueError("ИНН должен состоять только из цифр")
            else:
                raise ValueError("ИНН должен иметь длину 12 символов, а сейчас",len(value_str))
        else:
            raise TypeError("ИНН должно быть строкой или числом")

    @property
    def account(self) -> str:
        return self.__account

    @account.setter
    def account(self, value: str | int):
        if isinstance(value, (str, int)):
            value_str = str(value).strip()
            if re.match(r"^\d{11}$", value_str):
                self.__account = value_str
            else:
                raise ValueError("Расчетный счет должен состоять из 11 цифр")
        else:
            raise TypeError("Расчетный счет должен быть строкой или числом")

    @property
    def correspondent_account(self) -> str:
        return self.__correspondent_account

    @correspondent_account.setter
    def correspondent_account(self, value: str | int):
        if isinstance(value, (str, int)):
            value_str = str(value).strip()
            if re.match(r"^\d{11}$", value_str):
                self.__correspondent_account = value_str
            else:
                raise ValueError("Корреспондентский счет должен состоять из 11 цифр")
        else:
            raise TypeError("Корреспондентский счет должен быть строкой или числом")

    @property
    def bic(self) -> str:
        return self.__bic

    @bic.setter
    def bic(self, value: str | int):
        if isinstance(value, (str, int)):
            value_str = str(value).strip()
            if len(value_str) == 9 and re.match(r"^\d{9}$", value_str):  # БИК должен состоять из 9 цифр
                self.__bic = value_str
            else:
                raise ValueError("БИК должен состоять из 9 цифр")
        else:
            raise TypeError("БИК должен быть строкой или числом")

    @property
    def type_of_ownership(self) -> str:
        return self.__type_of_ownership

    @type_of_ownership.setter
    def type_of_ownership(self, value: str):
        if isinstance(value, str):
            value_str = value.strip()
            if value_str != None and len(value_str) <= 3:  # Добавлена проверка длины
                self.__type_of_ownership = value_str
            elif value_str == "":
                raise ValueError("Тип собственности не должен быть пустым")
            else:
                raise ValueError("Тип собственности не должен быть больше 5 символов")
        else:
            raise TypeError("Тип собственности должен быть строкой")


