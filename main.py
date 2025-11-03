import uvicorn
from fastapi import FastAPI,HTTPException
from fastapi.responses import HTMLResponse
from src.core.response_format import ResponseFormat
from src.core.http_responses import (TextResponse, JsonResponse, ErrorResponse,
                                     FormatResponse)
from src.logics.factory_entities import FactoryEntities
from src.logics.factory_converters import FactoryConverters
from src.singletons.repository import Repository
from src.singletons.start_service import StartService
from src.singletons.settings_manager import SettingsManager
from pathlib import Path 
from fastapi import Query 
from datetime import datetime
from typing import List,Dict

settings_file = "data/settings.json"
start_service = StartService()
settings_manager = SettingsManager()
factory_entities = FactoryEntities()
factory_converters = FactoryConverters()

app = FastAPI()


@app.get("/api/status")
def status():
    """Проверить доступность REST API"""
    return TextResponse("success")


@app.get("/api/responses/formats")
def get_response_formats():
    """Доступные форматы ответов"""
    content = [format.name.lower() for format in ResponseFormat]
    return JsonResponse(content)


@app.get("/api/responses/models")
def get_response_models():
    """Типы моделей, доступные для формирования ответов"""
    content = [key for key in Repository.keys()]
    return JsonResponse(content)


@app.get("/api/responses/build")
def build_response(format: str, model: str):
    """
    Сформировать ответ для моделей в переданном формате:
    - `format`: строковое обозначение формата ответа
    - `model`: строковое обозначения типа моделей
    """
    formats = [format.name.lower() for format in ResponseFormat]
    if format is None:
        return ErrorResponse("param 'format' must be transmitted")
    format = format.lower()
    if format not in formats:
        return ErrorResponse(
            f"not such format '{format}'. Available: {formats}"
        )
    
    model_types = [key for key in Repository.keys()]
    if model is None:
        return ErrorResponse("param 'model' must be transmitted")
    if model not in model_types:
        return ErrorResponse(
            f"not such model '{model}'. Available: {model_types}"
        )

    models = list(start_service.repository.data[model].values())
    result = factory_entities.create(format).build(models)

    return FormatResponse(result, format)


@app.get("/api/recipes")
def get_recipes():
    """Получить список рецептов в формате JSON"""
    key = Repository.recipes_key
    recipes = list(start_service.repository.data[key].values())
    result = factory_converters.convert(recipes)

    return JsonResponse(result)


@app.get("/api/recipes/{unique_code}")
def get_recipe(unique_code: str):
    """
    Получить рецепт в формате JSON по его уникальному коду:
    - `unique_code`: уникальный код рецепта в хранилище
    """
    recipe = start_service.repository.get(unique_code=unique_code)
    result = factory_converters.convert(recipe)

    return JsonResponse(result)


@app.get("/api/osv", response_class=HTMLResponse)
def get_osv(start_date: str, end_date: str, storage: str):
    """
    Получение оборотно-сальдовой ведомости (ОСВ) в формате HTML.
    - `start_date`: дата начала (YYYY-MM-DD)
    - `end_date`: дата окончания (YYYY-MM-DD)
    - `storage`: склад
    """
    try:
        # Преобразуем строки в даты
        start_date_2 = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_2 = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Получаем данные из репозитория (замените на ваш реальный код)
        stock_data: List[StockData] = start_service.repository.get_stock_data(storage, start_date_2, end_date_2)

        # Формируем HTML-таблицу
        html_table = """
        <table border="1">
            <thead>
                <tr>
                    <th>Начальный остаток</th>
                    <th>Номенклатура</th>
                    <th>Единица измерения</th>
                    <th>Приход</th>
                                        <th>Расход</th>
                    <th>Конечный остаток</th>
                </tr>
            </thead>
            <tbody>
        """

        for item in stock_data:
            html_table += f"""
                <tr>
                    <td>{item.initial_balance}</td>
                    <td>{item.nomenclature}</td>
                    <td>{item.measure_unit}</td>
                    <td>{item.income}</td>
                    <td>{item.expense}</td>
                    <td>{item.final_balance}</td>
                </tr>
            """

        html_table += """
            </tbody>
        </table>
        """

        return HTMLResponse(content=html_table)

    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат даты. Используйте YYYY-MM-DD.")
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/api/save") # Используем POST, так как это изменение состояния на сервере
def save_data_to_file(filename: str = Query(...)): # filename как Query параметр
    """
    Сохранить все данные репозитория в файл
    - `filename`: имя выходного файла
    """
    if not filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Filename must end with .json")

    # Пример безопасного пути: сохранение только в предопределенной директории 'data_exports'
    safe_path = Path("data_exports") / filename
    safe_path.parent.mkdir(parents=True, exist_ok=True) # Создать директорию, если ее нет

    try:
        # service_instance вместо start_service
        # (Убедитесь, что `service_instance = StartService()` определено в начале файла)
        repository_data = start_service.repository.data
        # all_keys = list(repository_data.keys())
    
        # # Определяем последний ключ
        # last_key = all_keys[-1]
        
        
        # # Создаем новый словарь, исключая последний ключ
        # result_data = {key: value for key, value in repository_data.items() if key != last_key}
        result = factory_converters.convert(repository_data)
        with open(safe_path, 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=4) # indent=4 для красивого форматирования
        
        return JsonResponse({"message": f"Data saved successfully to {safe_path}"})
    
    except TypeError as te:
        raise HTTPException(status_code=500, detail=f"Data serialization error: {str(te)}. Ensure all objects in repository.data are JSON-serializable.")
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Failed to save data: {str(ex)}")


@app.get("/api/directories")
def get_directories():
    directories = {
        "measure_unit": factory_converters.convert(start_service.repository.data[Repository.measure_unit_key]),
        "nomenclatures": factory_converters.convert(start_service.repository.data[Repository.nomenclatures_key]),
        "nomenclature_groups": factory_converters.convert(start_service.repository.data[Repository.nomenclature_group_key]),
        "storages": factory_converters.convert(start_service.repository.data[Repository.storages_key]),  # Добавлено
        "transactions": factory_converters.convert(start_service.repository.data[Repository.transactions_key]),  # Добавлено
    }
    return JsonResponse(directories)
@app.get("/api/transactions")
def get_transactions():
    key = Repository.transactions_key
    transactions = list(start_service.repository.data[key].values())
    result = [transaction.to_dict() for transaction in transactions]

    return JsonResponse(result)


if __name__ == "__main__":
    settings_manager.load(settings_file)
    start_service.start(settings_file)
    uvicorn.run(app=app,
                host="localhost",
                port=8080)
