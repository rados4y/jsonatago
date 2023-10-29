from typing import Any
import json
from .jsonatago_capi import compile, free_compile, evaluate, compile_evaluate  # type: ignore


def jeval(jsonData: Any, expression: str, raw: bool = False) -> Any:
    code: str
    result: str
    if not isinstance(jsonData, str):
        jsonData = json.dumps(jsonData)
    code, result = compile_evaluate(expression, jsonData)  # type:ignore
    return result_to_python(code, result, raw)  # type:ignore


class Jsonata:
    def __init__(self, expression: str):
        code: str
        code = compile(str(id(self)), expression)  # type:ignore
        if code:
            raise Exception(f"JSONata compilation failed: {code}")

    def __del__(self):
        free_compile(str(id(self)))

    def evaluate(self, jsonData: Any, raw: bool = False) -> Any:
        code: str
        result: str
        if not isinstance(jsonData, str):
            jsonData = json.dumps(jsonData)
        code, result = evaluate(str(id(self)), jsonData)  # type:ignore
        return result_to_python(code, result, raw)  # type:ignore


def result_to_python(code: str, result: str, raw: bool = False) -> Any:
    # no result
    if code == "no results found":
        return None
    # error
    if code:
        raise Exception(f"JSONata evaluation failed: {code}")
    # boolean
    if raw:
        return result
    if result == "true":
        return True
    if result == "false":
        return False
    # string
    if result.startswith('"') and result.endswith('"'):
        return result[1:-1]
    # json object
    if result.startswith("{") and result.endswith("}"):
        return json.loads(result)
    # json array
    if result.startswith("[") and result.endswith("]"):
        return json.loads(result)
    # try number
    try:
        return float(result)
    except ValueError:
        pass
    return result
