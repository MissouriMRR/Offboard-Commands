import asyncio
from mavsdk import System


async def backward(drone: System, distance: float) -> None:
    """
    Moves backwards a set distance by calculating move time using a velocity of 20

    Parameters
    ----------
    drone : System
        MavSDK object for drone control
    distance: float
        distance in meters wanted to go forward
    """
    move_time = distance / 20

    await drone.offboard.set_velocity_body(mavsdk.offboard.VelocityBodyYawSpeed(-20, 0, 0, 0))

    await asyncio.sleep(move_time)

    await drone.offboard.set_velocity_body(mavsdk.offboard.VelocityBodyYawSpeed(0, 0, 0, 0))
    return
