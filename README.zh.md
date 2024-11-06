# 北京邮电大学创新学院时间智能车循迹 python 版

[前往 Go 版本](https://github.com/DrinkLessMilkTea/robot_car)

[lib](https://github.com/King-sj/CarRobot/tree/lib)

## 多语言
- [English](README.md)
- [中文](README.zh.md)

## 环境设置

- Python 3.11
- 无额外需求

## 如何开始

```sh
python -m src
```

**或者在 VSCode 中按 F5。**

## API 文档

### 通用汽车类

文件: `src/car.py`

- `Car()`: 创建一个实例
- `connect()`: 异步连接到汽车的 WiFi 并使用 tcp
- `update_state()`: 异步更新汽车状态
- `set_speed(...)`: 设置汽车速度
- `distance`: 与障碍物的距离
- `in_road`: 汽车是否在正确的路径上
- `have_obstacle`: 前方是否有障碍物（基于红外信号）

### 最小示例

```py
from src.car import Car
from src.logging_config import setup_logging
import logging
from src.config import Config
import asyncio
logger = logging.getLogger(__name__)
# @attention await sleep some times is necessary to release thread for other coroutine.
async def control_car(car: Car):
  car.set_speed(0.5, 0.5)
  while True:
    print(f"当前状态: {car.distance}, {car.in_road}, {car.have_obstacle}")
    if car.distance is None or car.in_road is None or car.speed is None:
      await asyncio.sleep(0.1)
      continue
    if car.distance < 20:
      print("改变状态")
      car.set_speed(0.5, 0.0)
    else:
      print("改变状态")
      car.set_speed(0.5, 0.5)
    await asyncio.sleep(0.1)

async def main():
  setup_logging()
  car = Car()
  await car.connect()
  await asyncio.gather(
    car.update_state(),
    control_car(car)
  )

if __name__ == "__main__":
  logger.setLevel(Config.LOG_LEVEL)
  asyncio.run(main())
  print("完成")
```

### 智能汽车

文件: `src/robot_craft_car.py`

- `class RobotCraftCar(Car)`: 进一步封装汽车
一些示例
```py
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
```
### 示例用法

```py
from src.robot_craft_car import RobotCraftCar as Car, Direction
from src.logging_config import setup_logging
import logging
from src.config import Config
import asyncio

logger = logging.getLogger(__name__)

async def control_car(car: Car):
  car.set_speed(0.3, 0.3)
  while True:
    print(f"当前状态: {car.distance}, {car.in_road}, {car.have_obstacle}")
    if car.distance is None or car.in_road is None or car.speed is None:
      await asyncio.sleep(0.1)
      continue
    if not car.in_road:
      await car.adjustment_dir(Direction.RIGHT, 1, lambda: car.in_road)
    if car.distance < 20:
      print("改变状态")
      await car.adjustment_dir(Direction.RIGHT, 1, lambda: car.distance is not None and car.distance > 40)
    await asyncio.sleep(0.1)

async def main():
  setup_logging()
  car = Car()
  await car.connect()
  await asyncio.gather(
    car.update_state(),
    control_car(car)
  )

if __name__ == "__main__":
  logger.setLevel(Config.LOG_LEVEL)
  asyncio.run(main())
  print("完成")
```

## 通信协议

![协议图 1](image-1.png)
![协议图 2](image.png)