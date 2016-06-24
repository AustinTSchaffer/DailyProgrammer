"""
File:     MutatingString.py
Author:   Austin Schaffer
Email:    schaffer.austin.t@gmail.com
Github:   http://github.com/AustinTSchaffer

Since:    2016-06-22
Modified: 2016-06-23

Description:
Contains the MutatingString class, which encapsulates a string and methods
used to perform genetic operations on the string.
"""

import string
import random


class MutatingString(object):
    
    """Encapsulates a string and methods used to mutate the string."""


    # Holds all chars available for genome mutations. Static member.
    chars = ''

    # Mutation rate of offspring during mating
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


    def mutate(self, distance = -1, maxDistance = -1):
       
        """ Causes the MutatingString's genome to randomly change. The amount
        the genome changes is proportional to its fitness.

        Args:
            distance: The distance between this MutatingString's genome and the
            input sequence. Defaults to half the number of bits in the
            contained gehammingDistancenome.
            maxDistance: The maximum distance between any string and the input
            sequence. This is dependent on the comparison algorithm used.
            Defaults to the number of bits in the contained genome.
        Returns:
            Returns the new value of this MutatingStrings genome
        """
        
        if len(self.genome) == 0 or self.genome is None:
            return
        
        percentDiff = (
            float(len(self.genome)*4) if distance    == -1 else float(distance) /
            float(len(self.genome)*8) if maxDistance == -1 else float(maxDistance)
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
