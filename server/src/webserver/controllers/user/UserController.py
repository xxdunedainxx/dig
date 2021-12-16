"""
Example requests:

POST create user:

curl -X POST http://0.0.0.0/user \
   -H 'Content-Type: application/json' \
   -d '{"username" :"test user", "email" :"zrmmaster@aol.com", "password" :"some password"}'
"""

from src.core.util.LogFactory import LogFactory
from src.webserver.decorators.HTTPLogger import http_logger
from src.webserver.WebServer import WebServerInit
from src.core.util.ErrorFactory import errorStackTrace

from flask import Flask, jsonify, request

from src.core.idm.data.model.User import User
from src.core.idm.user_mgmt.UserManagement import UserManagement

flask_ref: Flask = WebServerInit.flask

class UserController:

  def __init__(self):
    LogFactory.MAIN_LOG.info('Start TestController')

  @staticmethod
  def __validate_create_user_payload(payload) -> bool:
    return True

  @staticmethod
  def process_usermgmt_post_request(request):
    if UserController.__validate_create_user_payload(request.json) == False:
      return {"message": "bad request"}, 404
    else:
      try:
        userObj: User=User.deserialize(request.json)
        UserManagement.create_user(userObj)
        return {"message": "ok"}, 200
      except Exception as e:
        return {"message" : "bad request"},404

  @staticmethod
  def process_usermgmt_patch_request(request):
    try:
      userObj: User=User.deserialize(request.json)
      UserManagement.update_user(userObj)
      return {"message": "ok"}, 200
    except Exception as e:
      return {"message" : "bad request"},404


  @staticmethod
  @flask_ref.route('/user', methods=['POST','PATCH'])
  @http_logger
  def user_management_api():
    try:
      if request.method == 'POST':
        return UserController.process_usermgmt_post_request(request)
      elif request.method == 'PATCH':
        return UserController.process_usermgmt_patch_request(request)
      else:
        return {"message" : "invalid request"}, 400
    except Exception as e:
      LogFactory.MAIN_LOG.error(f"Failed user management api {errorStackTrace(e)}")
      return {
        "response" : "sadness"
      }, 500