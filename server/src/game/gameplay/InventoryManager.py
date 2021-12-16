from src.game.data.db.item.InventoryData import InventoryData
from src.core.idm.data.model.User import User

class InventoryManager:

  def __init__(self):
    pass

  @staticmethod
  def get_inventory(user: User):
    InventoryData.initialize()
    return InventoryData.get_inventory(user)