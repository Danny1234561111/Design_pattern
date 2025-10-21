import connexion
from flask import request

from Src.Core.response_format import ResponseFormat
from Src.Logics.factory_entities import factory_entities
from Src.reposity import reposity
from Src.start_service import start_service
from Src.settings_manager import settings_manager

# Путь к файлу настроек
settings_file = "D:/Загрузки/homework6/Design_pattern/settings.json"

# Инициализация сервисов
start_service = start_service()
settings_manager = settings_manager()
factory = factory_entities()

# Инициализация приложения
app = connexion.FlaskApp(__name__)

"""Проверить доступность REST API"""
@app.route("/api/status", methods=['GET'])
def status():
    return {"status": "success"}

"""Доступные форматы ответов"""
@app.route("/api/responses/formats", methods=['GET'])
def get_response_formats():
    return [
        format.name.lower()
        for format in ResponseFormat
    ]

"""Типы моделей, доступные для формирования ответов"""
@app.route("/api/responses/models", methods=['GET'])
def get_response_models():
    return [
        key
        for key in reposity.keys()
    ]

"""Сформировать ответ для моделей (model) в переданном формате (format)"""
@app.route("/api/responses/build", methods=['GET'])
def build_response():
    format = request.args.get('format')
    if format is None:
        return {"error": "param 'format' must be transmitted"}
    
    format = format.lower()
    if format not in get_response_formats():
        return {
            "error": f"not such format '{format}'. Available: "
                    f"{get_response_formats()}"
        }
    
    model_type = request.args.get('model')
    if model_type is None:
        return {"error": "param 'model' must be transmitted"}
    
    if model_type not in get_response_models():
        return {
            "error": f"not such model '{model_type}'. "
                    f"Available: {get_response_models()}"
        }

    models = list(start_service.repository.data[model_type].values())

    return {"result": factory.create(format).build(models)}

# Проверка файла настроек
if not os.path.exists(self.settings_file):
        print(f"File does not exist: {settings_file}")

# Запуск приложения
if __name__ == '__main__':
    start_service.start(settings_file)
    settings_manager.load(settings_file)
    app.run(host="localhost", port=8080)
