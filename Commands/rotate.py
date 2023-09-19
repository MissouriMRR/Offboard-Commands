import asyncio
import mavsdk
from mavsdk import System
from mavsdk import offboard


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

    yaw: float = drone.offboard.PositionNedYaw.yaw_deg

    await drone.offboard.set_postion_ned(offboard.PositionNedYaw(0, 0, 0, yaw + degrees))
    return
