"""
Example requests:

POST create user:

curl -X POST http://0.0.0.0/inventory \
   -H 'Content-Type: application/json' \
   -d '{"user":{"id":1,"username" :"test user", "email" :"some email", "password" :"some password"}}'
"""


from src.core.util.LogFactory import LogFactory
from src.webserver.decorators.HTTPLogger import http_logger
from src.webserver.WebServer import WebServerInit
from src.core.util.ErrorFactory import errorStackTrace

from flask import Flask, jsonify, request

from src.game.gameplay.InventoryManager import InventoryManager
from src.core.idm.data.model.User import User

flask_ref: Flask = WebServerInit.flask

class InventoryController:

  def __init__(self):
    LogFactory.MAIN_LOG.info('Start InventoryController')

  @staticmethod
  @flask_ref.route('/inventory', methods=['POST'])
  @http_logger
  def inventory_api():
    try:
      LogFactory.MAIN_LOG.info("inventory api")

      return {
        "inventory" : InventoryManager.get_inventory(User.deserialize(request.json["user"])).serialize()
      }, 200
    except Exception as e:
      LogFactory.MAIN_LOG.error(f"Failed Fetching InventoryController api {errorStackTrace(e)}")
      return {
        "response" : "sadness"
      }, 500