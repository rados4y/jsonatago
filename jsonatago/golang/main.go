package main

import (
	"C"
	"encoding/json"
	"fmt"
	"sync"

	"github.com/blues/jsonata-go"
)

var (
	exprMap  = make(map[string]*jsonata.Expr)
	mapMutex sync.RWMutex
)

//export CompileJSONata
func CompileJSONata(id *C.char, expression *C.char, resultCode **C.char, resultExpression **C.char) {
	expr, err := jsonata.Compile(C.GoString(expression))
	if err != nil {
		*resultCode = C.CString("CompileError")
		*resultExpression = expression
		return
	}
	mapMutex.Lock()
	exprMap[C.GoString(id)] = expr
	mapMutex.Unlock()

	*resultCode = C.CString("OK")
	*resultExpression = expression
}

//export FreeJSONata
func FreeJSONata(id *C.char) {
	mapMutex.Lock()
	delete(exprMap, C.GoString(id))
	mapMutex.Unlock()
}

//export EvaluateJSONata
func EvaluateJSONata(id *C.char, jsonData *C.char, resultCode **C.char, result **C.char) {
	mapMutex.RLock()
	expr, exists := exprMap[C.GoString(id)]
	mapMutex.RUnlock()

	if !exists {
		*resultCode = C.CString("InvalidID")
		*result = C.CString("")
		return
	}

	var input interface{}
	err := json.Unmarshal([]byte(C.GoString(jsonData)), &input)
	if err != nil {
		*resultCode = C.CString("UnmarshalError")
		*result = C.CString("")
		return
	}

	evalResult, err := expr.Eval(input)
	if err != nil {
		*resultCode = C.CString("EvaluateError")
		*result = C.CString("")
		return
	}

	resultBytes, err := json.Marshal(evalResult)
	if err != nil {
		*resultCode = C.CString("MarshalError")
		*result = C.CString("")
		return
	}

	*resultCode = C.CString("OK")
	*result = C.CString(string(resultBytes))
}

func main() {
	fmt.Println("Hello, Modules2! This is mypackage speaking!")
}
