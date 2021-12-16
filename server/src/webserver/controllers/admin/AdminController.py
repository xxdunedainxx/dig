"""
Example requests:

GET all users

curl http://0.0.0.0/admin/users \
   -H 'Content-Type: application/json'
"""

from src.core.util.LogFactory import LogFactory
from src.webserver.decorators.HTTPLogger import http_logger
from src.webserver.WebServer import WebServerInit
from src.core.util.ErrorFactory import errorStackTrace

from flask import Flask, jsonify, request

from src.core.idm.data.model.User import User
from src.core.idm.data.db.UserData import UserData

flask_ref: Flask = WebServerInit.flask

class AdminController:

  def __init__(self):
    LogFactory.MAIN_LOG.info('Start AdminController')

  @staticmethod
  @flask_ref.route('/admin/users', methods=['GET'])
  @http_logger
  def admin_api():
    try:
      UserData.initialize()
      allUsers = UserData.fetch_all_users()
      rUsers = []
      for user in allUsers:
        rUsers.append(user.serialize())
      return {"users": rUsers},200
    except Exception as e:
      LogFactory.MAIN_LOG.error(f"Failed admin api {errorStackTrace(e)}")
      return {
        "response" : "sadness"
      }, 500