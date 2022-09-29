package main

import (
	"fmt"
	"net/http"
	"os"
)

func main() {
	var mux *http.ServeMux = http.NewServeMux()
	var fs http.Handler = http.FileServer()

	mux.HandleFunc("/get_orgs", get_orgs)

	var port string = os.Getenv("PORT")

	if port == "" {
		port = "1421"
	}

	//handler := logRequestHandler(mux)
	fmt.Println("starting server at", port)
	//http.ListenAndServe(":"+port, handler)
}
