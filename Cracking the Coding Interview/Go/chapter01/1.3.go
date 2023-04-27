package chapter01

import (
	"strings"
)

// URLIfy trims the whitespace from the input string, and replaces the internal spaces
// with `"%20"`.
//
// The result of this function is not actually URL-safe.
func URLIfy(someString string) string {
	someString = strings.TrimSpace(someString)

	return strings.Replace(someString, " ", "%20", -1)
}
