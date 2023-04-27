package chapter01

import (
	"strings"
	"unicode"
)

/*

IsAPermutationOfAPalindrome returns true if the input string can be rearranged
to form a palindrome.

Palindromes can only be formed if there is 0 or 1 letters that occur and odd
number of times. If there are 2 or more letters that occur an odd number of
times, then if you pair off all of the remaining letters, you end up with more
that 1 letter that cannot be paired. For example, in a case where you have and
even number of each letter `a` through `x`, and have an odd number of `y`s and
an odd number of `z`s, then you end up in the following situation:

`"abbcccdddd...(y)(z) ? (z)(y)...ddddcccbba"`

where you have to fill in `?` with 1 `y` and 1 `z`, resulting in an asymmetric
string of characters, which opposes the definition of a palindrome.

*/
func IsAPermutationOfAPalindrome(someString string) bool {
	letters := make(map[rune]int)

	for _, letter := range strings.ToLower(someString) {
		if unicode.IsLower(letter) {
			letters[letter]++
		}
	}

	numberOfOddLetters := 0
	for _, count := range letters {
		if count%2 == 1 {
			if numberOfOddLetters > 0 {
				return false
			}
			numberOfOddLetters++
		}
	}

	return true
}
