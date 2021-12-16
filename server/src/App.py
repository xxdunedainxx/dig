from src.core.Configuration import Configuration, CONF_INSTANCE
from src.core.Setup import Setup
from src.core.util.LogFactory import LogFactory
from src.core.Services import ServiceNames
from src.core.threading.ThreadPool import WorkerPool
from src.webserver.APIFactory import APIFactory
from src.integrations.discord.Discord import DiscordIntegration
from src.game.threading.jobs.RefreshUserEnergy import RefreshUserEnergyJob
from src.core.data.DatabaseFactory import DatabaseFactory
from src.core.data.DBClient import DBClient
from src.core.util.ErrorFactory import errorStackTrace

import time

class App:

  conf: Configuration = None

  def __init__(self):
    self.conf: Configuration = CONF_INSTANCE
    Setup.init_main_app_resources()
    self.__pre_flight_checks()
    LogFactory.MAIN_LOG.info('startup app :)')


  def run(self):
    self.init_api_thread()
    self.init_refresh_energy_job()
    self.init_discord_thread()
    self.__run_forever()


  def init_discord_thread(self):
    if CONF_INSTANCE.DISCORD["enabled"] == True:
      LogFactory.MAIN_LOG.info("Discord enabled, setting up discord thread")
      self.discord_worker: WorkerPool = WorkerPool(
        poolName=ServiceNames.discord,
        size=1,
        poolType='default',
        targetMethod=DiscordIntegration.start_discord_in_thread
      )
      self.discord_worker.run()
    else:
      LogFactory.MAIN_LOG.info("Discord not enabled, not running thread")

  def init_api_thread(self):
    if CONF_INSTANCE.API_SERVER_ENABLED:
      LogFactory.MAIN_LOG.info("Startup API Server thread")
      self.api_worker: WorkerPool = WorkerPool(
        poolName=ServiceNames.apiServer,
        size=1,
        poolType='default',
        targetMethod=APIFactory.run_api_in_thread
      )
      self.api_worker.run()
    else:
      LogFactory.MAIN_LOG.info("API Server not enabled, skipping")

  def init_refresh_energy_job(self):
    LogFactory.MAIN_LOG.info("Setting up energy refresh job..")
    self.energy_job_worker: WorkerPool = WorkerPool(
      poolName=ServiceNames.energyRefresh,
      size=1,
      poolType='default',
      targetMethod=RefreshUserEnergyJob.refresh_user_energy_job
    )

    self.energy_job_worker.run()

  def __run_forever(self):
    LogFactory.MAIN_LOG.info("running app forever...")
    while True:
      time.sleep(5)
      LogFactory.MAIN_LOG.info("main app heart beat..")

  def __pre_flight_checks(self):
    LogFactory.MAIN_LOG.info("Pre-flight checks")
    self.__check_data_connection()

  def __check_data_connection(self):
    LogFactory.MAIN_LOG.info("checking mysql connection")
    client: DBClient = DatabaseFactory.fetch_db_client()