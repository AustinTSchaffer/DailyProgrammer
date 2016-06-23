

mDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def answer(x, y, z):
    
    answers = [
        AnAnswer(x, y, z), 
        AnAnswer(x, z, y),
        AnAnswer(y, x, z),
        AnAnswer(y, z, x),
        AnAnswer(z, x, y),
        AnAnswer(z, y, x)
    ]

    validAnswers = []
    
    for answer in answers:
        if (answer.verify()):
            
            add = True

            for va in validAnswers:
                if (answer.equals(va)):
                    add = False
            
            if add:
                validAnswers.append(answer)

    if len(validAnswers) == 1:
        va = validAnswers[0]
        return '{:02d}/{:02d}/{:02d}'.format(va.mm, va.dd, va.yy)
    
    return 'Ambiguous'


class AnAnswer():

    def __init__(self, mm, dd, yy):
        self.mm = mm
        self.dd = dd
        self.yy = yy

    def verify(self):

        if not (self.mm - 1) in range(12):
            return False
        
        febMod = 1 if self.yy % 4 == 0 else 0

        if not ((self.dd - 1) in 
            range(mDays[self.mm - 1] + (febMod if self.mm == 2 else 0))
        ):
            return False
        
        return True

    def equals(self, other):
        return (
            self.mm == other.mm and
            self.dd == other.dd and
            self.yy == other.yy
        )

