from src.core.idm.data.model.User import User
from src.core.idm.data.db.UserData import UserData

from datetime import datetime

from src.core.util.LogFactory import LogFactory

class Authentication:

  @staticmethod
  def authenticate_user(email: str, password: str):
    UserData.initialize()
    dbUser = UserData.get_user_by_email(email)

    if dbUser is not None and dbUser.password == password:
      LogFactory.MAIN_LOG.info(f"Authenticated user {email}")
      dbUser.last_login = datetime.now()
      UserData.register_login_time(dbUser)
      return True
    else:
      LogFactory.MAIN_LOG.info(f"Unable to auth user {email}")
      return False