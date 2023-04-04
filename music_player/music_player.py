import sys
from os import listdir
from os.path import isfile, join
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton, QStyle, QLabel, \
    QSlider, QMainWindow
from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QAudioInput
from PyQt5.QtMultimediaWidgets import QVideoWidget


def is_music_file(filename):
    """Check if filename is an audio file"""
    valid_music_extensions = \
        ['wav', 'mp3', 'amv']
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
        layout.setSpacing(0)

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
        self.volume_slider.setRange(0, 100)

        layout.addWidget(self.prev_btn, 0, 0, Qt.AlignCenter)
        layout.addWidget(self.play_btn, 0, 1, Qt.AlignCenter)
        layout.addWidget(self.next_btn, 0, 2, Qt.AlignCenter)
        layout.addWidget(self.media_duration_slider, 1, 0, 1, 4, Qt.AlignCenter)
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
        self.first_audio_file_name = self.music_album[0] if self.music_album else None

    def __init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 475)
        layout.setSpacing(20)
        layout.insertStretch(-1, 1)

        playlist_title = QLabel(self)
        playlist_title.setText("My Playlist")
        playlist_title.setAlignment(Qt.AlignCenter)

        layout.addWidget(playlist_title)

        for file in self.music_album:
            music_labels = []
            if is_music_file(file):
                music_label = QLabel(self)
                music_label.setText(file[:-4])
                music_labels.append(music_label)
                layout.addWidget(music_label)


class MusicPlayer(QMainWindow):
    def __init__(self, music_album_path):
        super().__init__()
        self.__init_attr(music_album_path)
        self.__init_ui()
        self.load_audio_file(self.playing_now)

    def __init_attr(self, music_album_path):
        self.music_album_path = music_album_path

        self.playlistWidget = MyPlaylistWidget(self.music_album_path)
        self.musicIcon = QLabel(self)
        self.musicTitle = QLabel(self)
        self.mediaPlayerWidget = MediaPlayerWidget()
        self.mediaPlayer = QMediaPlayer()
        self.musicPlayerWidget = QWidget()

        self.index = 0
        self.playing_now = self.playlistWidget.first_audio_file_name
        self.audio_file_length = 0

    def __init_ui(self):
        self.setWindowTitle("Pi Media Center")
        self.setFixedSize(QSize(1080, 720))

        self.mediaPlayer.durationChanged.connect(self.set_slider_duration)
        self.mediaPlayer.positionChanged.connect(self.set_slider_position)
        self.mediaPlayer.stateChanged.connect(self.set_pause_icon)

        self.mediaPlayerWidget.volume_slider.setValue(self.mediaPlayer.volume())

        vboxLayout = QVBoxLayout()
        vboxLayout.setContentsMargins(30, 50, 30, 50)
        vboxLayout.setSpacing(10)

        self.musicTitle.setText(self.playing_now)

        pixmap = QPixmap('./global_icons/music_icon.png')
        pixmap = pixmap.scaled(QSize(426, 327), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.musicIcon.setPixmap(pixmap)

        vboxLayout.addWidget(self.musicIcon)
        vboxLayout.addWidget(self.musicTitle)
        vboxLayout.addWidget(self.mediaPlayerWidget)

        hboxLayout = QHBoxLayout(self)

        hboxLayout.addWidget(self.playlistWidget)
        hboxLayout.addLayout(vboxLayout)

        self.musicPlayerWidget.setLayout(hboxLayout)
        self.setCentralWidget(self.musicPlayerWidget)

    def load_audio_file(self, audio_file_name):
        full_file_path = self.music_album_path + audio_file_name
        audio_url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(audio_url)
        self.mediaPlayer.setMedia(content)

    def play_audio_file(self):
        if self.mediaPlayer.state() == QMediaPlayer.PausedState or \
                self.mediaPlayer.state() == QMediaPlayer.StoppedState:
            self.mediaPlayer.play()
            self.mediaPlayerWidget.play_btn.setIcon(self.mediaPlayerWidget.pause_icon)

    def pause_audio_file(self):
        # if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
        self.mediaPlayer.pause()
        self.mediaPlayerWidget.play_btn.setIcon(self.mediaPlayerWidget.play_icon)

    def set_pause_icon(self, state):
        print("Logging in")
        if state == 7:
            print("Logging in #2")
            self.mediaPlayerWidget.play_btn.setIcon(self.mediaPlayerWidget.play_icon)

    def reload_audio_file(self):
        self.playing_now = self.playlistWidget.music_album[self.index]
        self.load_audio_file(self.playing_now)
        self.pause_audio_file()
        self.musicTitle.setText(self.playing_now)

    def set_volume(self, gesture_id):
        current_volume = self.mediaPlayer.volume()
        if gesture_id == 33:
            self.mediaPlayer.setVolume(current_volume - 10)
            self.set_volume_slider_value(current_volume - 10)
        elif gesture_id == 32:
            self.mediaPlayer.setVolume(current_volume + 10)
            self.set_volume_slider_value(current_volume + 10)

    def set_slider_duration(self, duration):
        self.mediaPlayerWidget.media_duration_slider.setRange(0, duration)
        self.audio_file_length = duration

    def set_slider_position(self, position):
        self.mediaPlayerWidget.media_duration_slider.setValue(position)

    def set_volume_slider_value(self, volume):
        self.mediaPlayerWidget.volume_slider.setValue(volume)

    def gesture_handler(self, gesture_id):
        if gesture_id == 3:
            self.play_audio_file()
        elif gesture_id == 0:
            self.pause_audio_file()
        elif gesture_id == 30:
            self.index = (self.index - 1) % len(self.playlistWidget.music_album)
            self.reload_audio_file()
        elif gesture_id == 31:
            self.index = (self.index + 1) % len(self.playlistWidget.music_album)
            self.reload_audio_file()
        else:
            self.set_volume(gesture_id)


if __name__ == "__main__":
    my_music_album_path = './music_album/'
    app = QApplication(sys.argv)
    media_player = MusicPlayer(my_music_album_path)
    media_player.show()
    app.exec_()
