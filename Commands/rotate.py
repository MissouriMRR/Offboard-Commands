import asyncio
import mavsdk
from mavsdk import System


async def rotate(drone: System, degrees: float) -> None:
    """
    changes yaw rotation in accordance to direction the drone is facing

    Parameters
    ----------
    drone : System
        MavSDK object for drone control
    degrees: float
        degrees wanting to change in accordance in direction facing
    """

    yaw = drone.offboard.PositionNedYaw.yaw_deg

    await asyncio.sleep(move_time)

    await drone.offboard.set_postion_ned(mavsdk.offboard.PostionNedYaw(0,0,0,yaw+degrees))
    return
