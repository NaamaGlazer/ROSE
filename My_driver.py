from rose.common import obstacles, actions  # NOQA

driver_name = "Lane Switcher"

# Define the hard obstacles
hard_obstacles = {obstacles.BIKE, obstacles.BARRIER, obstacles.TRASH}

def obstacles_(car_x, car_y, world):
    try:
        # Check for hard obstacles in front of the car
        if world.get((car_x, car_y - 1)) in hard_obstacles:
            # If the car is in the leftmost lane, move right
            if car_x == 0:
                return actions.RIGHT
            # If the car is in the rightmost lane, move left
            elif car_x == 2:
                return actions.LEFT
            # If the car is in the middle lane, prefer to move right
            else:
                return actions.RIGHT
    except IndexError:
        # Handle out of bounds
        return actions.NONE
    return actions.NONE

def drive(world):
    car_x = world.car.x
    car_y = world.car.y

    # Handle lane switching for hard obstacles
    lane_switch_action = obstacles_(car_x, car_y, world)
    if lane_switch_action != actions.NONE:
        return lane_switch_action

    # Handle soft obstacles
    soft_obstacle_action = handle_soft_obstacles(world, car_x, car_y)
    if soft_obstacle_action:
        return soft_obstacle_action

    return actions.NONE

def handle_soft_obstacles(world, car_x, car_y):
    try:
        obstacle = world.get((car_x, car_y - 1))
        if obstacle == obstacles.WATER:
            return actions.BRAKE
        elif obstacle == obstacles.CRACK:
            return actions.JUMP
        elif obstacle == obstacles.PENGUIN:
            return actions.PICKUP
    except IndexError:
        return actions.NONE
    return False
