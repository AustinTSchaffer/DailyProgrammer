from typing import List, Iterable

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if len(prices) == 0:
            return 0

        max_profit = 0

        for profit, strategy in self.generate_valid_strategies(prices):
            if profit > max_profit:
                max_profit = profit

        return max_profit


    def profit_from_strategy(self, prices: List[int], strategy: List[int]) -> int:
        profit = 0
        for index, price in enumerate(prices):
            profit += (price * strategy[index])
        return profit


    def generate_valid_strategies(self, prices: List[int]):
        """
        This method has side effects to cut down on memory overhead. Use
        each value from the iterable before asking for the next. Each strategy
        is made of the following actions:

        - `-1` -> Buy (Decrease profit)
        - `1` -> Sell (Increate profit)
        - `0` -> Cooldown (do nothing)
        """

        strategy_length = len(prices)

        # valid_next_action[state] -> [(allowed_action, next_state), ...]
        # state -> (have_cooled_down, holding_stock)
        valid_next_action = {
            (True, True): [
                (0, (True, True)),
                (1, (False, False)),
            ],
            (True, False): [
                (0, (True, False)),
                (-1, (True, True)),
            ],
            (False, True): [
                (0, (True, True)),
            ],
            (False, False): [
                (0, (True, False)),
            ],
        }

        strategy = [0] * strategy_length

        def adjust_strategy(profit, prev_state, start_index):
            if start_index >= (strategy_length):
                yield profit, strategy
                return

            for action, state in valid_next_action[prev_state]:
                strategy[start_index] = action

                yield from adjust_strategy(profit + (action * prices[start_index]), state, start_index+1)

        yield from adjust_strategy(0, (True, False), 0)

if __name__ == "__main__":
    sln = Solution()
    input_ = [1,2,4]
    output = sln.maxProfit(input_)
    print(f"Solution().maxProfit({input_}) -> {output}")

    input_ = [48,12,60,93,97,42,25,64,17,56,85,93,9,48,52,42,58,85,81,84,69,36,1,54,23,15,72,15,11,94]
    output = sln.maxProfit(input_)
    print(f"Solution().maxProfit({input_}) -> {output}")
