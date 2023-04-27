package chapter01

import (
	"strconv"
	"unicode/utf8"
)

/*

StringCompression replaces repeated characters in the input string with that
repeated character and a number. If this compression ends up being longer than
the original string, then the original string is returned.

*/
func StringCompression(uncompressed string) string {
	compressedBuilder := make([]byte, 0)
	currentCount := 0
	currentRune, _ := utf8.DecodeRuneInString(uncompressed)

	for _, r := range uncompressed {
		if r == currentRune {
			currentCount++
		} else {
			strconv.AppendQuoteRune(compressedBuilder, currentRune)
			strconv.AppendInt(compressedBuilder, int64(currentCount), 10)
			currentCount = 0
			currentRune = r
		}
	}

	compressed := string(compressedBuilder)

	if utf8.RuneCountInString(compressed) <= utf8.RuneCountInString(uncompressed) {
		return compressed
	}

	return uncompressed
}
