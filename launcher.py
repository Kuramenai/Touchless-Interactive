import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, \
QLabel, QButtonGroup
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPalette, QColor, QFont


class HomeScreen(QMainWindow):
    def __init__(self):
        super(HomeScreen, self).__init__()

        self.setWindowTitle("Pi Media Center")
        self.setFixedSize(QSize(640, 480))

        self.home_layout = QVBoxLayout()

        #Welcome Message
        self.welcome_message = QLabel()
        self.welcome_message.setText("Welcome to Pi Media Center")
        self.welcome_message.setFont(QFont("Sanserif", 20))
        self.welcome_message.setAlignment(Qt.AlignCenter|Qt.AlignTop)

        self.home_layout.addWidget(self.welcome_message)

        #Menu
        self.menu = QButtonGroup()

        self.pictures_button = QPushButton('PICTURES')
        self.music_button = QPushButton('MUSIC')
        self.videos_button = QPushButton('VIDEOS')

        self.menu.addButton(self.pictures_button, 1)
        self.menu.addButton(self.music_button, 2)
        self.menu.addButton(self.videos_button, 3)

        self.pictures_button.setFont(QFont("Sanserif", 15))
        self.music_button.setFont(QFont("Sanserif", 15))
        self.videos_button.setFont(QFont("Sanserif", 15))

        self.menu_layout = QHBoxLayout()
        self.menu_layout.addWidget(self.pictures_button)
        self.menu_layout.addWidget(self.music_button)
        self.menu_layout.addWidget(self.videos_button)

        self.home_layout.addLayout(self.menu_layout)

        #The Whole Home Screen
        self.home = QWidget()
        self.home.setLayout(self.home_layout)

        
        self.setCentralWidget(self.home)

        

class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()

        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)




app = QApplication(sys.argv)

Home = HomeScreen()
Home.show()

app.exec()
