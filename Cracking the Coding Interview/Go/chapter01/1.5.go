package chapter01

import (
	"reflect"
	"strings"
	"unicode/utf8"
)

/*

OneAway returns true if it only takes the addition, removal, or replacement of a
single `rune` to transform s1 into s2.

*/
func OneAway(s1 string, s2 string) bool {

	// Identical strings should be "0 away"
	if reflect.DeepEqual(s1, s2) {
		return false
	}

	// Using TrimLeftFunc to remove letters from the beginning of s1 and s2
	// simultaneously, until a non-matching rune is found.
	s1 = strings.TrimLeftFunc(s1, func(nextInS1 rune) bool {
		firstInS2, runeSize := utf8.DecodeRuneInString(s2)
		if firstInS2 == nextInS1 {
			s2 = s2[runeSize:]
			return true
		}
		return false
	})

	// Using TrimRightFunc to remove letters from the beginning of s1 and s2
	// simultaneously, until a non-matching rune is found.
	s1 = strings.TrimRightFunc(s1, func(nextInS1 rune) bool {
		lastInS2, runeSize := utf8.DecodeLastRuneInString(s2)
		if lastInS2 == nextInS1 {
			s2 = s2[:runeSize]
			return true
		}
		return false
	})

	return utf8.RuneCountInString(s1) <= 1 && utf8.RuneCountInString(s2) <= 1
}
