package main

import (
	"net/http"
	"log"
	"bytes"
	"mime/multipart"
	"os"
	"io"
)

func CheckError(err error) (bool){
	if err != nil {
		log.Fatalf("Error: %s\n", err)
		return true
	}
	return false
}

func main() {
	fName := "16933492_1286194308131803_1797124886_n.jpg"

	bodyBuf := &bytes.Buffer{}
	bodyWriter := multipart.NewWriter(bodyBuf)


	fileWriter, err := bodyWriter.CreateFormFile("image", fName)
	CheckError(err)

	fh, err := os.Open(fName)
	CheckError(err)

	_, err = io.Copy(fileWriter, fh)
	CheckError(err)

	contentType := bodyWriter.FormDataContentType()
	_ = bodyWriter.Close()

	req, _ := http.NewRequest("POST", "http://localhost:9696/image", bodyBuf)
	req.Header.Add("password", "not124")
	req.Header.Add("Content-Type", contentType)

	c := &http.Client{}

	resp, err := c.Do(req)
	CheckError(err)

	log.Print(resp)

	/*req, _ := http.NewRequest("POST","http://localhost:9696/image", strings.NewReader(form.Encode()))
	req.Header.Add("Content-Type", "multipart/form-data")
	err := req.ParseForm()
	if(err == nil) {
		log.Print(err)
	}
	v := 3 + 3

	log.Print(res, v)*/


}