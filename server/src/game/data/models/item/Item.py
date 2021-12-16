from src.core.data.Model import Model
from src.core.idm.data.model.User import User
from src.game.data.models.item.ItemType import ItemType

class Item(Model):

  def __init__(self, owner: User, itemType: ItemType, id=None):
    super(Model, self).__init__()

    self.owner = owner
    self.item_type = itemType
    self.id = id

  def serialize(self) -> dict:
    return {
      "owner" : self.owner.serialize(),
      "item_type" : self.item_type.serialize(),
      "id" : self.id
    }