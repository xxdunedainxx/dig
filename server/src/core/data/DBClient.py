from typing import Any

class DBClient:
  INSTANCE = None
  INSTANCES = []

  def __init__(self):
    pass


  @staticmethod
  def generate_db_client(**kwargs):
    pass

  @staticmethod
  def get_db_client(**kwargs):
    pass

  def request(self, request: Any, params: Any=None):
    raise NotImplementedError('request not implemented')