# %% Read ./data/mersenne_prime.txt

import number_labels

print("Reading ./data/mersenne_prime.txt")
mersenne_prime_digits = open("./data/mersenne_prime.txt").read().strip()

# %% Split the mersenne prime into groups of 3, starting from the least significant digits.

print("Splitting prime into groups of 3")
mersenne_prime_terms_reversed = [
    int("".join((
        mersenne_prime_digits[index - 2] if (index - 2) >= 0 else "",
        mersenne_prime_digits[index - 1] if (index - 1) >= 0 else "",
        mersenne_prime_digits[index] if index >= 0 else "",
    )))
    for index in range(len(mersenne_prime_digits) - 1, -1, -3)
]

# %% Label each numeric group

print("Labelling each numeric group")
mersenne_prime_labelled_reversed = [
    number_labels.triple_name(term) + " " + number_labels.number_label(term_number)
    for term_number, term in enumerate(mersenne_prime_terms_reversed)
    if term != 0
]

# %% Write ./data/mersenne_prime_labelled.txt

print("Writing ./data/mersenne_prime_labelled.txt")
with open("./data/mersenne_prime_labelled.txt", "w") as output_file:
    for labelled_term in reversed(mersenne_prime_labelled_reversed):
        output_file.write(labelled_term)
        output_file.write("\n")
        output_file.flush()

print("Done.")

# %%
