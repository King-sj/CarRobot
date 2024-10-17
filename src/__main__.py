# from src.car import Car
from src.robot_craft_car import RobotCraftCar as Car,Direction
from src.logging_config import setup_logging
import logging
from src.config import Config
import asyncio
from typing import Callable
logger = logging.getLogger(__name__)
async def control_car(car:Car):
  is_right_gesture = \
      lambda: car.in_road \
      and (not car.have_obstacle)\
      and (car.distance != None and car.distance > 40)
  while True:
    car.straight(is_right_gesture)
    print(f"current state: {car.distance}, {car.in_road}, {car.have_obstacle}")
    if(car.distance is None or car.in_road is None):
      await asyncio.sleep(0.1) # sleep some times to release thread
      continue
    
    if not is_right_gesture():
      await car.adjustment_dir(is_right_gesture)
    await asyncio.sleep(0.1) # wait for updating state

async def main():
  setup_logging()
  car = Car()
  v = control_car(car)
  await car.connect()
  await asyncio.gather(
        car.update_state(),
        control_car(car))


if __name__ == "__main__":
  logger.setLevel(Config.LOG_LEVEL)
  asyncio.run(main())
  print("done")