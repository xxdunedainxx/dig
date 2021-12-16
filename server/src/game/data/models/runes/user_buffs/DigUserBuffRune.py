from src.core.idm.data.model.User import User
from src.game.data.models.runes.DigRune import DigRune

class DigUserBuffRune(DigRune):

  def __init__(self, owner: User, id: int):
    DigRune.__init__(self,owner, id=id)

  # Applies buff to owner
  def apply_buff(self, owner: User, stackableMultiplier: int = 1) -> User:
    # Default no-op rune
    return owner