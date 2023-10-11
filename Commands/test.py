import asyncio
import logging
import sys

from typing import List

from mavsdk import System
from mavsdk import offboard
import mavsdk

from backward import backward
from forward import forward
from left import left
from right import right
from rotate import rotate
from upward import upward
from downward import downward
from movement import directional_movement

SIM_ADDR: str = "udp://:14540"
CON_ADDR: str = "serial:///dev/ttyUSB0:921600"


async def run() -> None:
    """ """

    # create a drone object
    drone: System = System()
    await drone.connect(system_address=SIM_ADDR)

    # initilize drone configurations
    await drone.action.set_takeoff_altitude(12)
    await drone.action.set_maximum_speed(25)

    # connect to the drone
    logging.info("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            logging.info("Drone discovered!")
            break

    logging.info("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            logging.info("Global position estimate ok")
            break

    logging.info("-- Arming")
    await drone.action.arm()

    logging.info("-- Taking off")
    await drone.action.takeoff()

    # wait for drone to take off
    await asyncio.sleep(60)

    print("I am here trying to set velocity")
    """
    await backward(drone, 100)

    await asyncio.sleep(30)

    await forward(drone, 100)

    await asyncio.sleep(30)

    await left(drone, 100)

    await asyncio.sleep(30)

    await right(drone, 100)

    await asyncio.sleep(30)

    await upward(drone, 100)

    await asyncio.sleep(30)

    await downward(drone, 100)

    await asyncio.sleep(30)

    await rotate(drone, 90)

    await asyncio.sleep(30)

    await forward(drone, 100)

    await asyncio.sleep(30)
    """
    await directional_movement(drone, 100, 100, 100)

    await asyncio.sleep(30)

    # return home
    await drone.action.return_to_launch()
    print("Staying connected, press Ctrl-C to exit")

    # infinite loop till forced disconnect
    while True:
        await asyncio.sleep(1)


# Runs through the code until it has looped through each element of
# the Lats and Longs array and the drone has arrived at each of them
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())
    except KeyboardInterrupt:
        print("Program ended")
        sys.exit(0)
