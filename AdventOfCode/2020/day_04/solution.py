#%%

passport_data_plaintext = open("passport_data.txt").readlines()

passports = []

current_passport = {}

for batch_file_line in passport_data_plaintext:
    batch_file_line = batch_file_line.strip()
    if len(batch_file_line) == 0:
        passports.append(current_passport)
        current_passport = {}
    else:
        current_passport.update({
            property_.split(":")[0]: property_.split(":")[1]
            for property_ in batch_file_line.split(" ")
        })

if current_passport:
    passports.append(current_passport)

del current_passport

# %% Part 1

def has_required_fields(passport):
    return (
        "byr" in passport and
        "iyr" in passport and
        "eyr" in passport and
        "hgt" in passport and
        "hcl" in passport and
        "ecl" in passport and
        "pid" in passport
    )

complete_passports = list(filter(has_required_fields, passports))
incomplete_passports = list(filter(lambda pp: not has_required_fields(pp), passports))

print("Part 1:", len(complete_passports))

# %% Part 2

def is_valid(passport):
    """
    Validates a passport that contains all required fields.
    I decided not to use regex for some reason.
    """

    valid_years = (
        (1920 <= int(passport["byr"]) <= 2002) and
        (2010 <= int(passport["iyr"]) <= 2020) and
        (2020 <= int(passport["eyr"]) <= 2030)
    )

    valid_height = (
        (59 <= int(passport["hgt"].replace("in", "")) <= 76)
        if passport["hgt"].endswith("in") else
        (150 <= int(passport["hgt"].replace("cm", "")) <= 193)
    )

    valid_colors = (
        passport["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"] and
        passport["hcl"].startswith("#") and
        len(passport["hcl"]) == 7 and
        all(map(
            lambda char: char in "0123456789abcdef",
            passport["hcl"][1:].lower()
        ))
    )

    valid_pid = (
        len(passport["pid"]) == 9 and
        all(map(
            lambda char: char in "0123456789",
            passport["pid"]
        ))
    )

    return valid_years and valid_height and valid_colors and valid_pid

valid_passports = list(filter(is_valid, complete_passports))

print("Part 2:", len(valid_passports))
