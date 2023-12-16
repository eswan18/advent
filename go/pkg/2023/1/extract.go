package y2023d1

import "fmt"

func extractDigits(line string) (int, error) {
	// Get all digits from the line
	digits := []int{}
	for _, r := range line {
		if r >= '0' && r <= '9' {
			digits = append(digits, int(r-'0'))
		}
	}
	if len(digits) == 0 {
		return 0, fmt.Errorf("no digits in line")
	}
	number := digits[0]*10 + digits[len(digits)-1]
	return number, nil
}
