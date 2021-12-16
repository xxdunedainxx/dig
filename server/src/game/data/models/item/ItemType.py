from src.core.data.Model import Model



class ItemType(Model):


  def __init__(self, name: str, rollChance: float, id: str):
    super(Model, self).__init__()

    self.name = name
    self.roll_chance = rollChance
    self.id = id

  def serialize(self) -> dict:
    return {
      "name" : self.name,
      "roll_chance" : self.roll_chance,
      "id" : self.id
    }

  @staticmethod
  def id_to_item(id):
    ITEM_IDS = {
      'rock': ItemType.rock,
      'ruby': ItemType.ruby
    }
    return ITEM_IDS[id]()

  @staticmethod
  def rock():
    return ItemType(
      name="rock",
      rollChance=1,
      id="rock"
    )

  @staticmethod
  def ruby():
    return ItemType(
      name="ruby",
      rollChance=.25,
      id="ruby"
    )