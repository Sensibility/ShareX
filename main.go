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
	"strings"
	"time"
	"errors"
	"fmt"
	"mime"
	"path"
)

type ModuleDef struct {
	Root		string
	Index 		string
	Password	string
}
type ConfigurationDef struct {
	CWD string
	Modules map[string]ModuleDef
}

type Page struct {
	Title string
	Image string
}

var config ConfigurationDef
type handle func(w http.ResponseWriter, r *http.Request, _ httprouter.Params, m ModuleDef)

func convertMimeToExt(mimeType string) string {
	res, err := mime.ExtensionsByType(mimeType); CheckError(err)

	return res[0]
}

func renderTemplate(w http.ResponseWriter, path string, p *Page) {
	t, err := template.ParseFiles(path); CheckError(err)
	_ = t.Execute(w, p)
}

func CheckError(err error) bool {
	if err != nil {
		log.Fatalf("Error: %s\n", err)
		return true
	}
	return false
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
	_, _ = h.Write([]byte(s))
	return h.Sum32()
}

func checkFileExists(fileName string, dir string) bool {
	_, err := os.Stat(strings.ReplaceAll(path.Join(dir, fileName), "/", "\\"))
	return !os.IsNotExist(err)
}

func hashFileName(fileName string, outputDir string, seconds ...int) (string, error) {
	second := time.Now().Second()
	if len(seconds) > 0 {
		second = seconds[0]
	}
	var err error; var res string
	i := 5
	for ; i > 0; i-- {
		newName := fileName + string(second + i)
		newName = fmt.Sprint(hashString(newName))

		if !checkFileExists(newName, outputDir) {
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

	imgDir := path.Join(config.CWD, m.Root)

	hash, err := hashFileName(header.Filename, imgDir); CheckError(err)

	hash += getFileType(in)

	outfile, err := os.Create(path.Join(imgDir, hash)); CheckError(err)

	_, err = io.Copy(outfile, in); CheckError(err)

	log.Print(header)

	w.Header().Add("ResponseType", "Text")
	_, _ = fmt.Fprintf(w, hash)
}

func checkPassword(h handle, module ModuleDef) httprouter.Handle {
	return func(w http.ResponseWriter, r *http.Request, ps httprouter.Params) {
		log.Print("Checking password from " + r.RemoteAddr)
		if r.Header.Get("Password") != module.Password {
			http.Error(w, http.StatusText(http.StatusUnauthorized), http.StatusUnauthorized)
		} else {
			h(w, r, ps, module)
		}
	}
}

func readConfig()  {
	dir, _ := os.Getwd()
	config = ConfigurationDef{
		CWD:   dir,
		Modules: nil,
	}

	file, err := os.Open( config.CWD + "/private/config/conf.json"); CheckError(err)

	decoder := json.NewDecoder(file); CheckError(decoder.Decode(&config))
	for k, v := range config.Modules {
		config.Modules[k] = ModuleDef{
			Root: v.Root,
			Index: v.Index,
			Password: v.Password}
	}
}
func main() {
	readConfig()
	router := httprouter.New()

	router.POST("/image", checkPassword(upload, config.Modules["Images"]))
	router.GET("/image/:name", getImage)

	root := config.Modules["Images"].Root
	router.ServeFiles(root + "*filepath", http.Dir(path.Join(config.CWD, root)))
	log.Fatal(http.ListenAndServe(":5000", router))
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
