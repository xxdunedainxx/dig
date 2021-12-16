"""
Example requests:

POST create user:

curl -X POST http://0.0.0.0/dig \
   -H 'Content-Type: application/json' \
   -d '{"user":{"id":1,"username" :"test user", "email" :"some email", "password" :"some password"},"digTypeId":1}'
"""

from src.core.util.LogFactory import LogFactory
from src.webserver.decorators.HTTPLogger import http_logger
from src.webserver.WebServer import WebServerInit
from src.core.util.ErrorFactory import errorStackTrace

from flask import Flask, jsonify, request

from src.core.idm.data.model.User import User
from src.core.idm.data.db.UserData import UserData
from src.game.gameplay.Dig import Dig

flask_ref: Flask = WebServerInit.flask

class DigController:

  def __init__(self):
    LogFactory.MAIN_LOG.info('Start DigController')

  @staticmethod
  @flask_ref.route('/dig', methods=['POST'])
  @http_logger
  def dig_api():
    try:
      UserData.initialize()
      userObj: User= UserData.get_user(request.json["user"]["id"])
      digTypeId: int = request.json["digTypeId"]
      objToObtain = Dig.dig(digTypeId, userObj)
      return {"message" : objToObtain},200
    except Exception as e:
      LogFactory.MAIN_LOG.error(f"Failed dig api {errorStackTrace(e)}")
      return {
        "response" : "sadness"
      }, 500