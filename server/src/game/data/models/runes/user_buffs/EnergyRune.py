from src.core.idm.data.model.User import User
from src.game.data.models.runes.user_buffs.DigUserBuffRune import DigUserBuffRune

from src.game.data.models.runes.Craftable import CraftResponse

from src.game.data.models.item.Inventory import Inventory
from src.game.data.db.rune.RuneData import RuneData
from src.core.idm.data.model.User import User

class EnergyRune(DigUserBuffRune):

  def __init__(self, owner: User, id: int):
    DigUserBuffRune.__init__(self,owner, id=id)

  # Applies buff to owner. Gives owner +1 energy per energy rune
  def apply_buff(self, owner: User, stackableMultiplier: int = 1) -> User:
    owner.energy+=(1 * stackableMultiplier)
    return owner

  @staticmethod
  def crafting_requirements():
    return {
      "rock" : 1
    }

  @staticmethod
  def craft(requestingUser: User, userInventory :Inventory) -> CraftResponse:

    # if more than 3 rocks, can craft a ruby rune
    if EnergyRune.has_crafting_requirements(inventory=userInventory, reqs=EnergyRune.crafting_requirements()):
      RuneData.initialize()
      newEnergyRune = EnergyRune(
        owner=requestingUser,
        id=0
      )
      RuneData.create_rune(newEnergyRune)
      EnergyRune.remove_user_materials(requestingUser, EnergyRune.crafting_requirements())

      ## Delete craftables stuff from requirements
      return CraftResponse(message="Crafted energy rune!", successful=True)
    else:
      return CraftResponse(message=f"in order to craft an energy rune, you need: {EnergyRune.crafting_requirements()}", successful=False)