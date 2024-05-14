import math
from graphics import *

#  ----------- player methods -----------

def accelerate_x(v) -> float:
    return v +PLAYER_A_X * TIME_DELTA

def decelerate_x(v) -> float:
    return v -PLAYER_A_X * TIME_DELTA

def accelerate_y(v) -> float:
    return v +PLAYER_A_Y * TIME_DELTA

def calc_loc_x(x, v) -> float:
    return x + v*TIME_DELTA + PLAYER_A_X/2 * (TIME_DELTA**2)

def calc_loc_y(y, v) -> float:
    return y + v*TIME_DELTA + PLAYER_A_Y/2 * (TIME_DELTA**2)


# ----------- ball methods -----------

def ball_calc_loc_x(x, v) -> float:
    return x + v*TIME_DELTA + BALL_A_X/2 * (TIME_DELTA**2)

def ball_calc_loc_y(y, v) -> float:
    return y + v*TIME_DELTA + BALL_A_Y/2 * (TIME_DELTA**2)

def ball_accelerate_x(v) -> float:
    return v +BALL_A_X * TIME_DELTA

def ball_decelerate_x(v) -> float:
    return v -BALL_A_X * TIME_DELTA

def ball_accelerate_y(v) -> float:
    return v +BALL_A_Y * TIME_DELTA

def calc_vx_impulse(v1x, v2x):
    """calculate horizontal velocity using impulse and momentum formula."""
    d = ((PLAYER_MASS*v1x*0.6 + BALL_MASS*v2x) / BALL_MASS)
    return d

def calc_vy_impulse(v1y, v2y):
    """calculate vertical velocity using impulse and momentum formula."""
    return (PLAYER_MASS*v1y*0.6 + BALL_MASS*v2y) / BALL_MASS
