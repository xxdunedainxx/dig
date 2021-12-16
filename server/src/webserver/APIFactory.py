from src.webserver.WebServer import WebServerInit

from src.core.Configuration import CONF_INSTANCE
from src.core.Setup import Setup
from src.core.util.LogFactory import LogFactory

class APIFactory:

    instance = None

    @staticmethod
    def generate_api_factory():
      if APIFactory.instance == None:
        APIFactory.instance = APIFactory()

      return APIFactory.instance

    def __init__(self):
        WebServerInit.init_flask()
        self.prep_controllers()

    def run(self, port: int = CONF_INSTANCE.FLASK_PORT_BIND):
        LogFactory.MAIN_LOG.info(f"Running API server, binding to  {CONF_INSTANCE.FLASK_HOST_BIND}:{port}")
        WebServerInit.flask.run (
            host=CONF_INSTANCE.FLASK_HOST_BIND,
            port=port,
            debug=False,
        )

    def prep_controllers(self):
      LogFactory.MAIN_LOG.info("Setting up API Server controllers")
      from src.webserver.controllers.test.TestController import TestController
      self.test_controller: TestController = TestController()
      from src.webserver.controllers.user.UserController import UserController
      self.user_controller: UserController = UserController()
      from src.webserver.controllers.admin.AdminController import AdminController
      self.adm_controller = AdminController()
      from src.webserver.controllers.digging.DigController import DigController
      self.dig_controller = DigController()
      from src.webserver.controllers.inventory.InventoryController import InventoryController
      self.inventory_controller = InventoryController()
      from src.webserver.controllers.crafting.CraftingController import CraftingController
      self.craft_controller = CraftingController()

    @staticmethod
    def run_api_in_thread():
      Setup.init_thread_resources()
      LogFactory.MAIN_LOG.info("Starting API Server in thread")
      APIFactory.instance = APIFactory()
      APIFactory.instance.run()
