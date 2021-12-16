from src.core.util.LogFactory import LogFactory
from src.core.util.ErrorFactory import errorStackTrace
from src.core.data.DBClient import DBClient
from src.core.data.connectors.mysql.MySql import MySql
from src.core.Configuration import CONF_INSTANCE

class DatabaseFactory:

  def __init__(self):
    pass

  @staticmethod
  def fetch_db_client() -> DBClient:
    if CONF_INSTANCE.DB_ENGINE == "mysql":
      LogFactory.MAIN_LOG.info(f"Fetching DB engine {CONF_INSTANCE.DB_ENGINE}")
      return DatabaseFactory.fetch_mysql_client()
    else:
      raise Exception(f"Unsupported DB engine... {CONF_INSTANCE.DB_ENGINE}")

  @staticmethod
  def fetch_mysql_client() -> MySql:
    LogFactory.MAIN_LOG.info('Creating Mysql instance')
    return MySql(
      host=CONF_INSTANCE.MYSQL_HOST,
      port=CONF_INSTANCE.MYSQL_PORT,
      username=CONF_INSTANCE.MYSQL_USERNAME,
      password=CONF_INSTANCE.MYSQL_PASSWORD
    )