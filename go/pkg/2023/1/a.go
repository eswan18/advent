package y2023d1

import (
	"fmt"
	"strings"
)

func Run_a(contents string) (string, error) {
	contents = strings.TrimSpace(contents)
	lines := strings.Split(contents, "\n")
	total := 0
	for _, line := range lines {
		number, err := extractDigits(line)
		if err != nil {
			return "", err
		}
		total += number
	}
	return fmt.Sprintf("%d", total), nil
}
