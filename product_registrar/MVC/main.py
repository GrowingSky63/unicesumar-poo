from .interface.console import ConsoleApp


def main() -> None:
    app = ConsoleApp()
    app.executar()


if __name__ == "__main__":
    main()

