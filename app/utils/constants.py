from enum import Enum

from typing import Union, Dict, List, Any , TypeVar

JSONType = Union[Dict[str, Any], List[Any], str, int, float, bool, None]

T = TypeVar("T")


class HTTPMethods():
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"


class AuthMethod():
    PAT = "PAT"
    OAUTH = "OAUTH"

