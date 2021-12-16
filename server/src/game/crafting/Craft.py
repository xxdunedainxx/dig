from src.core.util.LogFactory import LogFactory
from src.core.util.ErrorFactory import errorStackTrace
from src.core.util.StringFormatters import StringFormatters

from src.game.crafting.rune.BasicRuneCrafter import RuneCraftingException
from src.game.data.models.runes.pool_buffs.RubyRune import RubyRune
from src.game.data.models.runes.user_buffs.EnergyRune import EnergyRune

from src.game.data.models.item.Inventory import Inventory
from src.game.data.db.item.InventoryData import InventoryData
from src.core.idm.data.model.User import User

class CraftResponse:

  def __init__(self, message: str, successful: bool):
    self.message = message
    self.succuessful = successful

class Crafter:
  CRAFT_COMMANDS = {
    "rubyrune" : RubyRune.craft,
    "energyrune" : EnergyRune.craft
  }

  @staticmethod
  def craft(craftable: str, user: User):
    try:
      if craftable not in Crafter.CRAFT_COMMANDS.keys():
        return CraftResponse(f"Not a valid craftable. See list of craftables: \n{StringFormatters.convert_dict_keys_to_comma_seperated_list(Crafter.CRAFT_COMMANDS)}", False)
      userInventory: Inventory = InventoryData.get_inventory(user)
      return Crafter.CRAFT_COMMANDS[craftable](user, userInventory)
    except RuneCraftingException as e:
      LogFactory.MAIN_LOG.info("User does not have enough materials to craft..")
      return CraftResponse("Could not craft", False)
    except Exception as e:
      LogFactory.MAIN_LOG.error(f"Critical error crafting: {errorStackTrace(e)}")
      return CraftResponse("Could not craft", False)