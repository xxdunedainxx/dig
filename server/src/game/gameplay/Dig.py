from src.core.idm.data.model.User import User
from src.core.idm.data.db.UserData import UserData

from src.game.dig.DigType import DigType

from src.game.data.db.item.ItemData import ItemData
from src.game.data.models.item.Item import Item

from src.game.data.db.item.InventoryData import InventoryData
from src.game.data.models.item.Inventory import Inventory

from src.game.data.models.runes.pool_buffs.DigPoolBuffRune import DigPoolBuffRune

class Dig:

  def __init__(self):
    pass

  @staticmethod
  def apply_user_buffs_to_pool(pool: [], requestingUser: User):
    digPivot = 0

    userInv: Inventory = InventoryData.get_inventory(requestingUser)

    for rune in userInv.rune_buckets.keys():
      if issubclass(type(userInv.rune_buckets[rune][0]), DigPoolBuffRune):
        runeToApply: DigPoolBuffRune = userInv.rune_buckets[rune][0]
        pool, digPivot = runeToApply.apply_buff(
          pool,
          digPivot,
          len(userInv.rune_buckets[rune])
        )
    return pool

  @staticmethod
  def dig(idToDig: int, requestingUser: User):
    digToExecute: DigType = DigType.id_to_dig_type(idToDig)

    if digToExecute.required_level > requestingUser.level:
      return "You are not a high enough level to dig this item..."
    elif digToExecute.energy_required > requestingUser.energy:
      return f"You dont have enough energy..."
    else:
      digToExecute.pool = Dig.apply_user_buffs_to_pool(digToExecute.pool, requestingUser)

      itemDug=digToExecute.dig()
      ItemData.initialize()
      ItemData.create_item(
        Item(
          owner=requestingUser,
          itemType=itemDug
        )
      )

      requestingUser.reduce_energy(digToExecute.energy_required)
      UserData.initialize()
      UserData.update_user(requestingUser)
      return f"You dug {itemDug.name}!"

