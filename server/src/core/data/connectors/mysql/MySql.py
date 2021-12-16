from src.core.data.DBClient import DBClient
import json
import mysql.connector
from src.core.util.LogFactory import LogFactory
from src.core.util.ErrorFactory import errorStackTrace
import socket
import time

class MySql(DBClient):

  @staticmethod
  def generate_db_client():
    pass

  @staticmethod
  def get_db_client(dbIndex: int):
    pass

  def __init__(
          self,
          host: str,
          port: int,
          username: str,
          password: str
  ):
    super(DBClient, self).__init__()
    self.__host: str = host
    self.__port: int = port
    self.__username = username
    self.__password = password
    self.__check_ports()
    self.__establish_connection()

  def __check_ports(self):
    checks = 0

    while checks < 3:
      LogFactory.MAIN_LOG.info(f"Checking DB connection to {self.__host}:{self.__port}")
      a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      location = (self.__host, self.__port)
      result_of_check = a_socket.connect_ex(location)
      if result_of_check == 0:
        LogFactory.MAIN_LOG.info("[MySQL] connection is open to mysql host")
        a_socket.close()
        return
      else:
        if checks >= 3:
          LogFactory.MAIN_LOG.error("[MySQL] connection is not open to mysql host")
          a_socket.close()
          raise Exception("[MySql] failed to connect")
        else:
          checks+=1
          LogFactory.MAIN_LOG.info("[MySQL] Could not connect to mysql, backing off..")
          time.sleep(5)


  def __establish_connection(self):
    try:
      LogFactory.MAIN_LOG.info(f"Trying to establish DB connection to {self.__host}:{self.__port}")
      self.__connection = mysql.connector.connect(
        host=self.__host,
        port=self.__port,
        user=self.__username,
        password=self.__password,
        database='dig',
        use_pure=True
      )
    except socket.error as e:
      LogFactory.MAIN_LOG.error("[MYSQL] Failed to connect..")
      LogFactory.MAIN_LOG.error(f"[MYSQL] Failed to connect to DB: {errorStackTrace(e)}. Host: {self.__host}, port: {self.__port}")
      raise e
    except mysql.connector.errors.InterfaceError as e:
      LogFactory.MAIN_LOG.error("[MYSQL] Failed to connect..")
      LogFactory.MAIN_LOG.error(f"[MYSQL] Failed to connect to DB: {errorStackTrace(e)}. Host: {self.__host}, port: {self.__port}")
      raise e
    except Exception as e:
      LogFactory.MAIN_LOG.error("[MYSQL] Failed to connect..")
      LogFactory.MAIN_LOG.error(f"[MYSQL] Some other critical mysql connection error: {errorStackTrace(e)}. Host: {self.__host}, port: {self.__port}")
      raise e

  def __cursor(self):
    return self.__connection.cursor()

  def request(self, req, params=None):
    LogFactory.MAIN_LOG.info(f"Mysql request: {req}")
    if params != None and type(params) != tuple:
      raise Exception("INSECURE MYSQL REQUESTS SENT!! Tuple / parameterized requuests required.")
    cursor = self.__cursor()
    cursor.execute(req, params)
    if "select" in req.lower():
      return self.__parse_request(cursor)
    else:
      self.__connection.commit()
      return

  def __parse_request(self, cursor):
    if cursor != None:
      responseArray = []
      for row in cursor:
        responseArray.append(row)
      return responseArray
    else:
      return None