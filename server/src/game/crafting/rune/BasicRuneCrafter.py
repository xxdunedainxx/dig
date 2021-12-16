from src.core.idm.data.model.User import User

from src.game.data.db.item.InventoryData import InventoryData
from src.game.data.db.rune.RuneData import RuneData
from src.game.data.db.item.ItemData import ItemData
from src.game.data.models.runes.pool_buffs.RubyRune import RubyRune
from src.game.data.models.item.Inventory import Inventory


class RuneCraftingException(Exception):

  def __init__(self, message: str):
    super().__init__(f"Failed to craft rune due to: {message}")

class BasicRuneCrafter:

  def __init__(self):
    pass

  @staticmethod
  def remove_user_materials(requestingUser : User, craftingRequirements: dict):
    ItemData.initialize()
    for material in craftingRequirements.keys():
      ItemData.destroy_user_items_with_limit(
        owner=requestingUser,
        itemType=material,
        limit=craftingRequirements[material]
      )

  @staticmethod
  def craft_item():
    pass
  @staticmethod
  def craft_ruby_rune(requestingUser: User):
    userInventory: Inventory = InventoryData.get_inventory(requestingUser)

    # if more than 3 rocks, can craft a ruby rune
    if RubyRune.has_crafting_requirements(inventory=userInventory, reqs=RubyRune.crafting_requirements()):
      RuneData.initialize()
      newRubyRune = RubyRune(
        owner=requestingUser,
        id=0
      )
      RuneData.create_rune(newRubyRune)
      BasicRuneCrafter.remove_user_materials(requestingUser, RubyRune.crafting_requirements())
      ## Delete craftables stuff from requirements
    else:
      raise RuneCraftingException("in order to craft a ruby, you need 3 rocks.")

