package main

import (
	"fmt"
	"net/http"
)

// Implementando un servidor HTTP básico, que responde con
func main() {
	http.HandleFunc("/", handler)
	http.ListenAndServe("localhost:8080", nil) // iniciando el servidor
}

// handler recibe la petición http y la procesa para devolver una respuesta http
func handler(response http.ResponseWriter, request *http.Request) {
	fmt.Fprintf(response, "Hola Go API's")
}
