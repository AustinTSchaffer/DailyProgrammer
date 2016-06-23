"""
File:     GeneticAlgorithms.py
Author:   Austin Schaffer
Email:    schaffer.austin.t@gmail.com
Github:   http://github.com/AustinTSchaffer

Since:    2016-06-22
Modified: 2016-06-22

Description:
Contains functions and structures used to perform operations on generations
of strings in an attempt to recreate an input character sequence.
"""


import MutatingString as MS


def hammingDistance(strA, strB):

    """ Determines the bitwise Hamming Distance between two strings. Used to
    determine the fitness of a mutating string against the input.

    Example:
        bin(ord('a'))                       == '0b1100001'
        bin(ord('9'))                       == '0b0111001'
        bin(ord('a') ^ ord('9'))            == '0b1011000' 
        bin(ord('a') ^ ord('9')).count('1') == 3
        hammingDistance('a', '9')           == 3
        hammingDistance('a', '9') * 4       == 12
        hammingDistance('aaaa', '9999')     == 12

    Args:
        strA: A string
        strB: A string
    Returns:
        Returns an integer that represents the Hamming Distance from a to b.
    Raises:
        ValueError: If the two strings are unequal in length or if one input is
        not a string.
    """
    
    if (not isinstance(strA, basestring) or not isinstance(strB, basestring)):
        raise ValueError('Input is not a string', valueA, valueB)

    if len(strA) != len(strB):
        raise ValueError('The two strings are unequal in length', strA, strB)

    # base case, hamming distance of nothing and nothing is 0
    if (len(strA) == 0) and (len(strB) == 0):
        return 0
    
    # XOR both first characters, count the 1s, remaining is recursive case
    return (bin(ord(strA[0]) ^ ord(strB[0])).count('1') + 
                hammingDistance(
                    (strA[1:] if (len(strA) > 1) else ''),
                    (strB[1:] if (len(strB) > 1) else '')
                )
            )
