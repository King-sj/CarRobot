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
  def straight(self):
    self.set_speed(0.2,0.2)
  def low_straight(self):
    self.set_speed(0.2,0.2)
  def turn_left(self):
    self.set_speed(-0.1,0.1)
  def turn_right(self):
    self.set_speed(0.1,-0.1)
  async def adjustment_dir(self, dir:Direction, duration:float, is_right_gesture:Callable):
    time_left = duration
    if (dir == Direction.LEFT):
      self.turn_left()
    else:
      self.turn_right()
    while time_left > 0:
      if is_right_gesture():
        break
      time_left -= 0.1
      await asyncio.sleep(0.1)
    self.straight()