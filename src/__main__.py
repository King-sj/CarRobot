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
  car.set_speed(0.5, 0.5)
  print(car.in_road)
  print(car.distance)
  print(car.have_obstacle)
  while True:
    # 检测ctrl+c信号并让小车停止
    try:
      pass
    except KeyboardInterrupt:
      break
    except Exception as e:
      logger.error(f"{e}")
    finally:
      car.set_speed(0, 0)
      logger.info("Car stop")
      break

  # TODO more code/func need call


if __name__ == "__main__":
  logger.setLevel(Config.LOG_LEVEL)
  asyncio.run(main())