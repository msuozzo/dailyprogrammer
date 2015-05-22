package main

import (
	"fmt"
    "log"
	"io/ioutil"
	"os"
	"sort"
	"strconv"
	"strings"
)

type WordCount struct {
	Word  string
	Count uint
}

// Define type to sort WordCounts
type ByCount []WordCount
func (a ByCount) Len() int           { return len(a) }
func (a ByCount) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }
func (a ByCount) Less(i, j int) bool { return a[i].Count < a[j].Count }


// Return a mapping of words (strings without whitespace) to their frequency in
// the string provided
func wordCount(s string) map[string]uint {
	m := make(map[string]uint)
	words := strings.Fields(s)
	for _, word := range words {
		if v, present := m[word]; !present {
			m[word] = v
		}
		m[word] += 1
	}
	return m
}

func main() {
    // Read file provided as first argument
	fname := os.Args[1]
	file_bytes, err := ioutil.ReadFile(fname)
	if err != nil {
            log.Fatal("Failed to load file: ", err)
	}
	file_text := string(file_bytes)

    // Read n and parse as uint
	n_str := os.Args[2]
	n, err := strconv.ParseUint(n_str, 10, 32)
	if err != nil {
            log.Fatal("Failed to parse n: ", err)
	}

    // Count words and sort these counts
    word_count := wordCount(file_text)
	counts := []WordCount{}
	for word, count := range word_count {
		counts = append(counts, WordCount{word, count})
	}
	sort.Sort(sort.Reverse(ByCount(counts)))

    last_ind := int(n)
    if last_ind > len(counts) {
            fmt.Println("NOTE: File has fewer than ", n, " unique words.")
            fmt.Println("      Only able to display ", len(counts), " words.")
            last_ind = len(counts)
    }
	for i := 0; i < last_ind; i++ {
		fmt.Println(counts[i])
	}
}
