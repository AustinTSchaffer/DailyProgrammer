# Postmortem

Last Updated: January 26, 2018

Looking back on this challenge, there is a lot I would have changed and not 
much that I would keep the same. This document outlines some of the issues 
that I have looking back on my old code. 


## Permutations

```python
def answer(x, y, z):
    
    answers = [
        AnAnswer(x, y, z), 
        AnAnswer(x, z, y),
        AnAnswer(y, x, z),
        AnAnswer(y, z, x),
        AnAnswer(z, x, y),
        AnAnswer(z, y, x)
    ]

    # ...
```

I like that I made a class that encapsulated a potential answer, but I don't 
like that the `answer(x,y,z)` function has hard-coded the "generate all 
permutations" step. If it had better permutation generation, then the part of 
the code that verifies each potential answer would only have to run once for 
each distinct permutation.

I'm not really sure if the scope of this challenge warrants something as 
complicated as a distinct permutation generator, since there are only 3 
components to a Year-Month-Day-style date. I'd say that once you hit 4 
options, it would be smart to expand that part of the logic. 

## Encapsulation and Validation

What's the number of days in each month doing all the way up there in the top 
of the file? It's not like that changes.

Also, why even have that? I bet there's a date class that I could have used 
too... yep, just checked. Why reinvent the wheel on things like leap years and 
month number calculations?

## Validation 

Oh, geez.

```python
validAnswers = []

for answer in answers:
    if (answer.verify()):
        
        add = True

        for va in validAnswers:
            if (answer.equals(va)):
                add = False
        
        if add:
            validAnswers.append(answer)
```

Once I fell in love with C#'s LINQ, I wanted every programming language to 
work that way. Clearly, Microsoft got that right. Well, someone got it right. 
I wonder where the inspiration for LINQ came from...

Anyway, there's definitely a better way to do this.

## Documentation

None of the methods have contracts, nothing is written down. There's not a lot 
of code here, but I still think it's important to document a method whose name 
is so unclear, such as `answer()`. 
