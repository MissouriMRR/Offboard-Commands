import asyncio
from mavsdk import System
import math

async def directional_movement(drone: System, rightDistance: float, forwardDistance: float, upDistance: float) -> None:
    """
    Moves to a set position to the drone by calculating move time using a velocity of 20
     and speed for each direction based on the time and resultant distance

    Parameters
    ----------
    drone : System
        MavSDK object for drone control
    Rightdistance: float
        distance in meters wanted to go forward
    Forwarddistance: float
        distance in meters wanted to go forward
    Updistance: float
        distance in meters wanted to go forward
    """
    distance = math.sqrt((rightDistance ** 2) + (forwardDistance **2)+ (upDistance ** 2))

    rightVelocity = rightDistance/distance * 20
    forwardVelocity = forwardDistance/distance * 20
    upVelocity = upDistance/distance * 20

    move_time = distance / 20

    await drone.offboard.set_velocity_body(rightVelocity, forwardVelocity, upVelocity, 0)

    await asyncio.sleep(move_time)

    await drone.offboard.set_velocity_body(0, 0, 0, 0)
    return