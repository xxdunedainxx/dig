from src.core.data.Model import Model

from datetime import datetime

class User(Model):

  def __init__(self,
               username: str,
               password: str,
               email: str,
               lastLogin: datetime,
               energy: int,
               level: int,
               id: int
    ):
    super(Model, self).__init__()

    self.username = username
    self.password = password
    self.email = email
    self.last_login = lastLogin
    self.energy = int(energy)
    self.level = int(level)
    self.id = int(id) if id is not None else None

  def serialize(self) -> dict:
    return {
      "username" : self.username,
      "password" : self.password,
      "last_login" : self.last_login,
      "energy": self.energy,
      "level": self.level,
      "id": self.id
    }

  def reduce_energy(self, reduction: int):
    self.energy = self.energy - reduction

  @staticmethod
  def deserialize(obj: dict):
    return User(
      username=obj["username"],
      password=obj["password"],
      email=obj["email"],
      lastLogin=obj["last_login"] if "last_login" in obj.keys() else datetime.now(),
      energy=obj["energy"] if "energy" in obj.keys() else 1,
      level=obj["level"] if "level" in obj.keys() else 1,
      id=obj["id"] if "id" in obj.keys() else None
    )