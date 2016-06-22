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

    
    def __init__(self, length, chars=string.printable):
        """
        Initializes a mutating string with a random genome.

        Args:
            length: Desired length of the genome (contained string)

            chars: A string representing all of the different characters
            available to MutatingStrings. (defaults to string.printable)
        """

        MutatingString.chars = chars

        self.genome = ''.join(random.SystemRandom().choice(
            MutatingString.chars) for _ in range(length))


    def mutate(self, fitness=0.5):
        """ Causes the MutatingString's genome to randomly change. The amount
        the genome changes is proportional to its fitness. Fitness is equal to
        1 - (HD(self.genome, input) / len(self.genome)*8).

        Args:
            fitness: The fitness of the MutatingString against the input.
            Defaults to 50 percent.
        """

        # TODO

    def mate(mutatingString):
        """ Creates an offspring MutatingString by mating with another
        MutatingString. The offspring will inherit one half of its genome from
        each parent, randomly, character by character.

        Args:
            mutatingString: Another mutating string
        Returns:
            Returns an offspring of self and other.
        """
        # TODO

        return MutatingString(len(self.genome), MutatingString.chars)
    
    

def hammingDistance(stringA, stringB):
    """ Determines the bitwise Hamming Distance between two strings. Used to
    determine the fitness of a mutating string against the input.

    Example:
        bin(ord('a'))                       == '0b1100001'
        bin(ord('9'))                       == '0b0111001'
        bin(ord('a') ^ ord('9'))            == '0b1011000' 
        bin(ord('a') ^ ord('9')).count('1') == 3
        3 * len('aaaa')                     == 12
        hammingDistance('aaaa', '9999')     == 12

    Args:
        stringA: A string
        stringB: A string
    Returns:
        Returns an integer that represents the Hamming Distance from a to b.
    """

    if (len(stringA) == 0) and (len(stringB) == 0):
        return 0
    
    a = 0 if (len(stringA) == 0) else ord(stringA[0])
    b = 0 if (len(stringB) == 0) else ord(stringB[0])

    return (bin(a ^ b).count('1') + 
                hammingDistance(
                    (stringA[1:] if (len(stringA) > 1) else ''),
                    (stringB[1:] if (len(stringB) > 1) else '')
                )
            )
