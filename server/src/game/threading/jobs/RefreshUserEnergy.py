# TODO nightly job to refresh all User's energy, most likely to run 12:00 PST
# Add function for eneergy refresh which takes into account energy runes

from src.core.util.LogFactory import LogFactory
from src.core.Setup import Setup
from src.core.threading.Cron import Cron
from src.core.Services import ServiceNames
from src.core.Configuration import CONF_INSTANCE

from src.core.idm.data.db.UserData import UserData
from src.core.idm.data.model.User import User

from src.game.data.db.item.InventoryData import InventoryData
from src.game.data.models.item.Inventory import Inventory

from src.game.data.models.runes.user_buffs.EnergyRune import EnergyRune

class RefreshUserEnergyJob:


  @staticmethod
  def refresh_user_energy_job():
    Setup.init_thread_resources()
    LogFactory.MAIN_LOG.info(f"scheduling energy refresh job for every {CONF_INSTANCE.REFRESH_ENERGY_INTERVAL} minute(s)")
    Cron.run_every_x_minutes(RefreshUserEnergyJob.refresh_user_energy, CONF_INSTANCE.REFRESH_ENERGY_INTERVAL)
    Cron.execute_jobs()

  @staticmethod
  def refresh_user_energy():
    LogFactory.MAIN_LOG.info("Refreshing user energy..")
    users: [User] = UserData.fetch_all_users()

    for user in users:
      userInv: Inventory = InventoryData.get_inventory(user)

      for item in userInv.rune_buckets:
        if issubclass(type(userInv.rune_buckets[item][0]), EnergyRune):
          runeToApply: EnergyRune = userInv.rune_buckets[item][0]
          user.energy = 5
          runeToApply.apply_buff(user, len(userInv.rune_buckets[item]))
          UserData.update_user(user)
