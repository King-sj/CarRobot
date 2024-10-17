from src.car import Car
from enum import Enum
from typing import Callable
import asyncio
class Direction(Enum):
  LEFT = "left"
  RIGHT = "right"

class RobotCraftCar(Car):
  def __init__(self):
    super().__init__()
  def set_speed(self, left_speed: float, right_speed: float):
    # 轮速差同步
    left_speed *= 0.72
    return super().set_speed(left_speed, right_speed)
  async def stop(self,duration:float|None=None):
    self.set_speed(0.0,0.0)
    if duration != None:
      await asyncio.sleep(duration)
  def straight(self):
    self.set_speed(0.2,0.2)
  def turn_left(self):
    self.set_speed(-0.2,0.2)
  def turn_right(self):
    self.set_speed(0.2,-0.2)
  async def __adjustment_dir(self, dir:Direction, duration:float, is_right_gesture:Callable):
    if is_right_gesture():
      return
    time_left = duration
    delay = 0.1
    if (dir == Direction.LEFT):
      self.turn_left()
    else:
      self.turn_right()
    print("begin turn")
    while time_left > 0:
      if is_right_gesture():
        break
      time_left -= delay
      await asyncio.sleep(delay)
      print(f"current state: {self.distance}, {self.in_road}, {self.have_obstacle}")
    print("end turn")
    await self.stop(0.1)
  async def adjustment_dir(self, is_right_gesture:Callable):
    start_duration = 0.2
    while not is_right_gesture() and start_duration <= 0.4:
      await self.__adjustment_dir(Direction.LEFT,start_duration,is_right_gesture)
      start_duration += 0.1
      if is_right_gesture():
        break
      await self.stop(0.2)          
    await self.__adjustment_dir(Direction.RIGHT,0.3,is_right_gesture)
    start_duration = 0.05
    while not is_right_gesture() and start_duration <= 0.2:
      await self.__adjustment_dir(Direction.RIGHT,start_duration,is_right_gesture)
      start_duration += 0.1
      if is_right_gesture():
        break
      await self.stop(0.2)
    self.straight()