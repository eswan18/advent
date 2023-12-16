package main

import (
	y2023d1 "advent/pkg/2023/1"
	"fmt"
	"os"
	"strconv"
)

func main() {
	if len(os.Args) != 4 {
		fmt.Println("Usage: go run ./cmd/advent/main.go <year> <day> <a/b>")
		os.Exit(1)
	}

	// os.Args[0] is the program name, so arguments start from os.Args[1]
	yearStr, dayStr, part := os.Args[1], os.Args[2], os.Args[3]

	// Coerce year and day to integers
	year, err := strconv.Atoi(yearStr)
	if err != nil {
		fmt.Println("Invalid year", yearStr)
		os.Exit(1)
	}
	validYears := map[int]bool{2023: true}
	if !validYears[year] {
		fmt.Println("Invalid year", yearStr)
		os.Exit(1)
	}

	day, err := strconv.Atoi(dayStr)
	if err != nil {
		fmt.Println("Invalid day", dayStr)
		os.Exit(1)
	}
	validDays := map[int]bool{}
	for i := 1; i <= 25; i++ {
		validDays[i] = true
	}
	if !validDays[day] {
		fmt.Println("Invalid day", dayStr)
		os.Exit(1)
	}

	contents, err := contentsFor(year, day, part)
	if err != nil {
		fmt.Println("Error reading input:", err)
		os.Exit(1)
	}

	var result string
	switch year {
	case 2023:
		result, err = run2023(day, part, contents)
	}
	if err != nil {
		fmt.Println("Error :", err)
		os.Exit(1)
	}
	fmt.Printf("Solution: %s\n", result)
}

func run2023(day int, part, contents string) (string, error) {
	switch day {
	case 1:
		switch part {
		case "a":
			return y2023d1.Run_a(contents)
		case "b":
			// return y2023d1.Run_b(contents)
		}
	}
	return "", fmt.Errorf("Invalid day/part combination: %d, %s", day, part)
}

func contentsFor(year, day int, part string) (string, error) {
	filename := fmt.Sprintf("../inputs/%d/%d/%s/input.txt", year, day, part)
	// Read and return the file's contents as a string
	content, err := os.ReadFile(filename)
	if err != nil {
		return "", err
	}
	return string(content), nil
}
