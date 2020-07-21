import itertools
from datetime import date


def answer(x, y, z):
    # Determines if any permutation of integers x,y,z 
    # can be resolved to a valid date. If one is found,
    # the date is output in the format mm/dd/yy. Otherwise,
    # the method returns "Ambiguous".

    answers = [ 
        # Output Format
        '{:02d}/{:02d}/{:02d}'.format(p[0], p[1], p[2]) 

        # Permutation Generation
        for p in set(itertools.permutations([x, y, z])) 

        # Condition
        if validDate(p[0], p[1], p[2])
    ]

    return answers[0] if len(answers) == 1 else 'Ambiguous'


def validDate(mm, dd, yyyy):
    # Returns true if the input
    # that constitutes a valid yyyy/mm/dd style date.

    try:
        date(
            int(yyyy),
            int(mm), 
            int(dd)
        )

    except ValueError:
        return False
    return True
