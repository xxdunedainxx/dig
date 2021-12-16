from src.core.data.Model import Model
from src.game.data.models.item.ItemType import ItemType

import random

class DigType(Model):


  def __init__(self, requiredLevel: int, energyRequired: int, pool: [], id: int):
    super(Model, self).__init__()

    self.required_level = requiredLevel
    self.energy_required = energyRequired
    self.pool = pool
    self.id = id


  def serialize(self) -> dict:
    return {
      "required_level" : self.required_level,
      "energy_required" : self.energy_required,
      "pool" : self.pool,
      "id" : self.id
    }

  def dig(self):
    return random.choice(self.pool)

  @staticmethod
  def id_to_dig_type(id):
    ITEM_IDS = {
      'rock': DigType.dig_rock,
      'ruby': DigType.big_dig_ruby
    }
    return ITEM_IDS[id]()

  @staticmethod
  def dig_rock():
    rockPool = [ItemType.rock() for _ in range(1000)]
    return DigType(
      requiredLevel=1,
      energyRequired=1,
      pool=rockPool,
      id=1
    )

  @staticmethod
  def big_dig_ruby():
    rockList = [ItemType.rock() for _ in range(90)]
    rubyList= [ItemType.ruby() for _ in range(10)]

    combinedList = []
    combinedList.extend(rockList)
    combinedList.extend(rubyList)

    return DigType(
      requiredLevel=1,
      energyRequired=1,
      pool=combinedList,
      id=2
    )