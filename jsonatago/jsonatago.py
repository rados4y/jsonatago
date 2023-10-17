from .jsonatago_capi import compile_jsonata, free_jsonata, evaluate_jsonata  # type: ignore


class Jsonata:
    def __init__(self, expression: str):
        code: str
        code = compile_jsonata(str(id(self)), expression)  # type:ignore
        if code:
            raise Exception(f"JSONata compilation failed: {code}")

    def __del__(self):
        free_jsonata(str(id(self)))

    def evaluate(self, jsonData: str) -> str:
        code: str
        result: str
        code, result = evaluate_jsonata(str(id(self)), jsonData)  # type:ignore
        if code:
            raise Exception(f"JSONata evaluation failed: {code}")
        return result
