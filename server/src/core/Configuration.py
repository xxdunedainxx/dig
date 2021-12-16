import os
import json

class Configuration:
  DEFAULT_VALUES: dict = {
    "FLASK_HOST_BIND": "0.0.0.0",
    "FLASK_PORT_BIND": 80,
    "FLASK_CORS_ORIGIN": "*",
    "API_SERVER_ENABLED" : True,
    "APP_HEALTH_PORT": 9090,
    "DB_ENGINE" : "mysql",
    "APP_HEALTH_ONLY_API_TOGGLE": True,
    "MYSQL_HOST" : "localhost",
    "MYSQL_PORT" : 3306,
    "DISCORD" : {
      "DISCORD_TOKEN": None,
      "ENABLED" : True,
      "USER_SESSION_TIMEOUT_MINUTES" : 180
    },
    "REFRESH_ENERGY_INTERVAL" : 1
  }

  def __init__(self):
    self.VERSION = '0.0.1'
    self.CONF_FILE_LOCATION: str = './conf.json'
    self.RAW_CONF: str = open(self.CONF_FILE_LOCATION, "r").read().strip()
    print(f"Raw configuration file {self.RAW_CONF}")
    self.CONF: dict = json.loads(self.RAW_CONF)

    # Flask configurations
    self.FLASK_HOST_BIND: str = self.__get_value("FLASK_HOST_BIND")
    self.FLASK_PORT_BIND: int = self.__get_value("FLASK_PORT_BIND")
    self.FLASK_CORS_ORIGIN: str = self.__get_value("FLASK_CORS_ORIGIN")
    self.APP_HEALTH_PORT: int = self.__get_value("APP_HEALTH_PORT")
    self.API_SERVER_ENABLED: bool = self.__get_value("API_SERVER_ENABLED")

    # DB Engine
    self.DB_ENGINE: str = self.__get_value("DB_ENGINE")

    # Mysql configurations
    self.MYSQL_HOST: str = self.__get_value("MYSQL_HOST")
    self.MYSQL_PORT: int = self.__get_value("MYSQL_PORT")
    self.MYSQL_USERNAME: str = self.__get_value("MYSQL_USERNAME")
    self.MYSQL_PASSWORD: str = self.__get_value("MYSQL_PASSWORD")

    self.DISCORD: dict = self.__get_value("DISCORD")
    self.REFRESH_ENERGY_INTERVAL: int = self.__get_value("REFRESH_ENERGY_INTERVAL")


  def __get_value(self, key: str):
    # environment variables have highest prio
    if key in os.environ.keys():
      return self.__get_environ_value(key)
    elif key in self.CONF.keys():
      return self.__parse_conf_file_value(key)
    elif key in Configuration.DEFAULT_VALUES.keys():
      return self.DEFAULT_VALUES[key]
    else:
      raise Exception(f"Could not find value for required key {key} :(")

  def __get_environ_value(self, key: str):
    return os.environ.get(key)

  def __parse_conf_file_value(self, key: str):
    return self.CONF[key]


CONF_INSTANCE = Configuration()