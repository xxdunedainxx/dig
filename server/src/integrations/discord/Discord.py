from src.core.Configuration import CONF_INSTANCE
from src.core.util.LogFactory import LogFactory
from src.core.util.ErrorFactory import errorStackTrace
from src.core.util.StringFormatters import StringFormatters

from src.core.security.Authentication import Authentication

from src.core.idm.data.model.User import User
from src.core.idm.data.db.UserData import UserData
from src.core.idm.user_mgmt.UserManagement import UserManagement
from src.game.gameplay.InventoryManager import InventoryManager

from src.game.data.models.item.ItemType import ItemType
from src.game.gameplay.Dig import Dig
from src.game.crafting.Craft import Crafter,CraftResponse
from src.core.Setup import Setup

from datetime import datetime
import discord
import os
from functools import wraps

def authenticate_discord_user(discord_msg_handler):
  @wraps(discord_msg_handler)
  async def authenticate_discord_user_wrapper(*args, **kwargs):
    message: discord.Message = args[0]
    LogFactory.MAIN_LOG.info(f"Checking if user is authed {message.author.name}")
    if message.author.id in DiscordIntegration.logged_in_users.keys():
      dSession: DiscordSession = DiscordIntegration.logged_in_users[message.author.id]
      if dSession.is_timed_out() == False:
        return await discord_msg_handler(*args, **kwargs)
      else:
        await message.channel.send(":poop: Your session has timed out, please log back in..")
        return
    else:
      await message.channel.send(":no_entry: You are not logged in... :)")
      return

  return authenticate_discord_user_wrapper
def discord_message_logger(discord_msg_handler):
  @wraps(discord_msg_handler)
  def logger_wrapper(*args, **kwargs):
    message: discord.Message = args[0]
    LogFactory.MAIN_LOG.info(f"message request from {message.author.name}. Content: {message.content}")
    return discord_msg_handler(*args, **kwargs)

  return logger_wrapper

class DiscordUser:

  def __init__(self, appUser: User, discordUser):
    self.appUser = appUser
    self.discUser = discordUser

  def get_app_user(self):
    self.appUser = UserData.get_user_by_email(self.appUser.email)
    return self.appUser

class DiscordSession:

  def __init__(self, discordUser: DiscordUser):
    self.user: DiscordUser = discordUser
    self.discord_login: datetime = datetime.now()

  def is_timed_out(self):
    if ((datetime.now() - self.discord_login).seconds / 60) > CONF_INSTANCE.DISCORD["USER_SESSION_TIMEOUT_MINUTES"]:
      return True
    else:
      return False

class DiscordIntegration:

  LOGIN_REQUEST_QUEUE_ITEM = "LOGIN_REQUEST"
  REGISTER_ACCOUNT_QUEUE_ITEM = "REGISTER_ACCOUNT"

  # Mapping of userID:queueItem
  MESSAGE_REQUEST_QUEUE = {

  }

  login_request_queue = []
  register_account_queue = []
  logged_in_users = {

  }

  instance = None

  @staticmethod
  @discord_message_logger
  async def queue_user_request(message: discord.Message, queueType: str) -> bool:
    if DiscordIntegration.user_has_message_queue_request(message):
      await message.channel.send(f"You must cancel your current open request, \"{DiscordIntegration.MESSAGE_REQUEST_QUEUE[message.author.id]}\", via the 'digCancel' command")
      return False
    else:
      DiscordIntegration.MESSAGE_REQUEST_QUEUE[message.author.id] = queueType
      return True


  @staticmethod
  def user_has_message_queue_request(message: discord.Message) -> bool:
    return message.author.id in DiscordIntegration.MESSAGE_REQUEST_QUEUE.keys()

  @staticmethod
  def user_has_login_request(message: discord.Message) -> bool:
    return DiscordIntegration.user_has_message_queue_request(message) and DiscordIntegration.MESSAGE_REQUEST_QUEUE[message.author.id] == DiscordIntegration.LOGIN_REQUEST_QUEUE_ITEM

  @staticmethod
  def user_has_register_account_request(message: discord.Message) -> bool:
    return DiscordIntegration.user_has_message_queue_request(message) and DiscordIntegration.MESSAGE_REQUEST_QUEUE[
      message.author.id] == DiscordIntegration.REGISTER_ACCOUNT_QUEUE_ITEM

  @staticmethod
  @discord_message_logger
  async def cancel_user_queue_request(message: discord.Message) -> None:
    if DiscordIntegration.user_has_message_queue_request(message):
      DiscordIntegration.MESSAGE_REQUEST_QUEUE.pop(message.author.id)
      await message.channel.send(':white_check_mark: Your request has been canceled.')
    else:
      await message.channel.send('?You dont have any open requests?')

  @staticmethod
  def start_discord_in_thread():
    Setup.init_thread_resources()
    DiscordIntegration.instance = DiscordIntegration()
    DiscordIntegration.instance.run()

  @staticmethod
  def parsed_commands_help_output():
    output = ""

    for parsed_cmd in PARSED_CMDS_HELP.keys():
      output+=f"\n:keyboard: **Command**: {parsed_cmd}\n:information_source: **Example**: {PARSED_CMDS_HELP[parsed_cmd]}"
    return output

  @staticmethod
  def single_commands_help_output():
    output = ""

    for cmd_help in SINGLE_COMMANDS_INFO.keys():
      output+=f"\n:keyboard: **Command:** {cmd_help}\n:information_source: **Description:** {SINGLE_COMMANDS_INFO[cmd_help]}\n"
    return output

  @staticmethod
  @discord_message_logger
  @authenticate_discord_user
  async def print_user_info(message: discord.message):
    userInfo: User = DiscordIntegration.logged_in_users[message.author.id].user.get_app_user()

    prettyPrintUserInfo = f"""
User INFO:
Username:{userInfo.username}
Current Energy Level: {userInfo.energy}
Last Login: {userInfo.last_login}
Email: {userInfo.email}
""".strip()
    await message.channel.send(prettyPrintUserInfo)


  @staticmethod
  @discord_message_logger
  @authenticate_discord_user
  async def dig_rock(message):
    await message.channel.send("digging..........")
    itemDug: ItemType = Dig.dig(ItemType.rock().id, DiscordIntegration.logged_in_users[message.author.id].user.get_app_user())
    await message.channel.send(itemDug)

  @staticmethod
  @discord_message_logger
  @authenticate_discord_user
  async def dig_rock_ruby(message):
    await  message.channel.send("digging..........")
    itemDug: ItemType = Dig.dig(ItemType.ruby().id, DiscordIntegration.logged_in_users[message.author.id].user.get_app_user())
    await  message.channel.send(itemDug)

  @staticmethod
  @discord_message_logger
  async def login_request(message):
    if await DiscordIntegration.queue_user_request(message, queueType=DiscordIntegration.LOGIN_REQUEST_QUEUE_ITEM) == True:
      await message.channel.send('Ok... please provide your email and password in the format: \'email:password\'')

  @staticmethod
  @discord_message_logger
  async def dig_help(message):
    digHelpDebugString = ":exclamation: THIS IS A DEBUG BOT :exclamation:" if CONF_INSTANCE.DEBUG == True else ''
    await message.channel.send(f"""{digHelpDebugString}
:printer:  A list of all available single DIG commands:\n {DiscordIntegration.single_commands_help_output()}
\n:printer:  A list of all available chained commands:\n {DiscordIntegration.parsed_commands_help_output()}""")

  @staticmethod
  @discord_message_logger
  @authenticate_discord_user
  async def dig_check_login(message):
    if message.author.id in DiscordIntegration.logged_in_users.keys():
      await message.channel.send("You are logged in :)")
    else:
      await  message.channel.send("You are not logged in... :)")

  @staticmethod
  @discord_message_logger
  async def dig_register_user_request(message):
    if await DiscordIntegration.queue_user_request(message, queueType=DiscordIntegration.REGISTER_ACCOUNT_QUEUE_ITEM) == True:
      await message.channel.send('Ok... please provide your account details in the form "username,email,password"')

  @staticmethod
  @discord_message_logger
  @authenticate_discord_user
  async def dig_inventory(message):
    inv=InventoryManager.get_inventory(DiscordIntegration.logged_in_users[message.author.id].user.get_app_user()).print_inventory(inventoryHeaderAvatar=":card_box:", itemHeaderAvatar=":rock:", runesHeaderAvatar=":crystal_ball:")
    await message.channel.send(f"Current inventory: {inv}")

  @staticmethod
  @discord_message_logger
  @authenticate_discord_user
  async def craft(message):
    itemToCraft = message.content.split(":")[1]
    resp: CraftResponse = Crafter.craft(itemToCraft,DiscordIntegration.logged_in_users[message.author.id].user.get_app_user())
    await message.channel.send(resp.message)



  @staticmethod
  def get_discord_integration():
    if DiscordIntegration.instance == None:
      DiscordIntegration.instance = DiscordIntegration()
    return DiscordIntegration.instance

  def __init__(self):
    self.client = None
    if CONF_INSTANCE.DISCORD["token"] != None and CONF_INSTANCE.DISCORD["enabled"] != False:
      LogFactory.MAIN_LOG.info("discord enabled!")
      self.setup_discord_client()
    else:
      LogFactory.MAIN_LOG.info("discord not enabled!")

  def run(self):
    self.client.run(CONF_INSTANCE.DISCORD['token'])

  async def process_login_request(self, message):
    if ":" in message.content:
      msgSplit = message.content.split(':')
      if Authentication.authenticate_user(msgSplit[0], msgSplit[1]):
        appUser = UserData.get_user_by_email(msgSplit[0])
        DiscordIntegration.logged_in_users[message.author.id] = \
        DiscordSession(
          discordUser=DiscordUser(
            appUser=appUser,
            discordUser=message.author
          )
        )
        await message.channel.send(":white_check_mark: You are authenticated!")
        DiscordIntegration.MESSAGE_REQUEST_QUEUE.pop(message.author.id)
      else:
        await message.channel.send(":no_entry: failed to authenticate :(")

  async def process_account_registration(self, message):
    if "," in message.content:
      userInfo = message.content.split(',')
      userObj = User(
        username = userInfo[0],
        email=userInfo[1],
        password=userInfo[2],
        lastLogin=datetime.now(),
        energy=1,
        level=1,
        id=10000000000
      )
      create = UserManagement.create_user(userObj)

      if create:
        await message.channel.send('you have been registered :)"')
        DiscordIntegration.MESSAGE_REQUEST_QUEUE.pop(message.author.id)
      else:
        await message.channel.send('something wasn\'t formatted right... Maybe check your email formatting? Or another account is already registered with the same email ... :( ... :)')
    else:
      await message.channel.send('REMEMBER THE FORMAT MUST BE: "username,email,password"')

  async def check_queued_requests(self, message):
    if DiscordIntegration.user_has_login_request(message):
      await self.process_login_request(message)
    elif DiscordIntegration.user_has_register_account_request(message):
      await self.process_account_registration(message)

  def __get_avatar_bytes(self) -> bytes:
    p=os.getcwd()
    with open("./assets/dig_avatar.png", "rb") as image:
      f = image.read()
      b = bytearray(f)
      return b

  def setup_discord_client(self):
    # self.avatar = self.__get_avatar_bytes()
    self.client: discord.Client = discord.Client()
    @self.client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(self.client))

        await self.client.user.edit(username=f"digBot")



    @self.client.event
    async def on_message(message):
        try:
          if message.author == self.client.user:
              return

          await self.check_queued_requests(message)

          if message.content.lower() in COMMANDS.keys():
              message.content = message.content.lower()
              await COMMANDS[message.content](message)
          else:
            for parse_cmd in PARSED_COMMANDS.keys():
              parse_cmd=parse_cmd.lower()
              if parse_cmd in message.content:
                await PARSED_COMMANDS[parse_cmd](message)
                break
        except Exception as e:
          LogFactory.MAIN_LOG.error(f"Failed to process message with error {errorStackTrace(e)} for message {message.content}")

def debug_string_injection():
  return 'debug' if CONF_INSTANCE.DEBUG == True else ''

COMMANDS = {
  f"{debug_string_injection()}diglogin": DiscordIntegration.login_request,
  f"{debug_string_injection()}dighelp" : DiscordIntegration.dig_help,
  f"{debug_string_injection()}diglogincheck" : DiscordIntegration.dig_check_login,
  f"{debug_string_injection()}digrock"  : DiscordIntegration.dig_rock,
  f"{debug_string_injection()}digregisteraccount" : DiscordIntegration.dig_register_user_request,
  f"{debug_string_injection()}diginventory" : DiscordIntegration.dig_inventory,
  f"{debug_string_injection()}digprofile" : DiscordIntegration.print_user_info,
  f"{debug_string_injection()}digcancel" : DiscordIntegration.cancel_user_queue_request
}

SINGLE_COMMANDS_INFO = {
  f"{debug_string_injection()}diglogin": "Login to the dig server",
  f"{debug_string_injection()}dighelp": "Get help, lol",
  f"{debug_string_injection()}diglogincheck": "Check if you are logged in",
  f"{debug_string_injection()}digrock": "Dig something",
  f"{debug_string_injection()}digregisteraccount": "Create a new dig account",
  f"{debug_string_injection()}diginventory": "Print your current inventory",
  f"{debug_string_injection()}digprofile" : "Print your profile info",
  f"{debug_string_injection()}digcancel" : "Cancel an outstanding request"
}

PARSED_COMMANDS = {
  f"{debug_string_injection()}digcraft:" : DiscordIntegration.craft
}

PARSED_CMDS_HELP = {
  f"{debug_string_injection()}digcraft:" : "digcraft:rubyRune"
}
