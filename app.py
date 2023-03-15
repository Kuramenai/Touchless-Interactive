from PyQt5.QtWidgets import QApplication
from home_screen import HomeMenu
from home_screen.launcher import HomeScreen


if __name__ == "__main__":

    import sys

    if __name__ == "__main__":
        app = QApplication(sys.argv)

        window = HomeScreen()
        window.show()

        app.exec_()