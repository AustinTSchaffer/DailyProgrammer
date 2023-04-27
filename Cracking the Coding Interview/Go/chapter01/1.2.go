package chapter01

import "reflect"

/*

StringsArePermutations returns `true` if the `LetterHistogram` of s1 matches the
`LetterHistogram` of s2.

*/
func StringsArePermutations(s1 string, s2 string) bool {
	return reflect.DeepEqual(
		LetterHistogram(s1),
		LetterHistogram(s2),
	)
}
