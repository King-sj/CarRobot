# from src.car import Car
from src.robot_craft_car import RobotCraftCar as Car,Direction
from src.logging_config import setup_logging
import logging
from src.config import Config
import asyncio
from typing import Callable
logger = logging.getLogger(__name__)
async def control_car(car:Car):
  car.set_speed(0.3, 0.3)
  while True:
    print(f"current state: {car.distance}, {car.in_road}, {car.have_obstacle}")
    if(car.distance is None or car.in_road is None or car.speed is None):
      await asyncio.sleep(0.1) # sleep some times to release thread
      continue
    if not car.in_road:
      await car.adjustment_dir(Direction.RIGHT,1,lambda:car.in_road)
    if (car.distance < 20):
      print("change state")
      await car.adjustment_dir(Direction.RIGHT,1,lambda:car.distance!=None and car.distance>40)
    await asyncio.sleep(0.1)

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