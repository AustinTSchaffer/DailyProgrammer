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

good_pps = list(filter(has_required_fields, passports))
bad_pps = list(filter(lambda pp: not has_required_fields(pp), passports))

print("Part 1:", len(good_pps))

# %%
