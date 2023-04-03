import sys
from os import listdir
from os.path import isfile, join
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton, QStyle, QLabel, \
    QSlider, QMainWindow
from PyQt5.QtCore import QSize, Qt

my_music_album = "../music_player/music_album/"


def is_music_file(filename):
    """Check if filename is a music file"""
    valid_music_extensions = \
        ['mp3', 'amv']
    filename_extension = filename[-3:]
    if filename_extension.lower() in valid_music_extensions:
        return True
    else:
        return False


class MediaPlayerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self):

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Prev, Play, Next Buttons
        self.play_btn = QPushButton()
        self.play_icon = self.style().standardIcon(QStyle.SP_MediaPlay)
        self.pause_icon = self.style().standardIcon(QStyle.SP_MediaPause)
        self.play_btn.setIcon(self.play_icon)

        self.next_btn = QPushButton()
        self.skip_forward_icon = self.style().standardIcon(QStyle.SP_MediaSkipForward)
        self.next_btn.setIcon(self.skip_forward_icon)

        self.prev_btn = QPushButton()
        self.skip_backward_icon = self.style().standardIcon(QStyle.SP_MediaSkipBackward)
        self.prev_btn.setIcon(self.skip_backward_icon)

        # Slider
        self.media_duration_slider = QSlider()
        self.media_duration_slider.setOrientation(Qt.Horizontal)

        # Volume Button and Slider
        self.volume_btn = QPushButton()
        self.volume_icon = self.style().standardIcon(QStyle.SP_MediaVolume)
        self.volume_btn.setIcon(self.volume_icon)

        self.volume_slider = QSlider()
        self.volume_slider.setOrientation(Qt.Horizontal)

        layout.addWidget(self.prev_btn, 0, 0, Qt.AlignCenter)
        layout.addWidget(self.play_btn, 0, 1, Qt.AlignCenter)
        layout.addWidget(self.next_btn, 0, 2, Qt.AlignCenter)
        layout.addWidget(self.media_duration_slider, 1, 0, Qt.AlignCenter)
        layout.addWidget(self.volume_btn, 0, 3, Qt.AlignCenter)
        layout.addWidget(self.volume_slider, 0, 4, Qt.AlignCenter)

        # self.setStyleSheet("QPushButton {border : 1px solid; border-radius: 15px; height : 30px; width : 30px}")


class MyPlaylistWidget(QWidget):
    def __init__(self, music_album_path):
        super().__init__()
        self.__init_attributes(music_album_path)
        self.__init_ui()

    def __init_attributes(self, music_album_path):
        self.music_album_path = music_album_path
        self.music_album = \
            [music for music in listdir(self.music_album_path) if isfile(join(self.music_album_path, music))]
        self.first_music_file_name = self.music_album[0] if self.music_album else None

    def __init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        playlist_title = QLabel(self)
        playlist_title.setText("My Playlist")

        layout.addWidget(playlist_title)

        for file in self.music_album:
            music_labels = []
            if is_music_file(file):
                music_label = QLabel(self)
                music_label.setText(file[:-4])
                music_labels.append(music_label)
                layout.addWidget(music_label)


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__init_attr()
        self.__init_ui()

    def __init_attr(self):
        self.mediaPlayerWidget = MediaPlayerWidget()
        self.playlistWidget = MyPlaylistWidget(my_music_album)
        self.musicTitle = QLabel(self)
        self.musicPlayerWidget = QWidget()

    def __init_ui(self):
        self.setWindowTitle("Pi Media Center")
        self.setFixedSize(QSize(1080, 720))

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.musicTitle.setText("rjeewr")

        layout.addWidget(self.playlistWidget, 0, 0, Qt.AlignCenter)
        layout.addWidget(self.mediaPlayerWidget, 1, 1, Qt.AlignCenter)
        layout.addWidget(self.musicTitle, 0, 1, Qt.AlignCenter | Qt.AlignBottom)

        self.musicPlayerWidget.setLayout(layout)
        self.setCentralWidget(self.musicPlayerWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    media_player = MusicPlayer()
    media_player.show()
    app.exec_()
