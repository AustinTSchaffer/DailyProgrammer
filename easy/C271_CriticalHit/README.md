# Challenge #271 [Easy] Critical Hit


Critical hits work a bit differently in this RPG. If you roll the maximum value on a die, you get to roll the die again and add both dice rolls to get your final score. Critical hits can stack indefinitely -- a second max value means you get a third roll, and so on. With enough luck, any number of points is possible.


### Input

d -- The number of sides on your die.

h -- The amount of health left on the enemy.

### Output

The probability of you getting h or more points with your die.

### Test Cases

| Input: d | Input: h | Output      |
|----------|----------|-------------|
| 4        | 1        | 1           |
| 4        | 4        | 0.25        |
| 4        | 5        | 0.25        |
| 4        | 6        | 0.1875      |
| 1        | 10       | 1           |
| 100      | 200      | 0.0001      |
| 8        | 20       | 0.009765625 |

### Implementation

This challenge was completed with Lua. I chose Lua, because I wanted to learn.

### Usage

Unconfirmed.
