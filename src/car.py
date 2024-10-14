import asyncio
from src.car_protocols import CarSendProtocol, CarReceiveProtocol
import logging
from src.config import Config
from typing import Tuple,TypeVar
logger = logging.getLogger(__name__)


class Car:
  '''
  This is a Car

  @TODO
  add more docs

  @Example:

  car = Car()

  await car.connect()

  task1 = asyncio.create_task(car.update_state)

  task2 = asyncio.create_task(other_func)

  '''
  COMP_T = float
  def __init__(self):
    self.writer: asyncio.StreamWriter | None = None
    self.reader: asyncio.StreamReader | None = None
    self.r_data: CarReceiveProtocol | None = None
    self.speed:Tuple[None|float,None|float] = (None,None)

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
    while True:
      await self.__receive()
      await asyncio.sleep(100)

  async def __receive(self):
    if self.reader is None:
      raise RuntimeError(
          "connection maybe disconnected, check your link to car")
    logger.debug("Waiting for data")
    data = await self.reader.readuntil(b'\r\n')
    data = data.decode('utf-8')
    logger.debug(f"Received: {data}")
    self.r_data = CarReceiveProtocol.from_json(data)

  def __in_range(self, p:COMP_T, l:COMP_T , r:COMP_T) -> bool:
    return l <= p and p <= r
  def set_speed(self, left_speed:float, right_speed:float):
    if not isinstance(left_speed,float) or not isinstance(right_speed,float):
      raise TypeError("speed should be float")
    if not self.__in_range(left_speed,0,1) or not self.__in_range(right_speed,0,1):
      raise ValueError("speed should between 0.0 to 1.0")
    self.__send(str(CarSendProtocol(left_speed, right_speed)))
  @property
  def distance(self):
    if self.r_data is None:
      logger.debug("not receive any data")
      return None
    return self.r_data.distance.value
  @property
  def in_road(self):
    if self.r_data is None:
      logger.debug("not receive any data")
      return None
    return self.r_data.in_road
  @property
  def have_obstacle(self):
    if self.r_data is None:
      logger.debug("not receive any data")
      return None
    return self.r_data.have_obstacle