"""
File:     GeneticAlgorithms.py
Author:   Austin Schaffer
Email:    schaffer.austin.t@gmail.com
Github:   http://github.com/AustinTSchaffer

Since:    2016-06-22
Modified: 2016-06-25

Description:
Contains functions and structures used to perform operations on generations
of strings in an attempt to recreate an input character sequence.
"""

from MutatingString import MutatingString
from datetime import datetime

import random

generationSize = 50
generationProp = 5

def generate(goal):
    """ Runs a genetic simulation in order to obtain the goal

    Args:
        goal: desired goal string
    Returns:
        Returns a 3 column table recording a summary of the evolution. Each row
        in the table will include the top 5, most fit members of the generation
        along with their fitnesses.
        [
            [[fitness, string], [same], [same], [same], [same]], #gen0
            [[firness, string], [same], [same], [same], [same]], #gen1

            ...
            
            [[fitness, goal], ... ]                        #genN
        ]

    """
    

    c_gen = []
    summary = []

    for _ in range(generationSize):
        c_gen.append(MutatingString(len(goal)))
    
    c_gen.sort(key=lambda x: hammingDistance(x.genome, goal))
    
    while(c_gen[0].genome != goal):
     
        summary.append(
            [
                hammingDistance(c_gen[0].genome, goal), 
                c_gen[0].genome,
                c_gen[1].genome,
                c_gen[2].genome,
                c_gen[3].genome,
                c_gen[4].genome
            ]
        )
        
        n_gen = []
        n_gen = c_gen[:generationProp]

        c_gen = []
     
        for _ in range(generationSize):
            c_gen.append(random.choice(n_gen).mate(random.choice(n_gen)))

        for member in c_gen:
            member.mutate(hammingDistance(member.genome, goal))

         
        c_gen.sort(key=lambda x: hammingDistance(x.genome, goal))


    return summary


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
        raise ValueError('Input is not a string', strA, strB)

    if len(strA) != len(strB):
        raise ValueError('The two strings are unequal in length', strA, strB)

    # base case, hamming distance of nothing and nothing is 0
    if (len(strA) == 0) and (len(strB) == 0):
        return 0
    
    # XOR both first characters, count the 1s, remaining is recursive case
    return (
        bin(ord(strA[0]) ^ ord(strB[0])).count('1') + 
        hammingDistance(strA[1:], strB[1:])
    )

def charwiseDistance(strA, strB):
    
    """ Determines the number of characters that are different between 
    strA and strB

    Args:
        strA: A string
        strB: A string
    Returns:
        Returns an integer that represents the number of different
        characters between a to b.
    Raises:
        ValueError: If the two strings are unequal in length or if one input is
        not a string.
    """
    
    if (not isinstance(strA, basestring) or not isinstance(strB, basestring)):
        raise ValueError('Input is not a string', strA, strB)

    if len(strA) != len(strB):
        raise ValueError('The two strings are unequal in length', strA, strB)

    # base case, distance from nothing to nothing is 0
    if (len(strA) == 0) and (len(strB) == 0):
        return 0
    
    return (
        (1 if strA[0] != strB[0] else 0) + 
        charwiseDistance(strA[1:], strB[1:])
    )
