class Solution:
    def angleClock(self, hour: int, minutes: int) -> float:
        hour_angle_deg = (hour * 30) + (minutes * 0.5)
        minute_angle_deg = minutes * 6
        
        output = abs(hour_angle_deg - minute_angle_deg) % 360
        output = (
            (360 - output)
            if output > 180 else
            output
        )

        print(f"Hour: ({hour} / {hour_angle_deg}) Minute: ({minutes} / {minute_angle_deg}) Diff: ({output})")

        return output
