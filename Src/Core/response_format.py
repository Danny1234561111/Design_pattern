from enum import Enum

class ResponseFormat(str, Enum):
    CSV = "CSV"
    MARKDOWN = "MARKDOWN"
    XML = "XML"
    JSON = "JSON"
