import json
import logging

logger = logging.getLogger(__name__)


class CarReceiveProtocol:

  class ReceiveData:

    def __init__(self, name: str, id: int, value: float | int):
      self.name: str = name
      self.id: float = id
      self.value: float | int = value

    def __str__(self):
      return f'{{"name":"{self.name}", "id":{self.id}, "value":{self.value}}}'

    @staticmethod
    def from_json(json_data):
      json_data = json.loads(json_data)
      return CarReceiveProtocol.ReceiveData(json_data['name'], json_data['id'],
                                            json_data['value'])

  def __init__(self, distance: float, front_light: int, bottom_light: int):
    self.distance = self.ReceiveData('distance', 4, distance)
    self.front_light = self.ReceiveData('light', 2, front_light)
    self.bottom_light = self.ReceiveData('light', 1, bottom_light)

  def __str__(self):
    return f'{{"sensors":[{self.distance},{self.front_light},{self.bottom_light}]}}'

  @staticmethod
  def from_json(json_data):
    json_data = json.loads(json_data)
    distance:float|None = None
    front_light:int|None = None
    bottom_light:int|None = None
    for sensor in json_data['sensors']:
      if sensor['id'] == 4:
        distance = sensor['value']
      elif sensor['id'] == 2:
        front_light = sensor['value']
      elif sensor['id'] == 1:
        bottom_light = sensor['value']
    if distance is None or front_light is None or bottom_light is None:
      raise ValueError('json_data must have distance, front_light, bottom_light')
    return CarReceiveProtocol(distance, front_light, bottom_light)

  def get_distance(self):
    return self.distance.value
  @property
  def in_road(self):
    return self.bottom_light.value == 1
  @property
  def have_obstacle(self):
    return self.front_light.value == 1


class CarSendProtocol:

  class SendData:

    def __init__(self, servoid: int, servospeed: float):
      self.servoid: int = servoid
      self.servospeed: float = servospeed

    def __str__(self):
      return f'{{"servoId":{self.servoid}, "servoSpeed":{self.servospeed}}}'

  def __init__(self, left_speed: float, right_speed: float):
    self.letServoMove = self.SendData(6, left_speed)
    self.rightServoMove = self.SendData(3, right_speed)

  def __str__(self):
    return f'{{"servos":[{self.letServoMove},{self.rightServoMove}]}}\r\n'


# test
if __name__ == '__main__':
  # 创建一个CarSendProtocol实例
  car_send_protocol = CarSendProtocol(0.5, 0.8)
  print(car_send_protocol.letServoMove.servospeed)
  # 创建一个CarReceiveProtocol实例
  car_receive_protocol = CarReceiveProtocol(0.5, 1, 0)
  print(car_receive_protocol.distance.value)
  json_data = '{"sensors":[{"name":"distance", "id":4, "value":0.5},{"name":"light", "id":2, "value":0.8},{"name":"light", "id":1, "value":0.3}]}'
  print(CarReceiveProtocol.from_json(json_data))