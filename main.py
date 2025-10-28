import connexion
from flask import request, jsonify
from Src.Core.response_format import ResponseFormat
from Src.Logics.factory_entities import factory_entities
from Src.reposity import reposity
from Src.start_service import start_service
from Src.settings_manager import settings_manager
from Src.Convert.convert_factory import FactoryConvertors  # Убедитесь, что путь правильный
from Src.Core.validator import argument_exception
from Src.Core.validator import operation_exception
from Src.Core.validator import validator
from enum import Enum
from typing import List, Any


name = "responses"
settings_file = "settings.json"

service_instance = start_service()
settings_manager_instance = settings_manager()
reposity_instance = reposity()  # Экземпляр reposity

app = connexion.FlaskApp(name)


@app.route("/api/status", methods=['GET'])
def status():
    return {"status": "success"}


@app.route("/api/responses/formats", methods=['GET'])
def get_response_formats():
    return [format.name.lower() for format in ResponseFormat]


@app.route("/api/responses/models", methods=['GET'])
def get_response_models():
    return [key for key in reposity_instance.keys()]


@app.route("/api/responses/build", methods=['GET'])
def build_response():
    format_param = request.args.get('format', '').lower()  # Получаем параметр формата
    try:
        validator.validate(format_param, str)  # Валидация формата
    except argument_exception as e:
        return {"error": str(e)}, 400

    try:
        format_enum = ResponseFormat[format_param.upper()]
    except KeyError:
        return {
            "error": f"not such format '{format_param}'. Available: {get_response_formats()}"
        }, 400

    model_type = request.args.get('model')
    try:
        validator.validate(model_type, str)  # Валидация типа модели
    except argument_exception as e:
        return {"error": str(e)}, 400

    if model_type not in get_response_models():
        return {
            "error": f"not such model '{model_type}'. Available: {get_response_models()}"
        }, 400

    models = service_instance._reposity.data.get(model_type, [])

    if not models:
        return {"error": f"No models found for type '{model_type}'."}, 404
    try:
        # Применяем FactoryConvertors для создания данных перед формированием ответа
        factory = FactoryConvertors()
        converted_models = factory.convert(models)

        # Применяем factory_entities для создания ответа
        response_output = factory_entities.create_response(format_enum, converted_models)

        if format_enum == ResponseFormat.JSON:
            return jsonify(response_output), {'Content-Type': 'application/json'}
        elif format_enum == ResponseFormat.CSV:
            return response_output, {'Content-Type': 'text/csv'}
        elif format_enum == ResponseFormat.MARKDOWN:
            return response_output, {'Content-Type': 'text/markdown'}
        elif format_enum == ResponseFormat.XML:
            return response_output, {'Content-Type': 'text/plain'}
        else:
            return response_output  # Вернуть в стандартном формате
    except (argument_exception, operation_exception) as e:
        return {"error": str(e)}, 500


@app.route("/api/receipts", methods=['GET'])
def GetReceipts():
    receipts = service_instance.get_receipts()  # Получаем все рецепты
    factory = FactoryConvertors()
    return jsonify(factory.convert(receipts))  # Преобразование через фабрику конвертеров


@app.route("/api/receipt/<int:id>", methods=['GET'])
def GetReceipt(id):
    receipt = service_instance.get_receipt(id)  # Получение конкретного чека
    factory = FactoryConvertors()
    return jsonify(factory.convert(receipt))  # Преобразование через фабрику конвертеров


# Запуск приложения
if __name__ == '__main__':
    try:
        settings_manager_instance.load(settings_file)
        service_instance.start(settings_file)
        app.run(host="localhost", port=8080)
    except Exception as e:
        print(f"Ошибка при запуске приложения: {str(e)}")