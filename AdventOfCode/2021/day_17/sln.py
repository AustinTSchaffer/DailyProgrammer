# target area: x=241..275, y=-75..-49

# The max Y velocity going up should be roughly equal to the max
# velocity that would overshoot the target area after one unit of
# time. The max velocity going up is 2 less than the absolute
# value of that downward velocity:
#
# - 1 less to make sure its in bounds
# - another 1 less to account for the additional increase in
#   velocity due to gravity
#
# Therefore, the max height is the sum of all the integers up
# to (and including) that velocity.
#
# For my problem input, this means that the max velocity going
# up is 74 units/time, so my Part 1 answer is sum(range(75)).
#
# Basically no code for Part 1. I did most of the working-out
# using Desmos, an online graphing tool, plus trial and error.

MIN_Y_VEL = -75
MAX_Y_VEL = 74

print("Part 1:", sum(range(MAX_Y_VEL + 1)))

# Finding the minimum and maximum X velocity follows the same
# logic. 23 is the minimum starting X velocity because any
# lower would never reach the minimum X position of the target
# area. This value was found by checking sum(range(X)) until
# X was inside the target area, and X-1 was outside.
# 
# Max X velocity is 275, because any higher overshoots the
# target area after 1 iteration.

MIN_X_VEL = 23
MAX_X_VEL = 275

starting_position = (0, 0)
target_area_x_range = tuple(sorted((241, 275)))
target_area_y_range = tuple(sorted((-75, -49)))

def in_bounds(position):
    return (
        position[0] >= target_area_x_range[0] and
        position[0] <= target_area_x_range[1] and
        position[1] >= target_area_y_range[0] and
        position[1] <= target_area_y_range[1]
    )

def overshot(position):
    return (
        position[0] > target_area_x_range[1] or
        position[1] < target_area_y_range[0]
    )

def step(position, velocity):
    position = (position[0] + velocity[0], position[1] + velocity[1])
    velocity = (max(0, velocity[0] - 1), velocity[1] - 1)
    return position, velocity

if __name__ == "__main__":
    valid_initial_velocities = []
    # I apparently got my reasoning slightly wrong earlier but increasing
    # these worked and luckily the simulation didn't take too long.
    for x_vel in range(MIN_X_VEL - 10, MAX_X_VEL + 10):
        for y_vel in range(MIN_Y_VEL - 10, MAX_Y_VEL + 10):
            position = (0, 0)
            velocity = (x_vel, y_vel)
            while not in_bounds(position) and not overshot(position):
                position, velocity = step(position, velocity)
            if in_bounds(position):
                valid_initial_velocities.append((x_vel, y_vel))
    print("Part 2:", len(valid_initial_velocities))
