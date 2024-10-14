from src.car import Car
from src.logging_config import setup_logging
import logging
from src.config import Config
import asyncio
logger = logging.getLogger(__name__)

async def control_car(car:Car):
  car.set_speed(0.5, 0.5)
  while True:
    print(f"current state: {car.distance}, {car.in_road}, {car.have_obstacle}")
    if(car.distance is None or car.in_road is None or car.speed is None):
      await asyncio.sleep(0.1)
      continue
    if (car.distance < 20):
      car.set_speed(0.5,0)
    else :
      car.set_speed(0.5,0.5)
async def main():
  setup_logging()
  car = Car()
  await car.connect()
  # task1 = asyncio.create_task(car.update_state())
  # task2 = asyncio.create_task(control_car(car))
  # https://docs.python.org/zh-cn/3/library/asyncio-task.html#
  await asyncio.gather(
        asyncio.to_thread(car.update_state),
        control_car(car))
  # try:
  #   await task1
  #   await task2
  # except KeyboardInterrupt:
  #   pass
  # except Exception as e:
  #   logger.error(f"{e}")
  # finally:
  #   car.set_speed(0.0, 0.0)
  #   task1.done()
  #   task2.done()
  #   logger.info("Car stop")
  # TODO more code/func need call


if __name__ == "__main__":
  logger.setLevel(Config.LOG_LEVEL)
  asyncio.run(main())
  print("done")