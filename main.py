import uvicorn
from fastapi import FastAPI,HTTPException
from fastapi.responses import HTMLResponse
from src.core.response_format import ResponseFormat
from src.core.http_responses import (TextResponse, JsonResponse, ErrorResponse,
                                     FormatResponse)
from src.logics.factory_entities import FactoryEntities
from src.logics.factory_converters import FactoryConverters
from src.logics.osd_tbs import OsdTbs
from src.logics.tbs_line import TbsLine
from src.singletons.repository import Repository
from src.singletons.start_service import StartService
from src.singletons.settings_manager import SettingsManager
from pathlib import Path 
from fastapi import Query 
from datetime import date
from typing import List,Dict
from src.dtos.filter_sorting_dto import filter_sorting_dto


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

@app.get("/api/storages")
def get_storages():
    """Получить список всех ID хранилищ."""
    try:
        storage_key = Repository.storages_key
        storages_data = start_service.repository.data[storage_key]
        storage_ids = list(storages_data.keys()) #Получаем ключи (ID) из словаря
        return JsonResponse(storage_ids)
    except KeyError:
        raise HTTPException(status_code=500, detail=f"Storage key '{Repository.storages_key}' not found in repository data.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
@app.post("/api/tbs/{storage_id}")
def get_tbs(start_date: date,end_date: date, storage_id: str, filters: dict = None):
    """
    Таблица оборотно-сальдовой ведомости (Trial Balance Sheet, TBS)
    - `storage_code`: уникальный код склада
    - `start`: начальная дата отчёта
    - `end`: дата окончания отчёта
    """
    if "filters" not in filters:
        filters["filters"] = None
    filters = filter_sorting_dto(filters["filters"])
    storage = start_service.repository.get(unique_code=storage_id)
    if storage is None:
        return ErrorResponse(f"Storage with code '{storage_id}' is null")
    
    if start_date >= end_date:
        return ErrorResponse(f"End date must be later than start date")
    
    headers,display_data_rows = OsdTbs.calculate(storage_id, start_date, end_date, start_service,filters)

    # Теперь мы получаем заголовки и данные для отображения здесь, в эндпоинте

    html_table_builder = factory_entities.create(ResponseFormat.HTMLTABLE)
    final_html = html_table_builder.build(headers=headers, data=display_data_rows,name = "оборотно-сальдовой ведомости") 
    

    return HTMLResponse(
        final_html
    )


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
    transactions = list(start_service.transactions.values())

    return JsonResponse(transactions)



@app.get("/api/block_date")
def get_block_date():
    headers = start_service.repository.headers
    display_data_rows = start_service.repository.turnovers_history

    # Теперь мы получаем заголовки и данные для отображения здесь, в эндпоинте

    html_table_builder = factory_entities.create(ResponseFormat.HTMLTABLE)
    final_html = html_table_builder.build(headers=headers, data=display_data_rows,name = "Остатки на контрольную дату") 
    

    return HTMLResponse(
        final_html
    )
@app.post("/api/block_date_new")
def post_block_date(new_date: date = Query(...)):
    start_service.convert_ost(new_date)
    headers = start_service.repository.headers
    display_data_rows = start_service.repository.turnovers_history

    # Теперь мы получаем заголовки и данные для отображения здесь, в эндпоинте

    html_table_builder = factory_entities.create(ResponseFormat.HTMLTABLE)
    final_html = html_table_builder.build(headers=headers, data=display_data_rows,name = f"остатков на {new_date}") 
    

    return HTMLResponse(
        final_html
    )

@app.get("/api/ost/{new_date}")
def search_ost_date(new_date: date):
    headers,display_data_rows = OsdTbs.calculate_new_ost(new_date,start_service)

    # Теперь мы получаем заголовки и данные для отображения здесь, в эндпоинте

    html_table_builder = factory_entities.create(ResponseFormat.HTMLTABLE)
    final_html = html_table_builder.build(headers=headers, data=display_data_rows,name = f"остатков на {new_date}") 
    

    return HTMLResponse(
        final_html
    )




if __name__ == "__main__":
    settings_manager.load(settings_file)
    start_service.start(settings_file)
    uvicorn.run(app=app,
                host="localhost",
                port=8082)