# %%

import re
policy_password_pairs_plaintext = open("policy-password-pairs.txt").readlines()

#%% Part 1

policy_password_pairs_interpreter = (
    re.compile(
        r'(?P<policy_min>\d+)-(?P<policy_max>\d+) (?P<password_letter>.): (?P<password>.+)\n'
    )
)

valid_policy_password_pairs = [
    policy_password_pair
    for policy_password_pair, parsed_ppp in (
        (_policy_password_pairs, policy_password_pairs_interpreter.match(_policy_password_pairs))
        for _policy_password_pairs in
        policy_password_pairs_plaintext
    )
    if (
        int(parsed_ppp["policy_min"])
        <= parsed_ppp["password"].count(parsed_ppp["password_letter"])
        <= int(parsed_ppp["policy_max"])
    )
]

print("Part 1:", len(valid_policy_password_pairs))

# %%

new_policy_password_pairs_interpreter = (
    re.compile(
        r'(?P<position_1>\d+)-(?P<position_2>\d+) (?P<password_letter>.): (?P<password>.+)\n'
    )
)

valid_policy_password_pairs = [
    policy_password_pair
    for policy_password_pair, parsed_ppp in (
        (_policy_password_pairs, new_policy_password_pairs_interpreter.match(_policy_password_pairs))
        for _policy_password_pairs in
        open("policy-password-pairs.txt").readlines()
    )
    if (
        (parsed_ppp["password"][int(parsed_ppp["position_1"]) - 1] == parsed_ppp["password_letter"])
        + (parsed_ppp["password"][int(parsed_ppp["position_2"]) - 1] == parsed_ppp["password_letter"])
        == 1
    )
]

print("Part 2:", len(valid_policy_password_pairs))
