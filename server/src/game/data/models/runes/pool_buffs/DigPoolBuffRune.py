from src.core.data.Model import Model
from src.core.idm.data.model.User import User
from src.game.data.models.runes.DigRune import DigRune
from src.game.data.models.item.ItemType import ItemType

### Increases chances of getting a ruby by 1%
class DigPoolBuffRune(DigRune):

  def __init__(self, owner: User, id: int, poolPercentage: float):
    DigRune.__init__(self,owner, id=id)

    self.pool_percentage = poolPercentage

  def serialize(self) -> dict:
    base=super(DigPoolBuffRune, self).serialize()
    base["pool_percentage"] = self.pool_percentage
    return base

  def item_to_add(self):
    return ItemType.rock()

  # Applies buff to owner
  def apply_buff(self, digPool: [], digPivot: int, stackableMultiplier: int = 1):
    sizeToApply = int(len(digPool) * (self.pool_percentage * stackableMultiplier))

    # remove items at pivot
    for i in range(sizeToApply):
      del digPool[digPivot]
      digPivot+=1
      if digPivot >= len(digPool):
        digPivot=0
    for i in range(sizeToApply):
      digPool.append(self.item_to_add())
    return digPool,digPivot