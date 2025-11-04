from enum import Enum, auto


"""Форматы ответов"""
class ResponseFormat(Enum):
    CSV = auto()
    MARKDOWN = auto()
    JSON = auto()
    XML = auto()
    HTMLTABLE=auto()
