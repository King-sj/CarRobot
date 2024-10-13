from src.car import Car
from src.logging_config import setup_logging
import logging
from src.config import Config
import asyncio
logger = logging.getLogger(__name__)

async def main():
  setup_logging()
  car = Car()
  await car.connect()
  car.set_speed(100, 100)
  print(car.in_road)
  print(car.distance)
  print(car.have_obstacle)

  # TODO more code/func need call


if __name__ == "__main__":
  logger.setLevel(Config.LOG_LEVEL)
  asyncio.run(main())