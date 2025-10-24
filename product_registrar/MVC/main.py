from .interface.console import ConsoleApp
from .database import init_db

def main() -> None:
  init_db()
  app = ConsoleApp()
  app.executar()

if __name__ == "__main__":
  main()

