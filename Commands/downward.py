"""
File containing function to move drone downwards a certain distance
"""
import asyncio
from mavsdk import System
from mavsdk import offboard


async def downward(drone: System, distance: float) -> None:
    """
    Moves downward a set distance by calculating move time using a velocity of 20

    Parameters
    ----------
    drone : System
        MavSDK object for drone control
    distance: float
        distance in meters wanted to go downward
    """

    ms_speed:float = 20
    move_time: float = distance / ms_speed

    await drone.offboard.set_velocity_body(offboard.VelocityBodyYawspeed(0, 0, -ms_speed, 0))

    await drone.offboard.start()

    await asyncio.sleep(move_time)

    await drone.offboard.set_velocity_body(offboard.VelocityBodyYawspeed(0, 0, 0, 0))
    return
