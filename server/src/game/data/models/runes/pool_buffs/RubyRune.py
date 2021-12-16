from src.core.idm.data.model.User import User
from src.game.data.models.runes.pool_buffs.DigPoolBuffRune import DigPoolBuffRune
from src.game.data.models.runes.Craftable import CraftResponse
from src.game.data.models.item.ItemType import ItemType

from src.game.data.models.item.Inventory import Inventory
from src.game.data.db.rune.RuneData import RuneData
from src.core.idm.data.model.User import User

### Increases chances of getting a ruby by 1%
class RubyRune(DigPoolBuffRune):

  def __init__(self, owner: User, id: int):
    DigPoolBuffRune.__init__(self,owner, id=id, poolPercentage=.1)

  # Override to add ruby instead
  def item_to_add(self):
    return ItemType.ruby()

  @staticmethod
  def crafting_requirements():
    return {
      "rock" : 3
    }

  @staticmethod
  def craft(requestingUser: User, userInventory :Inventory) -> CraftResponse:

    # if more than 3 rocks, can craft a ruby rune
    if RubyRune.has_crafting_requirements(inventory=userInventory, reqs=RubyRune.crafting_requirements()):
      RuneData.initialize()
      newRubyRune = RubyRune(
        owner=requestingUser,
        id=0
      )
      RuneData.create_rune(newRubyRune)
      RubyRune.remove_user_materials(requestingUser, RubyRune.crafting_requirements())

      ## Delete craftables stuff from requirements
      return CraftResponse(message="Crafted ruby!", successful=True)
    else:
      return CraftResponse(message=f"in order to craft a ruby, you need: {RubyRune.crafting_requirements()}", successful=False)