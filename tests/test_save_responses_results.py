import unittest
import pathlib
from src.core.response_format import ResponseFormat
from src.logics.factory_entities import FactoryEntities
from src.singletons.repository import Repository
from src.singletons.start_service import StartService


class TestSaveResponsesResults(unittest.TestCase):

    # Расширения файлов для форматов ответов
    __files_ex: dict = {
        ResponseFormat.CSV: "csv",
        ResponseFormat.MARKDOWN: "md",
        ResponseFormat.JSON: "json",
        ResponseFormat.XML: "xml",
    }
    
    # Путь до файла с тестовыми настройками
    __settings_name: str = "tests/data/settings_models.json"

    # Директория, в которую будут сохраняться файлы
    __save_directory: str = "tests/responses_results/"

    # Объект сервиса
    __start_service: StartService = StartService()

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.__start_service.start(self.__settings_name)

    # Автотест, создающий файлы и сохраняющий в них результаты ответов для
    # разных моделей
    def test_save_results_in_files(self):
        # Создание директории со всеми файлами
        dir_ = pathlib.Path(self.__save_directory)
        dir_.mkdir(exist_ok=True)

        models = Repository.keys()
        factory = FactoryEntities()

        for format in ResponseFormat:
            # Поддиректория с файлами одного формата
            subdir = dir_ / format.name.lower()
            subdir.mkdir(exist_ok=True)
            
            response = factory.create(format)

            for model in models:
                file_path = subdir / f"{model}.{self.__files_ex[format]}"
                file_path.touch(exist_ok=True)
                
                data = self.__start_service.repository.data[model].values()
                result = response.build(list(data))

                with open(file_path, 'w', encoding="utf-8") as file:
                    file.write(result)
                    file.close()


if __name__ == "__main__":
    unittest.main()