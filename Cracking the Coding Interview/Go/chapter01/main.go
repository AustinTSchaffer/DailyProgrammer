package chapter01

import (
	"fmt"
)

/*

Main runs example usages for all of the functions and types contained in this
package.

*/
func Main() {
	fmt.Println("Testing IsUnique")
	fmt.Println(IsUnique("test"))

	fmt.Println("Testing StringsArePermutations")
	fmt.Println(StringsArePermutations("tes", "ste"))
	fmt.Println(StringsArePermutations("tes", "test"))
	fmt.Println(StringsArePermutations("test", "test"))

	fmt.Println("Testing URLIfy")
	fmt.Println(URLIfy("Luke, I am your father       "))

	fmt.Println("Testing IsAPermutationOfAPalindrome")
	fmt.Println(IsAPermutationOfAPalindrome("aabbcccddee"))
	fmt.Println(IsAPermutationOfAPalindrome("aabbCcddddEeFfGgGgGGggggg"))
	fmt.Println(IsAPermutationOfAPalindrome("aabbCcddddEeFfgGgGGgggggX"))
	fmt.Println(IsAPermutationOfAPalindrome("aabbCcddddEeFfgGgGGgggggXYYY"))

	fmt.Println("Testing OneAway")
	fmt.Println(OneAway("asdf", "asdf"))
	fmt.Println(OneAway("adf", "asdf"))
	fmt.Println(OneAway("asddf", "asdf"))
	fmt.Println(OneAway("addf", "asdf"))

	fmt.Println("Testing MatrixRotate")
	main1dot7()
}
