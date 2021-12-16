from src.core.util.LogFactory import LogFactory
from src.webserver.decorators.HTTPLogger import http_logger
from src.webserver.WebServer import WebServerInit
from src.core.util.ErrorFactory import errorStackTrace

from flask import Flask, jsonify, request

flask_ref: Flask = WebServerInit.flask

class TestController:

  def __init__(self):
    LogFactory.MAIN_LOG.info('Start TestController')

  @staticmethod
  @flask_ref.route('/test', methods=['GET'])
  @http_logger
  def test_api():
    try:
      LogFactory.MAIN_LOG.info("test api")
      return {
        "response" : "hello world"
      }
    except Exception as e:
      LogFactory.MAIN_LOG.error(f"Failed Fetching test api {errorStackTrace(e)}")
      return {
        "response" : "sadness"
      }, 500