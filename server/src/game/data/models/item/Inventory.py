from src.core.data.Model import Model
from src.core.idm.data.model.User import User
from src.game.data.models.item.Item import Item

# TODO Rune inventory
class Inventory(Model):

  def __init__(self, items, runes, owner: User):
    super(Model, self).__init__()
    self.items = items
    self.runes = runes
    self.owner = owner
    self.item_buckets = {}
    self.rune_buckets = {}

    self.__setup_item_buckets()
    self.__setup_rune_buckets()


  def __setup_item_buckets(self):
    for item in self.items:
      if item.item_type.name in self.item_buckets.keys():
        self.item_buckets[item.item_type.name].append(item.item_type)
      else:
        self.item_buckets[item.item_type.name] = []
        self.item_buckets[item.item_type.name].append(item.item_type)

  def __setup_rune_buckets(self):
    for rune in self.runes:
      if rune.type in self.rune_buckets.keys():
        self.rune_buckets[rune.type].append(rune.type)
      else:
        self.rune_buckets[rune.type] = []
        self.rune_buckets[rune.type].append(rune)

  def __serialize_items(self):
    sItems = []
    for item in self.items:
      sItems.append(item.serialize())
    return sItems

  def __serialize_runes(self):
    rRunes = []
    for rune in self.runes:
      rRunes.append(rune.serialize())
    return rRunes

  def __get_items_printable(self):
    pItems = ""
    i=1

    for item in self.item_buckets.keys():
      pItems+=f"\n[{len(self.item_buckets[item])}] {item}"
      i+=1
    return pItems

  def __get_runes_printable(self):
    pRunes = ""
    i=1

    for rune in self.rune_buckets.keys():
      pRunes+=f"\n[{len(self.rune_buckets[rune])}] {rune}"
      i+=1
    return pRunes

  def serialize(self) -> dict:

    rObj = {
      "items" : self.__serialize_items(),
      "runes" : self.__serialize_runes(),
      "owner" : self.owner.serialize()
    }
    return rObj

  def print_inventory(self):

    return f""" 
      {self.owner.username}'s Inventory: \n
      Items: \n
      {self.__get_items_printable()}
      Runes: \n
      {self.__get_runes_printable()}
    """