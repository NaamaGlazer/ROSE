"""Game obstacles"""

import random

NONE = ""  # NOQA
CRACK = "crack"  # NOQA
TRASH = "trash"  # NOQA
PENGUIN = "penguin"  # NOQA
BIKE = "bike"  # NOQA
WATER = "water"  # NOQA
BARRIER = "barrier"  # NOQA
# GOLDEN_PENGUIN = "golden_penguin"  # NOQA
CEMENT_PACK = "cement_pack"
CEMENT_WALL = "cement_block"

ALL = (NONE, CRACK, TRASH, PENGUIN, BIKE, WATER, BARRIER)


def get_random_obstacle():
    return random.choice(ALL)
