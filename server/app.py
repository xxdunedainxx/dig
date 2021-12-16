from src.core.util.LogFactory import LogFactory
from src.core.util.ErrorFactory import errorStackTrace
from src.App import App
from src.core.threading.ExitHandlers import ExitHandlers

def main():
  try:
    ExitHandlers.catch_all_signals()
    app: App = App()
    app.run()
  except Exception as e:
    LogFactory.MAIN_LOG.error(f"something went wrong :( {errorStackTrace(e)}")
    exit(-1)

if __name__ == "__main__":
  LogFactory.main_log()
  LogFactory.MAIN_LOG.info('running main app')
  main()