import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, \
     QLabel, QButtonGroup, QFrame
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPalette, QColor, QFont

from home_screen.homeMenu import HomeMenu


class HomeScreen(QMainWindow):
    def __init__(self):
        super(HomeScreen, self).__init__()
        self.__init_attr()
        self.__init_ui()
    
    def __init_attr(self):
        self.__welcomeMessage = QLabel()
        self.homeMenu = HomeMenu()
        self.selections = ['PICTURES', 'MUSIC', 'VIDEOS']
        self.currentSelection = QLabel()
        self.userDetectedGesture = QLabel()
        self.btnGroup = self.homeMenu.getButtonGroup()
        self.__myHomeWidget = QWidget()

    def __init_ui(self):
        self.setWindowTitle("Pi Media Center")
        self.setFixedSize(QSize(1080, 720))
      
        # Welcome Message
        self.__welcomeMessage.setText("Welcome to Pi Media Center")
        self.__welcomeMessage.setFont(QFont("Goudy Old Style", 20))
        self.__welcomeMessage.setAlignment(Qt.AlignCenter|Qt.AlignTop)

        # Menu
        self.__load_menu()
        self.homeMenu.setFixedSize(500, 500)

        # Current Selection
        self.btnGroup.idToggled.connect(self.print_current_selection)
        self.currentSelection.setText(self.selections[0])
        self.currentSelection.setFont(QFont("Consolas", 10))
        self.currentSelection.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        # User Detected Gesture
        self.userDetectedGesture.setText('')
        self.userDetectedGesture.setFont(QFont("Consolas", 10))
        self.userDetectedGesture.setAlignment(Qt.AlignCenter | Qt.AlignBottom)

        # layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 50, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.__welcomeMessage)
        layout.addWidget(self.homeMenu, alignment=Qt.AlignHCenter | Qt.AlignVCenter)
        layout.addWidget(self.currentSelection, stretch=-1000)
        layout.addWidget(self.userDetectedGesture)
        layout.insertStretch(-1, 1)

        self.__myHomeWidget.setLayout(layout)
        self.setStyleSheet('border: solid 2px')
        self.setCentralWidget(self.__myHomeWidget)
    
    def __load_menu(self):

        icons_dir = 'home_screen/icons'
        self.homeMenu.addPictures([f'{icons_dir}/pictures_r.png', f'{icons_dir}/music_r.png', \
                                     f'{icons_dir}/movies_r.png'])
        
        for btn in self.homeMenu.getButtonGroup().buttons():
            btn.setFixedSize(40, 20)

        prev_btn = self.homeMenu.getPrevBtn()
        prev_btn.setFixedSize(60, 60)
        next_btn = self.homeMenu.getNextBtn()
        next_btn.setFixedSize(60, 60)
    
    def print_current_selection(self):
        idx = self.btnGroup.checkedId()
        self.currentSelection.setText(self.selections[idx])

    def display_current_selection_by_gesture_command(self, idx):
        self.currentSelection.setText(self.selections[idx])

