package main

import (
	y2023d1 "advent/pkg/2023/1"
	"fmt"
	"os"
	"strconv"

	"github.com/spf13/cobra"
)

func main() {
	var test bool
	var inputFilename string

	cmd := &cobra.Command{
		Use:   "advent [year] [day] [a/b]",
		Args:  cobra.ExactArgs(3),
		Short: "Run advent of code problems",
		Run: func(cmd *cobra.Command, args []string) {
			run(cmd, args, test, inputFilename)
		},
	}
	cmd.Flags().BoolVar(&test, "test", false, "Run in test mode")
	cmd.Flags().StringVar(&inputFilename, "file", "", "A custom input data file to use")

	if err := cmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

func run(cmd *cobra.Command, args []string, test bool, inputFilename string) {

	yearStr, dayStr, part := args[0], args[1], args[2]

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

	filename := buildInputFilename(test, inputFilename, year, day, part)
	contentsBytes, err := os.ReadFile(filename)
	if err != nil {
		fmt.Println("Error reading input:", err)
		os.Exit(1)
	}
	contents := string(contentsBytes)

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

func buildInputFilename(test bool, inputFilename string, year, day int, part string) string {
	path := fmt.Sprintf("../inputs/%d/%d/%s/", year, day, part)
	filename := "input.txt"
	if test {
		filename = "test_input.txt"
	}
	if inputFilename != "" {
		filename = inputFilename
	}
	return path + filename
}
