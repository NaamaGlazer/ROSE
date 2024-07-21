"""
This driver does not do any action.
"""

from rose.common import obstacles, actions  # NOQA

driver_name = "No Driver"

hard_obstacles = set([obstacles.BIKE, obstacles.BARRIER, obstacles.TRASH])


def drive(world):
    car_x = world.car.x
    car_y = world.car.y
    soft_obstacle_action = handle_soft_obstacles(world, car_x, car_y)
    if soft_obstacle_action:
        return soft_obstacle_action
    return actions.NONE


def handle_soft_obstacles(world, car_x, car_y):
    match world.get((car_x, car_y)):
        case obstacles.WATER:
            return actions.BRAKE
        case obstacles.CRACK:
            return actions.JUMP
        case obstacles.PENGUIN:
            return actions.PICKUP
        case _:
            return False
