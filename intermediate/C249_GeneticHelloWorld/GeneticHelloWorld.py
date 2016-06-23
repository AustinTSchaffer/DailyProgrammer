"""
File:     GeneticHelloWorld.py
Author:   Austin Schaffer
Email:    schaffer.austin.t@gmail.com
Github:   http://github.com/AustinTSchaffer

Since:    2016-06-22
Modified: 2016-06-22

Description:
Contains modules to satisfy the intermediate challenge numbered C249.
Implements a genetic algorithm for the purposes of recreating an input string
using random mutations.
"""


import string
import random


class MutatingString(object):
    
    """Encapsulates a string and methods used to mutate the string."""


    # Holds all chars available for mutations for this. Static member.
    chars = ''
    childMutRate = 0.005

    
    def __init__(self, length, chars=string.printable):
        
        """ Initializes a mutating string with a random genome.

        Args:
            length: Desired length of the genome (contained string)

            chars: A string representing all of the different characters
            available to MutatingStrings. Defaults to string.printable
        """

        MutatingString.chars = chars

        self.genome = ''.join(random.SystemRandom().choice(
            MutatingString.chars) for _ in range(length))


    def mutate(self, hammingDistance = -1):
       
        """ Causes the MutatingString's genome to randomly change. The amount
        the genome changes is proportional to its fitness.

        Args:
            hammingDistance: The Hamming Distance from this MutatingString
            to the desired input string. Defaults to half the maximum distance,
            0.5 times the number of bits. Assumes 8-bit chars.
        Returns:
            Returns the new value of this MutatingStrings genome
        """
        
        if len(self.genome) == 0 or self.genome is None:
            return
        
        percentDiff = (
            0.5 if hammingDistance == -1 else
            float(hammingDistance) / float(len(self.genome) * 8.0)
        )

        newGenome = []

        for i in range(len(self.genome)):
            newGenome.append(
                random.SystemRandom().choice(MutatingString.chars)
                if random.uniform(0,1) < percentDiff
                else self.genome[i]
            )
        
        self.genome = ''.join(newGenome)
        
        return self.genome


    def mate(self, mStr):
        
        """ Creates an offspring MutatingString by mating with another
        MutatingString. The offspring will inherit one half of its genome from
        each parent, randomly, character by character.

        Args:
            mStr: Another mutating string
        Returns:
            Returns an offspring of self and other.
        Raises:
            ValueError: If the two input strings are not the same length.
        """

        if len(self.genome) != len(mStr.genome):
            raise ValueError('The two strings are unequal in length', 
                self.genome, 
                mStr.genome)

        offspring = MutatingString(len(self.genome), MutatingString.chars)
        
        newGenome = []

        for i in range(len(self.genome)):
            newGenome.append( 
                random.choice(MutatingString.chars)
                if random.uniform(0,1) <= MutatingString.childMutRate
                else  self.genome[i]
                if random.uniform(0,1) <= 0.5
                else mStr.genome[i]
            )
        
        offspring.genome = ''.join(newGenome)
        return offspring
    

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
