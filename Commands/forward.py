import asyncio
from mavsdk import System
from mavsdk import offboard


async def forward(drone: System, distance: float) -> None:
    """
    Moves forward a set distance by calculating move time using a velocity of 20

    Parameters
    ----------
    drone : System
        MavSDK object for drone control
    distance: float
        distance in meters wanted to go forward
    """

    ms_speed: float = 20
    move_time: float = distance / 20

    await drone.offboard.set_velocity_body(offboard.VelocityBodyYawSpeed(ms_speed, 0, 0, 0))

    await drone.offboard.start()

    await asyncio.sleep(move_time)

    await drone.offboard.set_velocity_body(offboard.VelocityBodyYawSpeed(0, 0, 0, 0))
    return