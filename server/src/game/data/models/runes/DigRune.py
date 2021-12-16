from src.game.data.models.runes.Craftable import Craftable
from src.core.idm.data.model.User import User



class DigRune(Craftable):

  def __init__(self, owner: User, id):
    super(Craftable, self).__init__()

    self.owner = owner
    self.type = self.__class__.__name__
    self.id = id

  def serialize(self) -> dict:
    return {
      "owner" : self.owner.serialize(),
      "name" : self.type,
      "id" : self.id,
      "crafting_requirements" : DigRune.crafting_requirements()
    }

