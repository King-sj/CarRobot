import socket
from car_protocols import CarSendProtocol, CarReceiveProtocol
def communicate_with_server(ip, port):
  # 创建一个TCP/IP套接字
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  try:
    # 连接到服务器
    sock.connect((ip, port))
    print(f"Connected to {ip}:{port}")
    if True:
      # 发送数据
      message = str(CarSendProtocol(0.5, 0.5))
      sock.sendall(message.encode('utf-8'))
      print(f"Sent: {message}")

      # 接收数据
      data : bytes = sock.recv(1024)
      print(f"Received: {data.decode("utf-8")}")
      data = CarReceiveProtocol.from_json(data.decode('utf-8'))
  except Exception as e:
    print("some error ocurred!")
    print(e)
  finally:
    # 关闭连接
    sock.close()
    print("Connection closed")

# 使用指定的IP地址和端口进行通信
communicate_with_server('192.168.0.1', 9999)
