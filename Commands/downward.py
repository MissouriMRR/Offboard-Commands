import asyncio
from mavsdk import System


async def forward(drone: System, distance: int) -> None:
    """
    Moves downward a set distance by calculating move time using a velocity of 20

    Parameters
    ----------
    drone : System
        MavSDK object for drone control
    distance: int
        distance in meters wanted to go forward
    """
    move_time = distance / 20

    await drone.offboard.set_velocity_body(0, 0, -20, 0)

    await asyncio.sleep(move_time)

    await drone.offboard.set_velocity_body(0, 0, 0, 0)
    return
