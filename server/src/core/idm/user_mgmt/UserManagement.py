from src.core.util.ErrorFactory import errorStackTrace
from src.core.util.LogFactory import LogFactory
from src.core.idm.data.model.User import User
from src.core.idm.data.db.UserData import UserData

from src.core.security.Validators import EmailValidator

class UserManagement:

  def __init__(self):
    pass

  @staticmethod
  def create_user(userReq: User) -> bool:
    LogFactory.MAIN_LOG.info(f"Attempting to create user: {userReq.email}")
    UserData.initialize()
    userReq = UserManagement.__format_user_data(userReq)
    if not EmailValidator.is_valid(email=userReq.email) or UserManagement.__check_email_in_use(userReq):
      return False
    else:
      UserData.create_user(userReq)
      return True

  @staticmethod
  def update_user(userReq: User) -> bool:
    LogFactory.MAIN_LOG.info(f"Attempting to update user: {userReq.email}")
    UserData.initialize()
    userReq = UserManagement.__format_user_data(userReq)
    if not EmailValidator.is_valid(email=userReq.email) or UserManagement.__check_email_in_use(userReq):
      LogFactory.MAIN_LOG.warning(f"Email provided is not valid or is already in use: {userReq.email}")
      return False
    else:
      UserData.update_user(userReq)
      return True

  @staticmethod
  def __format_user_data(useReq: User):
    useReq.username = useReq.username.replace(' ', '')
    useReq.password = useReq.password.replace(' ', '')
    useReq.email = useReq.email.replace(' ', '')
    return useReq

  @staticmethod
  def __check_email_in_use(userReq: User):
    return UserData.get_user_by_email(userReq.email) != None