from src.game.data.models.runes.pool_buffs.RubyRune import RubyRune
from src.game.data.models.runes.user_buffs.EnergyRune import EnergyRune
from src.game.data.models.runes.DigRune import DigRune
from src.core.idm.data.model.User import User

class DigRuneFactory:

  DIG_RUNE_MAPPING = {
    "RubyRune" : RubyRune,
    "EnergyRune" : EnergyRune
  }

  def __init__(self):
    pass

  @staticmethod
  def get_rune(runeType: str, owner: User, id: int) -> DigRune:
    return DigRuneFactory.DIG_RUNE_MAPPING[runeType](owner, id)