from src.car import Car
from src.logging_config import setup_logging
import logging
from src.config import Config
import asyncio
logger = logging.getLogger(__name__)

async def control_car(car:Car):
  car.set_speed(0.5, -0.5)
  while True:
    print(f"current state: {car.distance}, {car.in_road}, {car.have_obstacle}")
    if(car.distance is None or car.in_road is None or car.speed is None):
      await asyncio.sleep(0.1)
      continue
    if (car.distance < 20):
      print("change state")
      car.set_speed(0.5,0.0)
    else :
      print("change state")
      car.set_speed(0.5,-0.5)
    await asyncio.sleep(0.1)

async def main():
  setup_logging()
  car = Car()
  await car.connect()
  await asyncio.gather(
        car.update_state(),
        control_car(car))


if __name__ == "__main__":
  logger.setLevel(Config.LOG_LEVEL)
  asyncio.run(main())
  print("done")