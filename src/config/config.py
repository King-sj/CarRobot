import configparser

config = configparser.ConfigParser()
config.read('src/config/config.ini')
print(config.sections())
class Config:
  LOG_LEVEL = config.get('DEFAULT', 'LogLevel')
  ServerIP = config.get('DEFAULT', 'ServerIP')
  ServerPort = config.getint('DEFAULT', 'ServerPort')

