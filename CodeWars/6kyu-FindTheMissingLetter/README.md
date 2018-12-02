# Find the missing letter

Write a method that takes an array of consecutive (increasing) letters as input
and that returns the missing letter in the array.

You will always get an valid array. And it will be always exactly one letter be
missing. The length of the array will always be at least 2. The array will
always contain letters in only one case.

Assumes the English alphabet with 26 letters.

## Example

```python
['a','b','c','d','f'] -> 'e'
['O','Q','R','S'] -> 'P'
```

## Python Solution

This Kata describes that the english alphabet should be assumed. I decided to
add support for arbitrary alphabets, just for fun. Other than that, the solution
uses a pretty simple iteration through the alphabet, in tandem with the input
characters, and returns the first letter in the alphabet that does not match the
current character of the input characters.

Bonus points for duck typing, because the `find_missing_letter` function can
take either an array of single characters, or a regular string.
