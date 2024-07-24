from rose.common import obstacles, actions  # NOQA

driver_name = "UR FACE"

NONE_SCORE = 10
JUMP_SCORE = 15
BRAKE_SCORE = 14
PICKUP_SCORE = 20
COLLISION_SCORE = -30


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
    best = max(
        get_best_rout(world, x, y - 1, actions.NONE),
        get_best_rout(world, x + 1 if x % 3 < 2 else 0, y - 1, actions.RIGHT),
        get_best_rout(world, x - 1 if x % 3 > 0 else 0, y - 1, actions.LEFT),
        key=lambda rout: rout[1],
    )

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
    # print("\n\n\n============================================================\n\n\n")

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
        return COLLISION_SCORE
    match world.get((x, y)):
        case obstacles.PENGUIN:
            return PICKUP_SCORE
        case obstacles.CRACK:
            return JUMP_SCORE
        case obstacles.WATER:
            return BRAKE_SCORE
        case obstacles.NONE:
            return NONE_SCORE
        case _:
            return COLLISION_SCORE


def get_best_rout(world, x, y, action, depth=0):
    current_score = get_score(world, x, y)
    if action != actions.NONE:
        if PICKUP_SCORE > current_score > NONE_SCORE:
            current_score = COLLISION_SCORE
        if current_score == PICKUP_SCORE:
            current_score = NONE_SCORE
    if y == 0:
        return ([action], current_score)
    left = ([], COLLISION_SCORE)
    right = ([], COLLISION_SCORE)
    none = ([], COLLISION_SCORE)
    # check action left
    if x % 3 > 0:
        left = get_best_rout(world, x - 1, y - 1, actions.LEFT, depth + 1)
    # check action right
    if x % 3 < 2:
        right = get_best_rout(world, x + 1, y - 1, actions.RIGHT, depth + 1)
    # check action none
    none = get_best_rout(world, x, y - 1, actions.NONE, depth + 1)
    # check action brake

    # commented out debug info
    # print(f"{left=}")
    # print(f"{right=}")
    # print(f"{none=}")

    # chouse best rout
    best = max(left, right, none, key=lambda act: act[1])
    # print(f"{best=}")  # commented out debug info
    # print(f"{depth=}\n\n")

    # break down the best rout to score and rout
    best_rout, best_score = best

    # insert the acition into action list, and add score sum
    return ([action] + best_rout, current_score + best_score)
    # action_list, score_sum
