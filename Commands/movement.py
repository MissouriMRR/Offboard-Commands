import asyncio
from mavsdk import System
import time
import math

async def movement(drone: System, Rightdistance: int, Forwardistance:int, Updistance:int) -> None:
    """
    Moves to a set position to the drone by calculating move time using a velocity of 20

    Parameters
    ----------
    drone : System
        MavSDK object for drone control
    Rightdistance: int
        distance in meters wanted to go forward
    Forwarddistance: int
        distance in meters wanted to go forward
    Updistance: int
        distance in meters wanted to go forward
    """

    move_time = distance / 20

    await drone.offboard.set_velocity_body(-20, 0, 0, 0)

    time.sleep(move_time)

    await drone.offboard.set_velocity_body(0, 0, 0, 0)
    return