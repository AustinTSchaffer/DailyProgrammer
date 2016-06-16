function critKillProbCalc(maxDam, health)
	
	local overflow = -1
	local remain = -1

	if health > maxDam then
		overflow = math.floor(health/maxDam)
		remain = health % maxDam
	else
		overflow = 0
		remain = health
	end
	
	-- TODO
end

critKillProbCalc(arg[1], arg[2])
