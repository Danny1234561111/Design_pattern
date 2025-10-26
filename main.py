import connexion
from flask import request
from Src.Core.response_format import ResponseFormat
from Src.Logics.factory_entities import factory_entities
from Src.reposity import reposity  # Обратите внимание на импорт
from Src.start_service import start_service
from Src.settings_manager import settings_manager

# Путь к файлу настроек
settings_file = "settings.json"

# Инициализация сервисов
service_instance = start_service()
settings_manager_instance = settings_manager()
reposity_instance = reposity()  # Экземпляр reposity

# Инициализация приложения
app = connexion.FlaskApp(__name__)

@app.route("/api/status", methods=['GET'])
def status():
    return {"status": "success"}

@app.route("/api/responses/formats", methods=['GET'])
def get_response_formats():
    return [format.name.lower() for format in ResponseFormat]

@app.route("/api/responses/models", methods=['GET'])
def get_response_models():
    return [key for key in reposity_instance.keys()]  # Используем экземпляр

@app.route("/api/responses/build", methods=['GET'])
def build_response():
    format_param = request.args.get('format', '').lower()  # Получаем параметр формата
    if not format_param:
        return {"error": "param 'format' must be transmitted"}, 400
    
    # Согласуем формат с ResponseFormat
    try:
        format_enum = ResponseFormat[format_param.upper()]
    except KeyError:
        return {
            "error": f"not such format '{format_param}'. Available: {get_response_formats()}"
        }, 400
    
    model_type = request.args.get('model')
    if not model_type:
        return {"error": "param 'model' must be transmitted"}, 400
    
    if model_type not in get_response_models():
        return {
            "error": f"not such model '{model_type}'. Available: {get_response_models()}"
        }, 400

    models = service_instance._reposity.data.get(model_type, [])
    
    print(f"Модели для '{model_type}': {models}")  # Проверяем модели
    
    if not models:
        return {"error": f"No models found for type '{model_type}'."}, 404

    # Применяем factory_entities для создания ответа
    response_output = factory_entities.create_response(format_enum, models)
    
    # Устанавливаем правильный Content-Type в зависимости от формата
    if format_enum == ResponseFormat.JSON:
        return response_output, {'Content-Type': 'application/json'}
    elif format_enum == ResponseFormat.CSV:
        return response_output, {'Content-Type': 'text/csv'}
    elif format_enum == ResponseFormat.MARKDOWN:
        return response_output, {'Content-Type': 'text/markdown'}
    elif format_enum == ResponseFormat.XML:
        return response_output, {'Content-Type': 'text/plain'}
    else:
        return response_output  # Вернуть в стандартном формате
# Запуск приложения
if __name__ == '__main__':
    try:
        settings_manager_instance.load(settings_file)
        service_instance.start(settings_file)
        app.run(host="localhost", port=8080)
    except Exception as e:
        print(f"Ошибка при запуске приложения: {str(e)}")