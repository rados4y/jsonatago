from ctypes import cdll, c_char_p, POINTER, byref
from importlib.resources import files
import platform
import os
from typing import Any


class Jsonata:
    __lib = None

    @staticmethod
    def __lib_init():
        # Load the shared library
        if Jsonata.__lib is not None:
            return

        # dll_path = pkg_resources.resource_filename("jsonatago", "golang/jsonatago.dll")
        resource_dir = str(files("jsonatago") / "golang")
        if platform.system() == "Windows":
            dll_file = "jsonatago_windows.dll"
        elif platform.system() == "Linux":
            dll_file = "jsonatago_linux.so"
        elif platform.system() == "Darwin":
            dll_file = "jsonatago_darwin.so"
        else:
            raise Exception(f"Unsupported platform: {platform.system()}")
        dll_path = os.path.join(resource_dir, dll_file)
        Jsonata.__lib = cdll.LoadLibrary(str(dll_path))

        # Set argument types and return types for CompileJSONata
        Jsonata.__lib.CompileJSONata.argtypes = [
            c_char_p,
            c_char_p,
            POINTER(c_char_p),
            POINTER(c_char_p),
        ]

        # Set argument types and return types for EvaluateJSONata
        Jsonata.__lib.EvaluateJSONata.argtypes = [
            c_char_p,
            c_char_p,
            POINTER(c_char_p),
            POINTER(c_char_p),
        ]

    def __init__(self, expression: str):
        Jsonata.__lib_init()
        # Data and pointers for CompileJSONata
        expression_bytes = expression.encode("utf-8")
        id_bytes = str(id(self)).encode("utf-8")
        resultCodeCompile = c_char_p()
        resultExpr = c_char_p()

        # Call CompileJSONata
        Jsonata.__lib.CompileJSONata(  # type:ignore
            id_bytes, expression_bytes, byref(resultCodeCompile), byref(resultExpr)
        )

        # Check result
        assert resultCodeCompile.value
        if resultCodeCompile.value.decode("utf-8") != "OK":
            raise Exception(
                f'JSONata compilation failed: {resultCodeCompile.value.decode("utf-8")}'
            )

    def __del__(self):
        if Jsonata.__lib is not None:
            return
        Jsonata.__lib.FreeJSONata(str(id(self)).encode("utf-8"))

    def evaluate(self, jsonData: str) -> str:
        # Data and pointers for EvaluateJSONata
        jsonData_bytes = jsonData.encode("utf-8")
        id_bytes = str(id(self)).encode("utf-8")
        resultCodeEval = c_char_p()
        result = c_char_p()

        # Call EvaluateJSONata
        Jsonata.__lib.EvaluateJSONata(  # type:ignore
            id_bytes, jsonData_bytes, byref(resultCodeEval), byref(result)
        )

        # Check result
        assert resultCodeEval.value
        if resultCodeEval.value.decode("utf-8") != "OK":
            raise Exception(
                f'JSONata evaluation failed: {resultCodeEval.value.decode("utf-8")}'
            )
        else:
            assert result.value
            return result.value.decode("utf-8")
