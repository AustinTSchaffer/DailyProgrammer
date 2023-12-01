input = [
    line.strip() for line in open("input.txt", "r").readlines()
]

sample_input = [
    line.strip() for line in open("sample_input.txt", "r").readlines()
]

import re

firstnumber_re = re.compile(r"^[^\d]*(\d).*$")
lastnumber_re = re.compile(r"^.*(\d)[^\d]*$")

total = 0

for line in input:
    fnm = firstnumber_re.match(line)
    lnm = lastnumber_re.match(line)
    total += int(fnm[1] + lnm[1])

print(total)

total = 0

number_names = ["one","two","three","four","five","six","seven","eight","nine"]

for line in input:
    fnm = firstnumber_re.match(line)

    first_named_number = ""
    first_index_of_named_number = len(line) + 1
    for name in number_names:
        idx = line.find(name)
        if idx != -1 and idx < first_index_of_named_number:
            first_named_number = name
            first_index_of_named_number = idx

    if fnm is None or first_index_of_named_number < fnm.span(1)[0]:
        first_number = number_names.index(first_named_number) + 1
    else:
        first_number = fnm[1]

    lnm = lastnumber_re.match(line)

    last_named_number = ""
    last_index_of_named_number = -1
    for name in number_names:
        reversed_name = "".join(reversed(name))
        reversed_line = "".join(reversed(line))
        idx = reversed_line.find(reversed_name)
        if idx != -1:
            idx = len(line) - idx - len(name)
            if idx > last_index_of_named_number:
                last_named_number = name
                last_index_of_named_number = idx
    
    if lnm is None or last_index_of_named_number > lnm.span(1)[0]:
        last_number = number_names.index(last_named_number) + 1
    else:
        last_number = lnm[1]

    total += int(str(first_number) + str(last_number))

print(total)
