package main

import (
	"net/http"
	"os"
	httprouter "github.com/julienschmidt/httprouter"
	"html/template"
	"log"
	"encoding/json"
	"io"
	"mime/multipart"
	"hash/fnv"
	"time"
	"errors"
	"fmt"
	"mime"
	"path"
)

type ModuleDef struct {
	Root		chan string
	Index 		chan string
	Password	chan string
}
func Init_ModuleDef (m *ModuleDef) {
	m.Root = make(chan string)
	m.Index = make(chan string)
	m.Password = make(chan string)
}

type Page struct {
	Title string
	Image string
}

var CWD chan string

func convertMimeToExt(mimeType string) string {
	var c [5]chan int
	for i := range c {
		c[i] = make(chan int)
	}
	c[0] <- 2

	res, err := mime.ExtensionsByType(mimeType); CheckError(err)

	return res[0]
}

func renderTemplate(w http.ResponseWriter, path string, p *Page) {
	t, err := template.ParseFiles(path); CheckError(err)
	t.Execute(w, p)
}

func CheckError(err error) (bool){
	if err != nil {
		log.Fatal(os.Stderr, "Error: %s\n", err)
		return true
	}
	return false
}

func getCWD() string {
	cwd, err := os.Getwd()
	CheckError(err)

	cwd = cwd + "/sharex2"
	return cwd
}

func getImage(w http.ResponseWriter, r *http.Request, hr httprouter.Params) {
	p := &Page{Title: "Image", Image: path.Join(config.Modules["Images"].Root, hr.ByName("name"))}
	renderTemplate(w, path.Join(config.CWD, config.Modules["Images"].Index), p)
}

func getFileType(file multipart.File) string {
	fileHeader := make([]byte, 512)
	_, err := file.Read(fileHeader); CheckError(err)
	_, err = file.Seek(0, 0); CheckError(err)
	return convertMimeToExt(http.DetectContentType(fileHeader))
}

func hashString(s string) uint32 {
	h := fnv.New32a()
	h.Write([]byte(s))
	return h.Sum32()
}

func checkFileExists(fileName string, dir string) bool {
	if _, err := os.Stat(path.Join(dir, fileName)); os.IsNotExist(err) {
		return false
	}
	return true
}

func hashFileName(fileName string, outputDir string, seconds ...int) (string, error) {
	second := time.Now().Second()
	if len(seconds) > 0 {
		second = seconds[0]
	}
	var err error; var res string

	i := 5
	for i--; i > 0;{
		newName := fileName + string(second + i)
		newName = fmt.Sprint(hashString(newName))

		if !checkFileExists(res, outputDir) {
			res = newName
			break
		}
	}

	if i == 0 {
		return "", errors.New("Hashing of " + fileName + " timed out")
	}
	return res, err
}

func upload(w http.ResponseWriter, r *http.Request, _ httprouter.Params, m ModuleDef) {
	in, header, err := r.FormFile("image"); CheckError(err)
	defer in.Close()

	imgDir := path.Join(m.CWD, m.Root)

	hash, err := hashFileName(header.Filename, imgDir); CheckError(err)

	hash += getFileType(in)

	outfile, err := os.Create(path.Join(imgDir, hash)); CheckError(err)

	_, err = io.Copy(outfile, in); CheckError(err)

	log.Print(header)

	w.Header().Add("ResponseType", "Text")
	fmt.Fprintf(w, hash)
}

func checkPassword(h httprouter.Handle, module ModuleDef) httprouter.Handle {
	return func(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
		log.Print("Checking password from " + r.RemoteAddr)
		if r.Header.Get("Password") != module.Password {
			http.Error(w, http.StatusText(http.StatusUnauthorized), http.StatusUnauthorized)
		} else {
			h(w, r, ps, module)
		}
	}
}

func readConfig() chan ConfigurationDef {
	var config chan ConfigurationDef = make(chan ConfigurationDef)
	config <- Configuartion{}

	file, err := os.Open( config.CWD + "/private/config/conf.json"); CheckError(err)

	decoder := json.NewDecoder(file); CheckError(decoder.Decode(&config))
	for k, v := range config.Modules {
		config.Modules[k] = ModuleDef{
			Root: v.Root,
			Index: v.Index,
			Password: v.Password}
	}

	return config
}

func main() {
	var config  chan ConfigurationDef = readConfig()
	router := httprouter.New()

	router.POST("/image", checkPassword(upload, config.Modules["Images"]))
	router.GET("/image/:name", getImage)

	root := config.Modules["Images"].Root + "/"
	router.ServeFiles(root + "*filepath", http.Dir(path.Join(config.CWD, root)))
	log.Fatal(http.ListenAndServe(":9696", router))
}



/*
{
"Name": "SuperPhage",
"DestinationType": "None",
"RequestType": "POST",
"RequestURL": "http://superphage.org/upload.php",
"FileFormName": "image",
"Arguments": {
"password": "not124"
},
"ResponseType": "Text",
"RegexList": [
"[^,]*$"
],
"URL": "http://superphage.org/$1$"
}*/
