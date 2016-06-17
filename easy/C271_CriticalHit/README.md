# Challenge #271 [Easy] Critical Hit


Critical hits work a bit differently in this RPG. If you roll the maximum value on a die, you get to roll the die again and add both dice rolls to get your final score. Critical hits can stack indefinitely -- a second max value means you get a third roll, and so on. With enough luck, any number of points is possible.


### Input

d -- The number of sides on your die.

h -- The amount of health left on the enemy.

### Output

The probability of you getting h or more points with your die.

### Examples

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

The probability of killing an enemy with health _h_ with a _d_ sided die is equal to 

    _(d - r)/(d<sup>v + 1</sup>)_
    where 
    _v = floor((h - 1)/d)_
    _r = (h - 1) mod d_

### Usage

This was implemented as a command line module, accepting the two parameters _d_ and _h_ as arguments. The module calculates the result as a decimal percentage, but reports the result as a natural percentage for readabilitiy.

    > lua .\CritKillProbCalc.lua 4 5
    25%
    > lua .\CritKillProbCalc.lua 100 200
    0.01%
    > lua .\CritKillProbCalc.lua 8 20
    0.9765625%

### Extra

There are a couple of issues with this system of critical hits. For one, if the player has an item that can only do one point of damage, then every fight is a guarenteed win. This is because all rolls result in a max value for the item, resulting in 100% critical hit chance. Also, the probability of killing an enemy that has a health of _h = d_ is the same as the probability of killing an enemy that has a health of _h = d + 1_.
