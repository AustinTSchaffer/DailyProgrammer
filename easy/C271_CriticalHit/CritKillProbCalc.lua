-- @file        CritKillProbCalc.lua
-- @version     1.0
-- @author      Austin Schaffer
-- @since       2016-06-19
-- @revision    2016-06-12
--
-- This module was implemented as a command line utility, accepting command 
-- line arguments. The module can also be called with dofile or require. If
-- used as a command line utility, it accepts two number arguments. This will
-- output the probability as a percentage, not a decimal.
--
-- Usage:
-- 
-- > lua ./CritKillProbCalc.lua [Die Size] [Enemy HP]
-- [Probabilitiy]%
--
-- Example:
--
-- > lua ./CritKillProbCalc.lua 6 4
-- 50%
-- 
--
-- If the module is called with dofile or require, then its method will output
-- the probability as a decimal.
-- 
-- Usage:
--
-- critKillProbCalc([Die Size], [Enemy HP])
--
-- Example:
--
-- > print(critKillProbCalc(6, 4))
-- 0.5


do
    if (arg ~= nil and arg[-1] ~= nil) then
        print(100*critKillProbCalc(arg[1], arg[2]) .. "%")
    end
end


function critKillProbCalc(d, h)
    -- Calculates the probability of killing an enemy with "h" HP remaining if
    -- the specified critical hit system is used and a single die with "d" 
    -- faces is rolled.
    -- 
    -- Specified Critical Hit System:
    -- If the maximum value of a die is rolled, then the player may roll the
    -- die again and add the result to the running total. The player can
    -- continue rolling a die as long as its maximum value keeps turning up and
    -- the running total is less than the enemy's remaining HP.
    --
    -- Outputs the probabilitiy as a decimal.
    --
    -- @param d Number of faces on a single die.
    -- @param h Numerical HP of enemy.
    -- @return Decimal probabilitiy of a kill.
	
	local v = math.floor((h - 1) / d) -- Overflow
	local r = (h - 1) % d             -- Remainder

	return (d - r) / (d ^ (v + 1))
end
