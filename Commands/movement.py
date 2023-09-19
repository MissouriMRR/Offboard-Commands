import asyncio
from mavsdk import System
import math
from mavsdk import offboard


async def directional_movement(
    drone: System, rightdistance: float, forwarddistance: float, updistance: float
) -> None:
    """
    Moves to a set position to the drone by calculating move time using a velocity of 20
     and speed for each direction based on the time and resultant distance

    Parameters
    ----------
    drone : System
        MavSDK object for drone control
    rightdistance: float
        distance in meters wanted to go right
    forwarddistance: float
        distance in meters wanted to go forward
    updistance: float
        distance in meters wanted to go up
    """
    distance: float = math.sqrt((rightdistance**2) + (forwarddistance**2) + (updistance**2))

    rightvelocity: float = rightdistance / distance * 20
    forwardvelocity: float = forwarddistance / distance * 20
    upvelocity: float = updistance / distance * 20

    move_time: float = distance / 20

    await drone.offboard.set_velocity_body(
        offboard.VelocityBodyYawspeed(rightvelocity, forwardvelocity, upvelocity, 0)
    )

    await asyncio.sleep(move_time)

    await drone.offboard.set_velocity_body(offboard.VelocityBodyYawspeed(0, 0, 0, 0))
    return
