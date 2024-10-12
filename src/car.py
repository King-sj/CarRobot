import asyncio
from src.car_protocols import CarSendProtocol, CarReceiveProtocol
import logging
from src.config import Config

logger = logging.getLogger(__name__)


class Car:

  def __init__(self):
    """
    必须调用connect
    """
    self.writer: asyncio.StreamWriter | None = None
    self.reader: asyncio.StreamReader | None = None
    self.r_data: CarReceiveProtocol | None = None

  async def connect(self):
    logger.debug(f"Connecting to server {Config.ServerIP}:{Config.ServerPort}")
    self.reader, self.writer = await asyncio.open_connection(
        Config.ServerIP, Config.ServerPort)
    # 启动一个协程来接收数据
    asyncio.create_task(self.__receive())

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

  async def __receive(self):
    if self.reader is None:
      raise RuntimeError(
          "connection maybe disconnected, check your link to car")
    logger.debug("Waiting for data")
    data = await self.reader.readuntil(b'\r\n')
    data = data.decode('utf-8')
    logger.debug(f"Received: {data}")
    self.r_data = CarReceiveProtocol.from_json(data)

  def set_speed(self, left_speed, right_speed):
    self.__send(str(CarSendProtocol(left_speed, right_speed)))

  def distance(self):
    if self.r_data is None:
      logger.debug("not receive any data")
      return None
    return self.r_data.distance

  def in_road(self):
    if self.r_data is None:
      logger.debug("not receive any data")
      return None
    return self.r_data.in_road

  def have_obstacle(self):
    if self.r_data is None:
      logger.debug("not receive any data")
      return None
    return self.r_data.have_obstacle
