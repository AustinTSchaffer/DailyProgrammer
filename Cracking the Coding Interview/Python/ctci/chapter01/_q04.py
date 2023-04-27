def palindrone_permutation(some_string: str) -> bool:
    """

    Returns `True` if the input string is a permutation of a palindrome, meaning
    the string can be rearranged into a palindrome. Only takes alphabet
    characters into consideration.

    Palindromes are sequences of letters that are identical forwards and
    backwards, ignoring spaces and punctuation. Permutations of palindromes
    don't necessarily have the same property, but you can determine whether or
    not it can be turned into a palindrome by counting how many letters appear
    an odd number of times.

    - If 0 letters appear an odd number of times, then its possible to pair up
      all letters, reflected across the midpoint of the sequence.
    - If 1 letter appears an odd number of times, that letter will appear
      exactly in the midpoint of the sequence, with all other alpha-characters
      paring up reflected across the midpoint of the sequence.
    - If 2 or more letters appear an odd number of times, then you will have at
      least 2 letters that cannot be paired up with any other letters. Given
      that you can only have 1 mismatched letter in a palindrome (the element at
      the very center of a sequence that has an odd length), you cannot have
      more than one.

    It's possible to calculate this by grouping the letters into a dict, where
    the letter maps to the number of times it appears in the sequence. This
    solution requires the data to be iterated twice. It's possible to instead
    iterate only once over the data by keeping a `set` of the letters that are
    mismatched, meaning a set that contains the letters that have appeared an
    odd number of times so far. Once the end of the string has been reached, the
    only assertion that needs to be made would be to calculate the length of the
    set.

    """

    mismatched_letters = set()

    for letter in some_string:
        if str.isalpha(letter):
            lower_letter = str.lower(letter)
            if lower_letter in mismatched_letters:
                mismatched_letters.remove(lower_letter)
            else:
                mismatched_letters.add(lower_letter)

    return len(mismatched_letters) <= 1
