"""
Example requests:

POST create user:

curl -X POST http://0.0.0.0/craft \
   -H 'Content-Type: application/json' \
   -d '{"user":{"id":1,"username" :"test user", "email" :"some email", "password" :"some password"},"craftType":"rubyRune"}'
"""

from src.core.util.LogFactory import LogFactory
from src.webserver.decorators.HTTPLogger import http_logger
from src.webserver.WebServer import WebServerInit
from src.core.util.ErrorFactory import errorStackTrace

from flask import Flask, jsonify, request

from src.core.idm.data.model.User import User
from src.core.idm.data.db.UserData import UserData
from src.game.crafting.Craft import Crafter, CraftResponse

flask_ref: Flask = WebServerInit.flask

class CraftingController:

  def __init__(self):
    LogFactory.MAIN_LOG.info('Start CraftingController')

  @staticmethod
  @flask_ref.route('/craft', methods=['POST'])
  @http_logger
  def craft_api():
    try:
      UserData.initialize()
      userObj: User= UserData.get_user(request.json["user"]["id"])
      craftType: str = request.json["craftType"]
      rMessage: CraftResponse =  Crafter.craft(craftType, userObj)
      if rMessage.succuessful:
        return {"message" : "Item crafted?"},200
      else:
        return {"message" : f"Failed to craft item '{rMessage.message}'"}, 404
    except Exception as e:
      LogFactory.MAIN_LOG.error(f"Failed dig api {errorStackTrace(e)}")
      return {
        "response" : "sadness"
      }, 500