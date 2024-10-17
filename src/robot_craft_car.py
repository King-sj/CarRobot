from src.car import Car
from enum import Enum
from typing import Callable
import asyncio
class Direction(Enum):
  LEFT = "left"
  RIGHT = "right"

class RobotCraftCar(Car):
  base_straight_speed = 0.7
  base_turn_speed = 0.1
  def __init__(self):
    super().__init__()
  def set_speed(self, left_speed: float, right_speed: float):
    return super().set_speed(left_speed, right_speed)
  def stop(self):
    self.set_speed(0.0,0.0)
  def straight(self,is_right_gesture:Callable[[],bool|None]):
    self.set_speed(self.base_straight_speed,self.base_straight_speed)
    # straight_speed = self.base_straight_speed
    # duration = 0.05
    # step = 1.3
    # while is_right_gesture():
    #   self.set_speed(straight_speed,straight_speed)
    #   await asyncio.sleep(duration)
    #   if not is_right_gesture():
    #     break
    #   straight_speed *= step
    #   if straight_speed > 1.0:
    #     straight_speed = 1.0
    # self.stop()
    
  def turn_left(self):
    self.set_speed(-self.base_turn_speed,self.base_turn_speed)
  def turn_right(self):
    self.set_speed(self.base_turn_speed,-self.base_turn_speed)
  async def __adjustment_dir(self, dir:Direction, duration:float, is_right_gesture:Callable[[],bool|None]):
    if is_right_gesture():
      self.straight(is_right_gesture)
      return
    if dir == Direction.LEFT:
      self.turn_left()
    else:
      self.turn_right()
    while duration > 0 and not is_right_gesture():
      await asyncio.sleep(0.01)
      duration -= 0.01
    if is_right_gesture():
      self.straight(is_right_gesture)
      return
  async def adjustment_dir(self, is_right_gesture:Callable[[],bool|None]):
    if is_right_gesture():
      return
    # 左转 0.5 s
    await self.__adjustment_dir(Direction.LEFT,0.5,is_right_gesture)
    # 右转 1.0 s
    await self.__adjustment_dir(Direction.RIGHT,2.0,is_right_gesture)
    # 左转 4.0 s
    await self.__adjustment_dir(Direction.LEFT,4.0,is_right_gesture)
    
