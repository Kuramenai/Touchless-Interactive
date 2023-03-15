import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, \
QLabel, QButtonGroup, QFrame
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPalette, QColor, QFont

from home_screen.homeMenu import HomeMenu


class HomeScreen(QMainWindow):
    def __init__(self):
        super(HomeScreen, self).__init__()
        self.__initVal()
        self.__initUI()
    
    def __initVal(self):
        self.__welcomeMessage = QLabel()
        self.__homeMenu = HomeMenu()
        self.__selections = ['PICTURES', 'MUSIC', 'VIDEOS']
        self.currentSelection = QLabel()
        self.btnGroup = self.__homeMenu.getButtonGroup()
        self.__myHomeWidget = QWidget()

    def __initUI(self):
        self.setWindowTitle("Pi Media Center")
        self.setFixedSize(QSize(1080, 720))
      
        #Welcome Message
        self.__welcomeMessage.setText("Welcome to Pi Media Center")
        self.__welcomeMessage.setFont(QFont("Goudy Old Style", 20))
        self.__welcomeMessage.setAlignment(Qt.AlignCenter|Qt.AlignTop)

        #Menu
        self.__loadMenu()
        self.__homeMenu.setFixedSize(500, 500)

        #Current Selection
        self.btnGroup.idToggled.connect(self.printCurrentSelection)
        self.currentSelection.setText(self.__selections[0])
        self.currentSelection.setFont(QFont("Consolas", 10))
        self.currentSelection.setAlignment(Qt.AlignCenter|Qt.AlignTop)

        #layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 50, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.__welcomeMessage)
        layout.addWidget(self.__homeMenu, alignment= Qt.AlignHCenter| Qt.AlignVCenter)
        layout.addWidget(self.currentSelection, stretch= -1000)
        layout.insertStretch( -1, 1 )

        self.__myHomeWidget.setLayout(layout)
        self.setStyleSheet('border: solid 2px')
        self.setCentralWidget(self.__myHomeWidget)
    
    def __loadMenu(self):

        icons_dir = 'home_screen/icons'
        self.__homeMenu.addPictures([f'{icons_dir}/pictures_r.png', f'{icons_dir}/music_r.png', \
                                     f'{icons_dir}/movies_r.png'])
        
        for btn in self.__homeMenu.getButtonGroup().buttons():
            btn.setFixedSize(40, 20)

        prevBtn = self.__homeMenu.getPrevBtn()
        prevBtn.setFixedSize(60, 60)
        nextBtn = self.__homeMenu.getNextBtn()
        nextBtn.setFixedSize(60, 60)
    
    def printCurrentSelection(self):
        idx = self.btnGroup.checkedId()
        self.currentSelection.setText(self.__selections[idx])
        
  


       