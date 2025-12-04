import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from src.core.response_format import ResponseFormat
from src.core.http_responses import (TextResponse, JsonResponse, ErrorResponse,
                                     FormatResponse)
from src.logics.factory_entities import FactoryEntities
from src.logics.factory_converters import FactoryConverters
from src.logics.osd_tbs import OsdTbs
from src.singletons.start_service import StartService
from src.singletons.settings_manager import SettingsManager
from pathlib import Path 
from fastapi import Query 
from datetime import date, datetime
from typing import List, Dict
from src.dtos.filter_sorting_dto import filter_sorting_dto
from src.logics.reference_service import ReferenceService
from src.core.observe_service import observe_service
from src.core.event_type import event_type
import json
import os
import time
from datetime import datetime as dt

# Импорт логгера
from src.logics.print_service import print_service

settings_file = "data/settings.json"
start_service = StartService()
settings_manager = SettingsManager()
factory_entities = FactoryEntities()
factory_converters = FactoryConverters()
reference_service = ReferenceService()

# Инициализация логгера
logger = print_service()

app = FastAPI()

# Middleware для логирования всех запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Извлекаем информацию о запросе
    request_info = {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "client_ip": request.client.host if request.client else "unknown",
        "user_agent": request.headers.get("user-agent", "")
    }
    
    # Логируем начало запроса
    logger.log_info(f"API Request started: {request.method} {request.url}", {
        "request": request_info,
        "stage": "start"
    })
    
    try:
        response = await call_next(request)
        
        # Логируем успешное завершение
        process_time = time.time() - start_time
        logger.log_info(f"API Request completed: {request.method} {request.url}", {
            "request": request_info,
            "stage": "end",
            "status_code": response.status_code,
            "process_time": f"{process_time:.3f}s"
        })
        
        return response
        
    except Exception as e:
        # Логируем ошибку
        process_time = time.time() - start_time
        logger.log_error(f"API Request error: {request.method} {request.url}", {
            "request": request_info,
            "stage": "error",
            "error": str(e),
            "process_time": f"{process_time:.3f}s"
        })
        raise

@app.get("/api/status")
def status():
    """Проверить доступность REST API"""
    logger.log_debug("Status endpoint called")
    return TextResponse("success")

@app.get("/api/responses/formats")
def get_response_formats():
    """Доступные форматы ответов"""
    logger.log_debug("Response formats endpoint called")
    content = [format.name.lower() for format in ResponseFormat]
    return JsonResponse(content)

@app.get("/api/responses/models")
def get_response_models():
    """Типы моделей, доступные для формирования ответов"""
    logger.log_debug("Response models endpoint called")
    content = [key for key in Repository.keys()]
    return JsonResponse(content)

@app.get("/api/responses/build")
def build_response(format: str, model: str):
    """
    Сформировать ответ для моделей в переданном формате
    """
    logger.log_info(f"Building response: format={format}, model={model}")
    
    formats = [format.name.lower() for format in ResponseFormat]
    if format is None:
        logger.log_error("Format parameter is missing")
        return ErrorResponse("param 'format' must be transmitted")
    
    format = format.lower()
    if format not in formats:
        logger.log_error(f"Invalid format: {format}")
        return ErrorResponse(
            f"not such format '{format}'. Available: {formats}"
        )
    
    model_types = [key for key in Repository.keys()]
    if model is None:
        logger.log_error("Model parameter is missing")
        return ErrorResponse("param 'model' must be transmitted")
    
    if model not in model_types:
        logger.log_error(f"Invalid model: {model}")
        return ErrorResponse(
            f"not such model '{model}'. Available: {model_types}"
        )

    try:
        models = list(start_service.repository.data[model].values())
        result = factory_entities.create(format).build(models)
        
        logger.log_info(f"Response built successfully: {len(models)} items")
        return FormatResponse(result, format)
    except Exception as e:
        logger.log_error(f"Error building response: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recipes")
def get_recipes():
    """Получить список рецептов в формате JSON"""
    logger.log_debug("Get all recipes endpoint called")
    key = Repository.recipes_key
    recipes = list(start_service.repository.data[key].values())
    result = factory_converters.convert(recipes)

    logger.log_info(f"Returning {len(recipes)} recipes")
    return JsonResponse(result)

@app.get("/api/recipes/{unique_code}")
def get_recipe(unique_code: str):
    """
    Получить рецепт по уникальному коду
    """
    logger.log_info(f"Get recipe: unique_code={unique_code}")
    
    recipe = start_service.repository.get(unique_code=unique_code)
    if not recipe:
        logger.log_warning(f"Recipe not found: {unique_code}")
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    result = factory_converters.convert(recipe)
    logger.log_debug(f"Recipe retrieved: {unique_code}")
    
    return JsonResponse(result)

@app.get("/api/storages")
def get_storages():
    """Получить список всех ID хранилищ"""
    logger.log_debug("Get all storages endpoint called")
    
    try:
        storage_key = Repository.storages_key
        storages_data = start_service.repository.data[storage_key]
        storage_ids = list(storages_data.keys())
        
        logger.log_info(f"Returning {len(storage_ids)} storage IDs")
        return JsonResponse(storage_ids)
    except KeyError:
        logger.log_error(f"Storage key not found: {Repository.storages_key}")
        raise HTTPException(status_code=500, detail=f"Storage key '{Repository.storages_key}' not found")
    except Exception as e:
        logger.log_error(f"Error getting storages: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/api/tbs/{storage_id}")
def get_tbs(start_date: date, end_date: date, storage_id: str, filters: dict = None):
    """
    Таблица оборотно-сальдовой ведомости
    """
    logger.log_info(f"TBS calculation: storage_id={storage_id}, start_date={start_date}, end_date={end_date}")
    
    if filters is None:
        filters = {"filters": None}
    
    if "filters" not in filters:
        filters["filters"] = None
    
    filters_obj = filter_sorting_dto(filters["filters"])
    storage = start_service.repository.get(unique_code=storage_id)
    
    if storage is None:
        logger.log_error(f"Storage not found: {storage_id}")
        return ErrorResponse(f"Storage with code '{storage_id}' is null")
    
    if start_date >= end_date:
        logger.log_error(f"Invalid date range: {start_date} >= {end_date}")
        return ErrorResponse(f"End date must be later than start date")
    
    try:
        headers, display_data_rows = OsdTbs.calculate(storage_id, start_date, end_date, start_service, filters_obj)
        logger.log_info(f"TBS calculated: {len(display_data_rows)} rows")
        
        html_table_builder = factory_entities.create(ResponseFormat.HTMLTABLE)
        final_html = html_table_builder.build(headers=headers, data=display_data_rows, name="оборотно-сальдовой ведомости")
        
        return HTMLResponse(final_html)
    except Exception as e:
        logger.log_error(f"Error calculating TBS: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/save")
def save_data_to_file(filename: str = Query(...)):
    """
    Сохранить все данные репозитория в файл
    """
    logger.log_info(f"Save data to file: {filename}")
    
    if not filename.endswith(".json"):
        logger.log_error(f"Invalid filename: {filename}")
        raise HTTPException(status_code=400, detail="Filename must end with .json")

    safe_path = Path("data_exports") / filename
    safe_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        repository_data = start_service.repository.data
        result = factory_converters.convert(repository_data)
        
        with open(safe_path, 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=4)
        
        logger.log_info(f"Data saved successfully to {safe_path}")
        return JsonResponse({"message": f"Data saved successfully to {safe_path}"})
    
    except TypeError as te:
        logger.log_error(f"Data serialization error: {str(te)}")
        raise HTTPException(status_code=500, detail=f"Data serialization error: {str(te)}")
    except Exception as ex:
        logger.log_error(f"Failed to save data: {str(ex)}")
        raise HTTPException(status_code=500, detail=f"Failed to save data: {str(ex)}")

@app.get("/api/directories")
def get_directories():
    """Получить все справочники"""
    logger.log_debug("Get all directories endpoint called")
    
    directories = {
        "measure_unit": factory_converters.convert(start_service.repository.data[Repository.measure_unit_key]),
        "nomenclatures": factory_converters.convert(start_service.repository.data[Repository.nomenclatures_key]),
        "nomenclature_groups": factory_converters.convert(start_service.repository.data[Repository.nomenclature_group_key]),
        "storages": factory_converters.convert(start_service.repository.data[Repository.storages_key]),
        "transactions": factory_converters.convert(start_service.repository.data[Repository.transactions_key]),
    }
    
    logger.log_info("Directories retrieved successfully")
    return JsonResponse(directories)

@app.get("/api/transactions")
def get_transactions():
    """Получить все транзакции"""
    logger.log_debug("Get all transactions endpoint called")
    
    key = Repository.transactions_key
    transactions = list(start_service.transactions.values())
    
    logger.log_info(f"Returning {len(transactions)} transactions")
    return JsonResponse(transactions)

@app.get("/api/block_date")
def get_block_date():
    """Получить остатки на контрольную дату"""
    logger.log_debug("Get block date endpoint called")
    
    headers = start_service.repository.headers
    display_data_rows = start_service.repository.turnovers_history
    
    logger.log_info(f"Block date data: {len(display_data_rows)} rows")
    
    html_table_builder = factory_entities.create(ResponseFormat.HTMLTABLE)
    final_html = html_table_builder.build(headers=headers, data=display_data_rows, name="Остатки на контрольную дату")
    
    return HTMLResponse(final_html)

@app.post("/api/block_date_new")
def post_block_date(new_date: date = Query(...)):
    """Обновить остатки на новую дату"""
    logger.log_info(f"Update block date: {new_date}")
    
    try:
        start_service.convert_ost(new_date)
        headers = start_service.repository.headers
        display_data_rows = start_service.repository.turnovers_history
        
        logger.log_info(f"Block date updated: {len(display_data_rows)} rows")
        
        html_table_builder = factory_entities.create(ResponseFormat.HTMLTABLE)
        final_html = html_table_builder.build(headers=headers, data=display_data_rows, name=f"остатков на {new_date}")
        
        return HTMLResponse(final_html)
    except Exception as e:
        logger.log_error(f"Error updating block date: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ost/{new_date}")
def search_ost_date(new_date: date):
    """Получить остатки на указанную дату"""
    logger.log_info(f"Search OST for date: {new_date}")
    
    try:
        headers, display_data_rows = OsdTbs.calculate_new_ost(new_date, start_service)
        
        logger.log_info(f"OST calculated: {len(display_data_rows)} rows")
        
        html_table_builder = factory_entities.create(ResponseFormat.HTMLTABLE)
        final_html = html_table_builder.build(headers=headers, data=display_data_rows, name=f"остатков на {new_date}")
        
        return HTMLResponse(final_html)
    except Exception as e:
        logger.log_error(f"Error calculating OST: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/referense/{name}")
async def get_reference_item(name: str):
    """Получение элемента справочника по имени"""
    logger.log_info(f"Get reference item by name: {name}")
    
    try:
        model = start_service.repository.get(name=name)
        if model:
            logger.log_debug(f"Reference item found: {name}")
            return JsonResponse(content=factory_converters.convert(model))
        else:
            logger.log_warning(f"Reference item not found: {name}")
            raise HTTPException(status_code=404, detail=f"Элемент '{name}' не найден")
    except Exception as e:
        logger.log_error(f"Error getting reference item: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/{reference_type}/all")
async def get_all_reference_items(reference_type: str):
    """Получение всех элементов справочника"""
    logger.log_info(f"Get all reference items: {reference_type}")
    
    try:
        if reference_type == "nomenclatures":
            items = factory_converters.convert(start_service.nomenclatures)
        elif reference_type == "measure_units":
            items = factory_converters.convert(start_service.measure_units)
        elif reference_type == "nomenclature_groups":
            items = factory_converters.convert(start_service.nomenclature_groups)
        elif reference_type == "storages":
            items = factory_converters.convert(start_service.storages)
        elif reference_type == "transactions":
            items = factory_converters.convert(start_service.transactions)
        elif reference_type == "recipes":
            items = factory_converters.convert(start_service.data.get(Repository.recipes_key, {}))
        else:
            logger.log_error(f"Unknown reference type: {reference_type}")
            raise HTTPException(status_code=400, detail=f"Неизвестный тип справочника: {reference_type}")
        
        logger.log_info(f"Returning {len(items) if isinstance(items, list) else 'unknown'} items for {reference_type}")
        return JsonResponse(items)
    except Exception as e:
        logger.log_error(f"Error getting all reference items: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/api/{reference_type}")
async def put_reference(reference_type: str, data: dict):
    """Добавление нового элемента справочника"""
    logger.log_info(f"Add reference: type={reference_type}, data={data.get('name', 'unknown')}")
    
    try:
        ReferenceService.add(reference_type, data)
        logger.log_info(f"Reference added successfully: {reference_type}/{data.get('name')}")
        return {"status": "SUCCESS", "message": "Reference added successfully"}
    except Exception as e:
        logger.log_error(f"Error adding reference: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.patch("/api/{reference_type}")
async def patch_reference(reference_type: str, name: str = Query(...), data: dict = None):
    """Обновление элемента справочника"""
    logger.log_info(f"Update reference: type={reference_type}, name={name}")
    
    try:
        if data is None:
            logger.log_error("No data provided for update")
            return ErrorResponse("Не переданы данные для обновления")
        
        item = reference_service.get(reference_type, name)
        if not item:
            logger.log_warning(f"Reference item not found: {name}")
            raise HTTPException(status_code=404, detail=f"Элемент '{name}' не найден")
        
        update_data = {"unique_code": item.get("unique_code"), **data}
        ReferenceService.change(reference_type, update_data)
        
        logger.log_info(f"Reference updated successfully: {reference_type}/{name}")
        return {"status": "SUCCESS", "message": "Reference updated successfully"}
    except Exception as e:
        logger.log_error(f"Error updating reference: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/{reference_type}")
async def delete_reference(reference_type: str, name: str = Query(...)):
    """Удаление элемента справочника"""
    logger.log_info(f"Delete reference: type={reference_type}, name={name}")
    
    try:
        item = reference_service.get(reference_type, name)
        if not item:
            logger.log_warning(f"Reference item not found: {name}")
            raise HTTPException(status_code=404, detail=f"Элемент '{name}' не найден")
        
        ReferenceService.remove(reference_type, {"unique_code": item.get("unique_code")})
        
        logger.log_info(f"Reference deleted successfully: {reference_type}/{name}")
        return {"status": "SUCCESS", "message": "Reference deleted successfully"}
    except Exception as e:
        logger.log_error(f"Error deleting reference: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/block_date/update")
async def update_block_date(new_block_date: date = Query(...)):
    """Обновление даты блокировки"""
    logger.log_info(f"Update block date: {new_block_date}")
    
    try:
        new_block_datetime = datetime.combine(new_block_date, datetime.min.time())
        
        observe_service.create_event(event_type.change_block_period(), {
            "new_block_date": new_block_datetime
        })
        
        logger.log_info(f"Block date updated successfully: {new_block_date}")
        return {"status": "success", "message": "Block date updated", "new_block_date": new_block_date.strftime("%Y-%m-%d")}
    except Exception as e:
        logger.log_error(f"Error updating block date: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/logs/test")
async def test_logging():
    """Тестовый эндпоинт для проверки логирования"""
    logger.log_debug("Test debug message")
    logger.log_info("Test info message", {"test": True, "number": 42})
    logger.log_error("Test error message", {"error": "test_error"})
    
    return {"status": "success", "message": "Test logs written"}

if __name__ == "__main__":
    # Логируем запуск приложения
    logger.log_info("Application starting", {
        "timestamp": dt.now().isoformat(),
        "settings_file": settings_file
    })
    
    try:
        settings_manager.load(settings_file)
        start_service.start(settings_file)
        
        logger.log_info("Application initialized successfully", {
            "block_date": start_service.block_date,
            "host": "localhost",
            "port": 8082
        })
        
        uvicorn.run(app=app, host="localhost", port=8082)
        
    except Exception as e:
        logger.log_error("Application startup failed", {"error": str(e)})
        print(f"Application startup failed: {e}")
        raise
