"""
This driver does not do any action.
"""

from rose.common import obstacles, actions  # NOQA

driver_name = "No Driver"

hard_obstacles = set([obstacles.BIKE, obstacles.BARRIER, obstacles.TRASH])

def obstacles_(car_pose_X, car_pose_Y,world):
    if world.get((car_pose_X,car_pose_Y-1)) == obstacles.BARRIER or obstacles.BIKE or obstacles.TRASH:
        if world.get((car_pose_X-1, car_pose_Y)) == obstacles.BARRIER or obstacles.BIKE or obstacles.TRASH:
            return actions.RIGHT
        elif world.get((car_pose_X+1, car_pose_Y)) == obstacles.BARRIER or obstacles.BIKE or obstacles.TRASH:
            return actions.LEFT



def drive(world):
    print("hi")
    car_x = world.car.x
    car_y = world.car.y
    soft_obstacle_action = handle_soft_obstacles(world, car_x, car_y)
    obstacles_action = obstacles_(car_x,car_y,world)
    if obstacles_action:
        return obstacles_action
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