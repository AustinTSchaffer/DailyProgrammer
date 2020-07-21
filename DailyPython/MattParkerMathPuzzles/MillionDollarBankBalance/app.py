from typing import Iterable, List, Tuple


WINNING_BALANCE = 1_000_000


def simulate_bank_balance(deposit1: int, deposit2: int) -> Iterable[int]:
    """
    Simulates the following proposal:

    You can make two deposits (of integer pounds) on two consecutive days and
    everyday the bank will add your last two balances together to give you a new
    balance.

    For example:
    - You deposit £10 on day 1.
    - You deposit £20 on day 2.
    
    Your balance on:
    - day 1 would be £10
    - day 2 would be £30
    - day 3 would be £40
    - day 4 would be £70
    """

    prev_balance = 0
    curr_balance = deposit1

    yield curr_balance

    prev_balance = curr_balance
    curr_balance += deposit2

    while True:
        yield curr_balance

        temp = prev_balance
        prev_balance = curr_balance
        curr_balance += temp


def test_simulate_bank_balance():
    simulator = simulate_bank_balance(10, 20)
    assert next(simulator) == 10
    assert next(simulator) == 30
    assert next(simulator) == 40
    assert next(simulator) == 70
    assert next(simulator) == 110


def simulate_competition_entry(deposit1: int, deposit2: int, threshhold: int) -> (bool, List[int]):
    """
    Simulates the following proposition:

    A bank is running a competition. You can make two deposits (of integer
    pounds) on two consecutive days and everyday the bank will add your last two
    balances together to give you a new balance.

    For example: You deposit £10 on day 1 and £20 on day 2. Your balance on day
    1 would be £10, day 2 £30, day 3 £40, day 4 £70 and so on.....

    You can keep the money if your balance eventually equals one million pounds
    exactly. If more than one person hits a million exactly, the prize goes to
    the person who took the longest to get there.

    This function, given the necessary 2 deposits, returns a tuple where [0] is
    a bool that shows whether the balance ever exactly equaled the threshold and
    [1] shows the account balance history.
    """

    bank_balance_simulation = simulate_bank_balance(deposit1, deposit2)

    balance_history = []
    balance = 0
    while balance < threshhold:
        balance = next(bank_balance_simulation)
        balance_history.append(balance)

    can_they_keep_the_money = (balance == threshhold)
    return can_they_keep_the_money, balance_history


def generate_distinct_integer_pairs() -> Iterable[Tuple[int, int]]:
    """
    Returns an iterable of distinct positive integer pairs, starting with (0,1).
    No entries will ever be repeated. The 2 integers will be ordered low-high.

    Skips (0,0).
    """

    higher_number = 1
    while True:
        for lower_number in range(higher_number + 1):
            yield (lower_number, higher_number)
        higher_number += 1


def test_generate_distinct_integer_pairs():
    generator = generate_distinct_integer_pairs()

    assert next(generator) == (0,1)
    assert next(generator) == (1,1)
    assert next(generator) == (0,2)
    assert next(generator) == (1,2)
    assert next(generator) == (2,2)
    assert next(generator) == (0,3)
    assert next(generator) == (1,3)
    assert next(generator) == (2,3)
    assert next(generator) == (3,3)
    assert next(generator) == (0,4)


class WinningResult:
    def __init__(self, deposit1: int, deposit2: int, balance_history: list):
        self.deposit1 = deposit1
        self.deposit2 = deposit2
        self.balance_history = balance_history

    def __repr__(self) -> str:
        return f"WinningResult({self.deposit1}, {self.deposit2}, {self.balance_history})"


def generate_winning_results(winning_balance: int) -> Iterable[WinningResult]:
    """
    Simulates the following proposition:

    A bank is running a competition. You can make two deposits (of integer
    pounds) on two consecutive days and everyday the bank will add your last two
    balances together to give you a new balance.

    For example: You deposit £10 on day 1 and £20 on day 2. Your balance on day
    1 would be £10, day 2 £30, day 3 £40, day 4 £70 and so on.....

    You can keep the money if your balance eventually equals one million pounds
    exactly. If more than one person hits a million exactly, the prize goes to
    the person who took the longest to get there.

    This function generates an iterable over all possible solutions to this
    problem given 2 starting positive integer pairs.
    """

    for integer_pair in generate_distinct_integer_pairs():
        is_winning_entry, balance_history = simulate_competition_entry(*integer_pair, winning_balance)

        if is_winning_entry:
            yield WinningResult(*integer_pair, balance_history)

        if len(balance_history) <= 2:
            # The script has reached the end of non-trivial solutions
            break

    return


if __name__ == '__main__':
    print('DEPOSIT_1,DEPOSIT_2,NUM_DAYS')
    for i, result in enumerate(generate_winning_results(WINNING_BALANCE)):
        print(f"{result.deposit1},{result.deposit2},{len(result.balance_history)}")
