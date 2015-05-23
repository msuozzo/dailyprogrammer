package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"regexp"
	"strings"
)

// source: http://stackoverflow.com/a/19832661/862857
func unpack(lst []string, vars ...*string) {
	if len(vars) != len(lst) {
		log.Fatal("Failed to unpack. Lengths do not match. len(", lst, ") != len(", vars, ")")
	}
	for i, str := range lst {
		*vars[i] = str
	}
}

// adapted from: http://stackoverflow.com/a/11422901/862857
func for_each_line(fname string) chan string {
	c := make(chan string)
	go func() {
		file, err := os.Open(fname)
		if err != nil {
			log.Fatal(err)
		}
		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			c <- scanner.Text()
		}
		close(c)
	}()
	return c
}

type RestrictionEnzyme struct {
	Name     string
	Type     string
	Pattern  *regexp.Regexp
	CutIndex int
}

// Take a string of the form "NAME TYPE PREPAT^POSTPAT" defining a restriction
// enzyme and generate a RestrictionEnzyme struct to encapsulate its behavior
func parse_enzyme(line string) RestrictionEnzyme {
	var name, type_, pat_str string
	unpack(strings.Fields(line), &name, &type_, &pat_str)
	cut_ind := strings.Index(pat_str, "^")
	cleaned_pat := strings.Replace(pat_str, "^", "", 1)
	lowered_pat := strings.ToLower(cleaned_pat)
	pat, _ := regexp.Compile(lowered_pat)
	return RestrictionEnzyme{name, type_, pat, cut_ind}
}

func main() {
	// Load enzyme definitions from the first file argument and create structs
	enzymes_fname := os.Args[1]
	var enzymes []RestrictionEnzyme
	for line := range for_each_line(enzymes_fname) {
		enzymes = append(enzymes, parse_enzyme(line))
	}

	// Load DNA sequence from second file argument and coalesce it into a
	// single string
	sequence_fname := os.Args[2]
	var subseqs []string
	for line := range for_each_line(sequence_fname) {
		subseqs = append(subseqs, strings.Fields(line)[1:]...)
	}
	sequence := strings.Join(subseqs, "")
	sequence = strings.ToLower(sequence)

	// Search through each enzyme in order and print any matches
	for _, enzyme := range enzymes {
		for _, index := range enzyme.Pattern.FindAllStringIndex(sequence, -1) {
			begin := index[0]
			end := index[1]
			// Print the name and absolute cut index
			fmt.Print(enzyme.Name, " ", begin+enzyme.CutIndex, " ")
			// Print the cut sequence with context
			leading_chars := 5
			trailing_chars := 20 - leading_chars - 3 - (end - begin)
			cut_str := fmt.Sprintf("[%s %s]", sequence[begin:begin+enzyme.CutIndex], sequence[begin+enzyme.CutIndex:end])
			with_context := fmt.Sprintf("%s%s%s", sequence[begin-leading_chars:begin], cut_str, sequence[end:end+trailing_chars])
			fmt.Println(with_context)
		}
	}
}
