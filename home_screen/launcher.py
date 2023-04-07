import sys
import settings
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, \
     QLabel, QButtonGroup, QFrame
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPalette, QColor, QFont

from home_screen.homeMenu import HomeMenu
from images_window.image_viewer import ImageViewer
from music_player.music_player import MusicPlayer
from video_player.video_player import VideoPlayer

album_path = './images_window/images/'
audio_album_path = './music_player/music_album/'
video_album_path = './video_player/videos/'


class HomeScreen(QMainWindow):
    def __init__(self):
        super(HomeScreen, self).__init__()
        self.__init_attr()
        self.__init_ui()
    
    def __init_attr(self):
        self.__welcomeMessage = QLabel()
        self.homeMenu = HomeMenu()
        self.selections = ['IMAGES', 'MUSIC', 'VIDEOS']
        self.currentSelection = QLabel()
        self.userDetectedGesture = QLabel()
        self.btnGroup = self.homeMenu.getButtonGroup()
        self.__myHomeWidget = QWidget()
        self.image_viewer = ImageViewer(album_path)
        self.music_player = MusicPlayer(audio_album_path)
        self.video_player = VideoPlayer(video_album_path)

    def __init_ui(self):
        self.setWindowTitle("Pi Media Center")
        self.setFixedSize(QSize(1080, 720))

        # Welcome Message
        self.__welcomeMessage.setText("Welcome to Pi Media Center")
        self.__welcomeMessage.setFont(QFont("Goudy Old Style", 20))
        self.__welcomeMessage.setAlignment(Qt.AlignCenter | Qt.AlignTop)

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
        self.homeMenu.addPictures([f'{icons_dir}/pictures_r.png', f'{icons_dir}/music_r.png', f'{icons_dir}/movies_r.png'])
        
        for btn in self.homeMenu.getButtonGroup().buttons():
            btn.setFixedSize(40, 20)

        prev_btn = self.homeMenu.getPrevBtn()
        prev_btn.setFixedSize(60, 60)
        next_btn = self.homeMenu.getNextBtn()
        next_btn.setFixedSize(60, 60)
    
    def print_current_selection(self):
        idx = self.btnGroup.checkedId()
        self.currentSelection.setText(self.selections[idx])

    def gesture_handler(self, gesture_id):
        btnGroup = self.homeMenu.getButtonGroup()
        idx = btnGroup.checkedId()
        if gesture_id == 3:
            if idx == 0:
                settings.current_window = 1
                self.image_viewer.setVisible(True)
            elif idx == 1:
                settings.current_window = 2
                self.music_player.setVisible(True)
            elif idx == 2:
                settings.current_window = 3
                self.video_player.setVisible(True)

        elif gesture_id == 30:
            new_idx = (idx - 1) % 3
            self.homeMenu.show_image_of_index_by_gesture_command(new_idx)
        elif gesture_id == 31:
            new_idx = (idx + 1) % 3
            self.homeMenu.show_image_of_index_by_gesture_command(new_idx)

    def display_current_selection_by_gesture_command(self, idx):
        self.currentSelection.setText(self.selections[idx])
