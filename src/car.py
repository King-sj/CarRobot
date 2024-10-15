import asyncio
from src.car_protocols import CarSendProtocol, CarReceiveProtocol
import logging
from src.config import Config
from typing import Tuple, TypeVar

logger = logging.getLogger(__name__)


class Car:
  '''
  Basic car, only provides communication, automatic state updates, speed setting, and state retrieval functions.

  .. warning::
  ```
    await sleep some times is necessary to release thread for other coroutine.
  ```


  Example Usage:
  ```python
  async def control_car(car:Car):
    car.set_speed(0.5, 0.5)
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
        car.set_speed(0.5,0.5)
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
  ```
  '''
  COMP_T = float

  def __init__(self):
    self.writer: asyncio.StreamWriter | None = None
    self.reader: asyncio.StreamReader | None = None
    self.r_data: CarReceiveProtocol | None = None
    self.speed: Tuple[None | float, None | float] = (None, None)

  async def connect(self):
    logger.debug(f"Connecting to server {Config.ServerIP}:{Config.ServerPort}")
    self.reader, self.writer = await asyncio.open_connection(
        Config.ServerIP, Config.ServerPort)

  def __send(self, message):
    if self.writer is None:
      raise RuntimeError(
          "server maybe disconnected, may you forget 'await car.connect()'")
    if not message:
      logger.error("No message to send")
      return
    logger.debug(f"Sending data {message}")
    self.writer.write(message.encode('utf-8'))
    logger.debug(f"Sent: {message}")

  async def update_state(self):
    print("begin update")
    while True:
      await self.__receive()

  async def __receive(self):
    if self.reader is None:
      raise RuntimeError(
          "connection maybe disconnected, check your link to car")
    logger.debug("Waiting for data")
    data = await self.reader.readuntil(b'\r\n')
    data = data.decode('utf-8')
    logger.debug(f"Received: {data}")
    self.r_data = CarReceiveProtocol.from_json(data)

  def __in_range(self, p: COMP_T, l: COMP_T, r: COMP_T) -> bool:
    return l <= p and p <= r

  def set_speed(self, left_speed: float, right_speed: float):
    if not isinstance(left_speed, float) or not isinstance(right_speed, float):
      raise TypeError("speed should be float")
    if not self.__in_range(left_speed, -1, 1) or not self.__in_range(
        right_speed, -1, 1):
      raise ValueError("speed should between -1.0 to 1.0")
    self.__send(str(CarSendProtocol(left_speed, right_speed)))

  @property
  def distance(self):
    if self.r_data is None:
      logger.debug("not receive any data")
      return None
    return float(self.r_data.distance.value)

  @property
  def in_road(self):
    if self.r_data is None:
      logger.debug("not receive any data")
      return None
    return bool(self.r_data.in_road)

  @property
  def have_obstacle(self):
    if self.r_data is None:
      logger.debug("not receive any data")
      return None
    return bool(self.r_data.have_obstacle)
