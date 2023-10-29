package main

import (
	"C"
	"encoding/json"
	"sync"

	"github.com/blues/jsonata-go"
)

var (
	exprMap  = make(map[string]*jsonata.Expr)
	mapMutex sync.RWMutex
)

//export CompileEvaluateJSONata
func CompileEvaluateJSONata(expression *C.char, jsonData *C.char, resultError **C.char, result **C.char) {
	expr, err := jsonata.Compile(C.GoString(expression))
	if err != nil {
		*resultError = C.CString(err.Error())
		return
	}
	var input interface{}
	err = json.Unmarshal([]byte(C.GoString(jsonData)), &input)
	if err != nil {
		*resultError = C.CString(err.Error())
		*result = C.CString("")
		return
	}

	evalResult, err := expr.Eval(input)
	if err != nil {
		*resultError = C.CString(err.Error())
		*result = C.CString("")
		return
	}

	resultBytes, err := json.Marshal(evalResult)
	if err != nil {
		*resultError = C.CString(err.Error())
		*result = C.CString("")
		return
	}

	*resultError = C.CString("")
	*result = C.CString(string(resultBytes))
}

//export CompileJSONata
func CompileJSONata(id *C.char, expression *C.char, resultError **C.char) {
	expr, err := jsonata.Compile(C.GoString(expression))
	if err != nil {
		*resultError = C.CString(err.Error())
		return
	}
	mapMutex.Lock()
	exprMap[C.GoString(id)] = expr
	mapMutex.Unlock()

	*resultError = C.CString("")
}

//export FreeJSONata
func FreeJSONata(id *C.char) {
	mapMutex.Lock()
	delete(exprMap, C.GoString(id))
	mapMutex.Unlock()
}

//export EvaluateJSONata
func EvaluateJSONata(id *C.char, jsonData *C.char, resultError **C.char, result **C.char) {
	mapMutex.RLock()
	expr, exists := exprMap[C.GoString(id)]
	mapMutex.RUnlock()

	if !exists {
		*resultError = C.CString("invalid identifier of object")
		*result = C.CString("")
		return
	}

	var input interface{}
	err := json.Unmarshal([]byte(C.GoString(jsonData)), &input)
	if err != nil {
		*resultError = C.CString(err.Error())
		*result = C.CString("")
		return
	}

	evalResult, err := expr.Eval(input)
	if err != nil {
		*resultError = C.CString(err.Error())
		*result = C.CString("")
		return
	}

	resultBytes, err := json.Marshal(evalResult)
	if err != nil {
		*resultError = C.CString(err.Error())
		*result = C.CString("")
		return
	}

	*resultError = C.CString("")
	*result = C.CString(string(resultBytes))
}

func main() {
}
