from rose.common import obstacles, actions  # NOQA

driver_name = "Lane Switcher"


def drive(world):
    # get car position
    x = world.car.x
    y = world.car.y

    # debug information
    # print("pos =", (x, y))
    # print("standing on", world.get((x, y)))
    # print(f"view:\n{(
    #     world.get((x - (1 if x % 3 > 0 else 0), y-1)),
    #     world.get((x, y-1)),
    #     world.get((x + (1 if x % 3 < 2 else 0), y-1))
    # )}")

    # get 3 possible routs
    none = get_best_rout(world, x, y - 1, actions.NONE)
    right = get_best_rout(world, x + (1 if x % 3 < 2 else 0), y - 1, actions.RIGHT)
    left = get_best_rout(world, x - (1 if x % 3 > 0 else 0), y - 1, actions.LEFT)
    # print(f"{left=}\n{right=}\n{none=}")  # debug info

    # chose the one that gives most points
    best = max(none, right, left, key=lambda rout: rout[1])

    # handle soft obstacle
    soft_aciton = handle_soft_obstacles(world)
    if soft_aciton is not False:
        # print("doing", soft_aciton)  # debug info
        return soft_aciton

    # more debug info
    # print(f"{best=}")
    # print(f"doing '{best[0][0]}'")
    # print(f"next is {best[0][1]}")
    # print("\n\n")
    # return the wanted action
    return best[0][0]


def handle_soft_obstacles(world):
    try:
        x = world.car.x
        y = world.car.y
        match world.get((x, y - 1)):
            case obstacles.PENGUIN:
                return actions.PICKUP
            case obstacles.WATER:
                return actions.BRAKE
            case obstacles.CRACK:
                return actions.JUMP
            case _:
                return False
    except IndexError:
        return False


def get_score(world, x, y):
    if y < 0:
        return -10
    match world.get((x, y)):
        case obstacles.PENGUIN:
            return 20
        case obstacles.CRACK:
            return 15
        case obstacles.WATER:
            return 14
        case obstacles.NONE:
            return 10
        case _:
            return -10


def get_best_rout(world, x, y, action, depth=0):
    current_score = get_score(world, x, y)
    if y == 0:
        return ([action], current_score)
    left = ([], -20)
    right = ([], -20)
    none = ([], -20)
    # check action left
    if x % 3 > 0:
        left = get_best_rout(world, x - 1, y - 1, actions.LEFT, depth + 1)
        # points go down if moving and landing an obstacle
        # so we do this to prevent it
        obstacle_score = get_score(world, x - 1, y - 1)
        if obstacle_score > 10:
            rout, score = left
            left = (rout, score - 10 - obstacle_score)
            # print(left[1])
    # check action right
    if x % 3 < 2:
        right = get_best_rout(world, x + 1, y - 1, actions.RIGHT, depth + 1)
        # points go down if moving and landing an obstacle
        # so we do this to prevent it
        obstacle_score = get_score(world, x + 1, y - 1)
        if obstacle_score > 10:
            rout, score = right
            right = (rout, score - 10 - obstacle_score)
            # print(right[1])
    # check action none
    none = get_best_rout(world, x, y - 1, actions.NONE, depth + 1)
    # check action brake

    # commented out debug info
    # print(f"{left=}")
    # print(f"{right=}")
    # print(f"{none=}")

    # chouse best rout
    best = max(left, right, none, key=lambda act: act[1])
    # print(f"{best=}") # commented out debug info
    # print(f"{depth=}\n\n")

    # break down the best rout to score and rout
    best_rout, best_score = best

    # insert the acition into action list, and add score sum
    return ([action] + best_rout, current_score + best_score)
    # action_list, score_sum


NONE_SCORE = 10
JUMP_SCORE = 15
BRAKE_SCORE = 14
PICKUP_SCORE = 20
COLLISION_SCORE = -10


def get_optimal_path(world, x, y, action):
    current_tile_score = get_score(world, x, y)
    if y == 0:
        return action, current_tile_score
    match world.get((x, y - 1)):
        case obstacles.NONE:
            best = get_best(world, x, y, action.NONE, NONE_SCORE)
        case obstacles.PENGUIN:
            best = get_best(world, x, y, actions.PICKUP, PICKUP_SCORE)
        case obstacles.CRACK:
            best = get_best(world, x, y, actions.JUMP, JUMP_SCORE)
        case obstacles.WATER:
            best = get_best(world, x, y, actions.BRAKE, BRAKE_SCORE)
        case _:
            best = get_best(world, x, y, actions.NONE, COLLISION_SCORE)
    return best

    """
    if y == 0:
        return
    if obs in front == NONE:
        rigth
        left 
        none
    elif obs in front == penguin:
        right
        left
        pickup
    """


def get_best(world, x, y, action, action_score):
    current_tile_score = get_score(world, x, y)
    able_right = 1 if x % 3 < 2 else 0
    able_left = -1 if x % 3 > 0 else 0
    a = get_optimal_path(world, x + able_right, y - 1, actions.RIGHT)
    b = get_optimal_path(world, x + able_left, y - 1, actions.LEFT)
    c = get_optimal_path(world, x, y - 1, actions.NONE)
    return max(
        (a[0], current_tile_score + NONE_SCORE + a[1]),
        (b[0], current_tile_score + NONE_SCORE + b[1]),
        (c[0], current_tile_score + action + c[1]),
        key=lambda t: t[1],
    )
