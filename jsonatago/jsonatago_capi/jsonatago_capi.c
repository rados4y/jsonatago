#include <Python.h>

/* Will come from go */
extern void CompileJSONata(char* id, char* expression, char** resultError);
extern void FreeJSONata(char* id);
extern void EvaluateJSONata(char* id, char* jsonData, char** resultError, char** result);
extern void CompileEvaluateJSONata(char* expression, char* jsonData, char** resultError, char** result);

// Function to be called from Python - CompileJSONata
static PyObject* compile(PyObject* self, PyObject* args) {
    const char* id;
    const char* expression;
    char* resultError;

    if (!PyArg_ParseTuple(args, "ss", &id, &expression)) {
        return NULL;
    }

    CompileJSONata((char*)id, (char*)expression, &resultError);

    PyObject* ret = Py_BuildValue("s", resultError);
    free(resultError); // resultCode is allocated in Go code, it needs to be freed after use

    return ret;
}

// Function to be called from Python - FreeJSONata
static PyObject* free_compile(PyObject* self, PyObject* args) {
    const char* id;

    if (!PyArg_ParseTuple(args, "s", &id)) {
        return NULL;
    }

    FreeJSONata((char*)id);

    Py_RETURN_NONE;
}

// Function to be called from Python - EvaluateJSONata
static PyObject* evaluate(PyObject* self, PyObject* args) {
    const char* id;
    const char* jsonData;
    char* resultError;
    char* result;

    if (!PyArg_ParseTuple(args, "ss", &id, &jsonData)) {
        return NULL;
    }

    EvaluateJSONata((char*)id, (char*)jsonData, &resultError, &result);

    PyObject* ret = Py_BuildValue("ss", resultError, result);
    free(resultError); // resultCode is allocated in Go code, it needs to be freed after use
    free(result);     // result is allocated in Go code, it needs to be freed after use

    return ret;
}

// Function to be called from Python - EvaluateJSONata
static PyObject* compile_evaluate(PyObject* self, PyObject* args) {
    const char* expression;
    const char* jsonData;
    char* resultError;
    char* result;

    if (!PyArg_ParseTuple(args, "ss", &expression, &jsonData)) {
        return NULL;
    }

    CompileEvaluateJSONata((char*)expression, (char*)jsonData, &resultError, &result);

    PyObject* ret = Py_BuildValue("ss", resultError, result);
    free(resultError); // resultCode is allocated in Go code, it needs to be freed after use
    free(result);     // result is allocated in Go code, it needs to be freed after use

    return ret;
}


// Define methods in the module
static PyMethodDef JsonataMethods[] = {
    {"compile", compile, METH_VARARGS, "Compile JSONata expression"},
    {"free_compile", free_compile, METH_VARARGS, "Free JSONata expression"},
    {"evaluate", evaluate, METH_VARARGS, "Evaluate JSONata expression"},
    {"compile_evaluate", compile_evaluate, METH_VARARGS, "Compile and evaluate JSONata expression"},
    {NULL, NULL, 0, NULL}
};

// Define the module
static struct PyModuleDef jsonatamodule = {
    PyModuleDef_HEAD_INIT,
    "jsonatago_capi",   // name of module
    NULL, // module documentation, may be NULL
    -1,   // size of per-interpreter state of the module, or -1 if the module keeps state in global variables.
    JsonataMethods
};

// Initialize the module
PyMODINIT_FUNC PyInit_jsonatago_capi(void) {
    return PyModule_Create(&jsonatamodule);
}