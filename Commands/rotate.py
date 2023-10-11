"""
file containing function to rotate drone in degrees
"""
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

    async for tel in drone.telemetry.attitude_euler():
        yaw: float = tel.yaw_deg

        await drone.offboard.set_position_ned(
            offboard.PositionNedYaw(0, 0, 0, yaw + degrees)
        )
        return
