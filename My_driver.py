from rose.common import obstacles, actions  # NOQA

driver_name = "Lane Switcher"


def drive(world):
    # get car position
    x = world.car.x
    y = world.car.y

    # debug information
    print("pos =", (x, y))
    print("standing on", world.get((x, y)))
    print(f"view:\n{(
        world.get((x - (1 if x % 3 > 0 else 0), y-1)),
        world.get((x, y-1)),
        world.get((x + (1 if x % 3 < 2 else 0), y-1))
    )}")

    # handle soft obstacle
    soft_aciton = handle_soft_obstacles(world)
    if soft_aciton is not False:
        print("doing", soft_aciton)  # debug info
        return soft_aciton

    # get 3 possible routs
    none = get_best_rout(world, x, y - 1, actions.NONE)
    right = get_best_rout(world, x + (1 if x % 3 < 2 else 0), y - 1, actions.RIGHT)
    left = get_best_rout(world, x - (1 if x % 3 > 0 else 0), y - 1, actions.LEFT)
    print(f"{left=}\n{right=}\n{none=}")  # debug info

    # chose the one that gives most points
    best = max(none, right, left, key=lambda rout: rout[1])

    # more debug info
    print(f"{best=}")
    print(f"doing '{best[0][0]}'")
    print(f"next is {best[0][1]}")
    print("\n\n")

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
    match world.get((x, y)):
        case obstacles.PENGUIN:
            return 10
        case obstacles.CRACK:
            return 5
        case obstacles.WATER:
            return 4
        case obstacles.NONE:
            return 0
        case _:
            return -10


def get_best_rout(world, x, y, action, depth=0):
    current_score = get_score(world, x, y)
    if y == 0:
        return ([action], current_score)
    left = ([], -20)
    right = ([], -20)
    none = ([], -20)
    # check left rout
    if x > 0:
        left = get_best_rout(world, x - 1, y - 1, actions.LEFT, depth + 1)
        # points go down if moving and landing an obstacle
        # so we do this to prevent it
        obstacle_score = get_score(world, x - 1, y - 1)
        if obstacle_score > 0:
            rout, score = left
            left = (rout, score - 10 - obstacle_score)
    # check right rout
    if x % 3 < 2:
        right = get_best_rout(world, x + 1, y - 1, actions.RIGHT, depth + 1)
        # points go down if moving and landing an obstacle
        # so we do this to prevent it
        obstacle_score = get_score(world, x + 1, y - 1)
        if obstacle_score > 0:
            rout, score = right
            right = (rout, score - 10 - obstacle_score)
    # check none
    none = get_best_rout(world, x, y - 1, actions.NONE, depth + 1)

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
