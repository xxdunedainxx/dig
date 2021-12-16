from src.core.data.Model import Model
from src.game.data.models.item.Inventory import Inventory
from src.core.idm.data.model.User import User
from src.game.data.db.item.ItemData import ItemData

class CraftResponse:

  def __init__(self, message: str, successful: bool):
    self.message = message
    self.succuessful = successful

class Craftable(Model):

  @staticmethod
  def crafting_requirements(**kwargs) -> dict:
    return {}

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
  def has_crafting_requirements(inventory: Inventory, reqs: dict) -> bool:
    for req in reqs:
      if req in inventory.item_buckets.keys() and len(inventory.item_buckets[req]) >= reqs[req]:
        continue
      else:
        return False
    return True

  @staticmethod
  def craft(requestingUser: User, userInventory: Inventory) -> CraftResponse:
    return CraftResponse(message="This craftable is not implemented, nothing happened", successful=False)