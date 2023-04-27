package chapter01

/*

LetterHistogram generates a map from rune to int, mapping every distinct rune
from the input string to the number of times it appears in the string.

*/
func LetterHistogram(someString string) map[rune]int {
	letterFreq := make(map[rune]int)
	for _, runeValue := range someString {
		letterFreq[runeValue]++
	}
	return letterFreq
}

/*

IsUnique returns true if all of the runes in a given string are unique, making
no considerations for punctuation, mixed-case character strings, and whitespace.

*/
func IsUnique(someString string) bool {
	h := LetterHistogram(someString)
	for _, v := range h {
		if v > 1 {
			return false
		}
	}
	return true
}
