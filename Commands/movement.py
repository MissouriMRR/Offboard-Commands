"""
file that contains funciton to move in a diagnol based on distance wanted to move in each direction
"""

import asyncio
import math
from mavsdk import System

from mavsdk import offboard


async def directional_movement(
    drone: System, right_distance: float, forward_distance: float, up_distance: float
) -> None:
    """
    Moves to a set position to the drone by calculating move time using a velocity of 20
     and speed for each direction based on the time and resultant distance

    Parameters
    ----------
    drone : System
        MavSDK object for drone control
    right_distance: float
        distance in meters wanted to go right
    forward_distance: float
        distance in meters wanted to go forward
    up_distance: float
        distance in meters wanted to go up
    """

    ms_speed: float = 20
    distance: float = math.sqrt((right_distance**2) + (forward_distance**2) + (up_distance**2))

    right_velocity: float = right_distance / distance * ms_speed
    forward_velocity: float = forward_distance / distance * ms_speed
    up_velocity: float = up_distance / distance * ms_speed

    move_time: float = distance / ms_speed

    await drone.offboard.set_velocity_body(
        offboard.VelocityBodyYawspeed(right_velocity, forward_velocity, up_velocity, 0)
    )

    await drone.offboard.start()

    await asyncio.sleep(move_time)

    await drone.offboard.set_velocity_body(offboard.VelocityBodyYawspeed(0, 0, 0, 0))
    return
