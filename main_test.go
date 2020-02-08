package main

import (
	"os"
	"testing"
)

const argsString string = "\nArgs:\n%s"
const errorString string = "%s was incorrect, got %s, but wanted %s" + argsString
const hasErrorsString string = "Expected there to be no errors but got %s" + argsString

func TestHash(t *testing.T) {
	hashValues := [...]uint32{2949673445, 2166136261}
	hashText := [...]string{"test", ""}

	for i, e := range hashText {
		hashedText := hashString(e)
		if hashedText != hashValues[i] {
			t.Errorf(errorString, "Hash", string(hashedText), string(hashValues[i]), e)
		}
	}
}

func TestCheckFileExists(t *testing.T) {
	fileNames := [2]string{"main_test.go", "totallynewfile.txt"}
	existence := [2]bool{true, false}
	//dir := "./"
	dir, _ := os.Getwd()
	existsStr := "false"
	nonStr := "true"

	for i, e := range fileNames {
		exists := checkFileExists(e, dir)
		t.Logf("Checking %s and %s, %t, %t", e, dir, existence[i], exists)
		if exists != existence[i] {
			if exists {
				existsStr = "true"
				nonStr = "false"
			}
			t.Errorf(errorString, "CheckFileExists", existsStr, nonStr, dir + "\n" + e)
		}
	}

	exists := checkFileExists(fileNames[0], "B:")
	if exists {
		existsStr = "true"
		nonStr = "false"
		t.Errorf(errorString, "CheckFileExists", nonStr, existsStr, fileNames[0] + "\n" + "B:")
	}

}

func TestHashFileName(t *testing.T) {
	fileName := "test"
	time := 10
	outputDir := "./"

	res, err := hashFileName(fileName, outputDir, time)

	if err != nil {
		t.Errorf("error %s", err)
	}
	if len(res) == 0  {
		t.Errorf("error in %s, result: %s", "HashFileName", res)
	}
}

