import uvicorn
from fastapi import FastAPI

from src.core.response_format import ResponseFormat
from src.core.http_responses import (TextResponse, JsonResponse, ErrorResponse,
                                     FormatResponse)
from src.logics.factory_entities import FactoryEntities
from src.logics.factory_converters import FactoryConverters
from src.singletons.repository import Repository
from src.singletons.start_service import StartService
from src.singletons.settings_manager import SettingsManager


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


if __name__ == "__main__":
    settings_manager.load(settings_file)
    start_service.start(settings_file)
    uvicorn.run(app=app,
                host="localhost",
                port=8080)
