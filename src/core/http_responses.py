from json import dumps
from typing import Any
from fastapi import Response


"""Текстовый HTTP ответ со статусом 200"""
class TextResponse(Response):

    def __init__(self, text: str):
        super().__init__(
            status_code=200,
            content=str(text),
            media_type="text/plain"
        )


"""HTTP ответ с контентом в формате JSON и со статусом 200"""
class JsonResponse(Response):

    def __init__(self, content: Any):
        super().__init__(
            status_code=200,
            content=dumps(content, ensure_ascii=False),
            media_type="application/json"
        )


"""HTTP ответ со статусом 4xx и описанием ошибки в формате JSON"""
class ErrorResponse(Response):

    def __init__(self, error: str, status_code: int = 400):
        super().__init__(
            status_code=status_code,
            content=dumps({"error": str(error)}),
            media_type="application/json"
        )


"""HTTP ответ с контентом в переданном формате и со статусом 200"""
class FormatResponse(Response):

    # Сопоставление текстового формата и содержания media_type
    match = {
        "csv": "text/plain; charset=utf-8",
        "json": "application/json",
        "markdown": "text/markdown; charset=utf-8",
        "xml": "text/xml",
    }

    def __init__(self, content: str, media_type: str):
        ct = self.match.get(media_type, "text/plain")
        if ct == "json":
            content = dumps(content)
        super().__init__(
            status_code=200,
            content=content,
            media_type=ct,
        )
