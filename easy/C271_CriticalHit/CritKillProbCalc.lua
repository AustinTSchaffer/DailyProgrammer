
function critKillProbCalc(d, h)
	
	local v = math.floor((h - 1) / d) -- Overflow
	local r = (h - 1) % d             -- Remainder

	return (d - r) / (d ^ (v + 1))
end

print(100*critKillProbCalc(arg[1], arg[2]) .. "%")
