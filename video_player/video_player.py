import sys
import settings
from os import listdir
from os.path import isfile, join
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton, QStyle, QLabel, \
    QSlider, QMainWindow
from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.QtGui import QPixmap, QMovie, QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QAudioInput
from PyQt5.QtMultimediaWidgets import QVideoWidget

from styles import music_player_stylesheet


def is_video_file(filename):
    """Check if filename is an audio file"""
    video_extensions = \
        ['mp4', 'avi', 'h264', 'mpg', 'mov', 'wmv', 'rm', 'swf', 'webm', 'mkv', 'flv', 'vob', '3gp', 'asf']
    filename_extension = filename[-3:]
    filename_extension_4char = filename[-4:]
    if filename_extension.lower() in video_extensions or filename_extension_4char.lower in video_extensions:
        return True
    else:
        return False


class MediaPlayerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__init_ui()

    def __init_ui(self):

        self.setFixedWidth(500)

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)
        layout.setSpacing(0)

        self.videoWidget = QVideoWidget()
        self.setFixedSize(QSize(480, 480))

        # Label for name of audio file
        self.videoFileName = QLabel()

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

        # Playing Time
        self.media_played_time = QLabel()
        self.media_played_time.setText("00:00")
        self.media_total_duration = QLabel()
        self.media_total_duration.setText("00:00")

        # Slider
        self.media_duration_slider = QSlider()
        self.media_duration_slider.setOrientation(Qt.Horizontal)
        self.media_duration_slider.setFixedSize(QSize(350, 15))

        # Volume Button and Slider
        self.volume_btn = QPushButton()
        self.volume_icon = self.style().standardIcon(QStyle.SP_MediaVolume)
        self.volume_btn.setIcon(self.volume_icon)
        self.volume_btn.setStyleSheet("""background-color: none""")

        self.volume_slider = QSlider()
        self.volume_slider.setOrientation(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)

        # Adding widgets to  layout
        layout.addWidget(self.videoWidget, 0, 1, 6, 17, Qt.AlignCenter)
        layout.addWidget(self.videoFileName, 10, 1, 1, 17, Qt.AlignCenter)
        layout.addWidget(self.prev_btn, 20, 5, 1, 1, Qt.AlignCenter)
        layout.addWidget(self.play_btn, 20, 9, 1, 1, Qt.AlignCenter)
        layout.addWidget(self.next_btn, 20, 13, 1, 1, Qt.AlignCenter)
        layout.addWidget(self.volume_btn, 20, 15, 1, 1, Qt.AlignRight)
        layout.addWidget(self.volume_slider, 20, 17, 1, 1, Qt.AlignRight)
        layout.addWidget(self.media_played_time, 21, 2, 1, 1, Qt.AlignLeft)
        layout.addWidget(self.media_total_duration, 21, 17, 1, 1, Qt.AlignLeft)
        layout.addWidget(self.media_duration_slider, 21, 3, 1, 14, Qt.AlignCenter)

        self.setStyleSheet(music_player_stylesheet.style)


class MyPlaylistWidget(QWidget):
    def __init__(self, video_album_path):
        super().__init__()
        self.__init_attributes(video_album_path)
        self.__init_ui()

    def __init_attributes(self, video_album_path):
        self.video_album_path = video_album_path
        self.video_album = \
            [music for music in listdir(self.video_album_path) if isfile(join(self.video_album_path, music))]
        self.first_video_file_name = self.video_album[0] if self.video_album else None
        self.video_labels = []

    def __init_ui(self):

        self.setStyleSheet("""  background-color: white; 
                                border-radius : 5px;
                                padding : 3px;
                                """)
        self.setFixedWidth(425)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 475)
        layout.setSpacing(20)
        layout.insertStretch(-1, 1)
        playlist_title = QLabel()
        playlist_title.setText("My Videos Playlist")
        playlist_title.setStyleSheet(""" background-color : #3167D1; color : white; font-weight : bold""")
        playlist_title.setFont(QFont("Goudy Old Style", 13))
        playlist_title.setAlignment(Qt.AlignCenter)

        layout.addWidget(playlist_title)

        for file in self.video_album:
            if is_video_file(file):
                video_label = QLabel()
                video_label.setText(file[:-4])
                self.video_labels.append(video_label)
                layout.addWidget(video_label)


class VideoPlayer(QMainWindow):
    def __init__(self, video_album_path):
        super().__init__()
        self.__init_attr(video_album_path)
        self.__init_ui()
        self.load_video_file(self.playing_now)

    def __init_attr(self, video_album_path):
        self.video_album_path = video_album_path

        self.playlistWidget = MyPlaylistWidget(self.video_album_path)
        self.mediaPlayerWidget = MediaPlayerWidget()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoPlayerWidget = QWidget()

        self.index = 0
        self.playing_now = self.playlistWidget.first_video_file_name
        self.video_file_length = 0

    def __init_ui(self):
        self.setWindowTitle("Pi Media Center")
        self.setFixedSize(QSize(1080, 720))

        # Highlighting playing now video label
        self.highlight_playing_now_label()

        # State management of media player
        self.mediaPlayer.setVideoOutput(self.mediaPlayerWidget.videoWidget)
        self.mediaPlayer.durationChanged.connect(self.set_slider_duration)
        self.mediaPlayer.positionChanged.connect(self.set_slider_position)
        self.mediaPlayer.stateChanged.connect(self.set_pause_icon)

        # Volume Control
        self.mediaPlayer.setVolume(50)
        self.mediaPlayerWidget.volume_slider.setValue(self.mediaPlayer.volume())

        # Displaying name of audio which is being played
        self.mediaPlayerWidget.videoFileName.setText(self.playing_now)
        self.mediaPlayerWidget.videoFileName.setAlignment(Qt.AlignCenter)

        # Setting up layouts
        hboxLayout = QHBoxLayout(self)
        hboxLayout.addWidget(self.playlistWidget)
        hboxLayout.addWidget(self.mediaPlayerWidget)

        self.setStyleSheet("""background-color: lightgray;""")

        self.videoPlayerWidget.setLayout(hboxLayout)
        self.setCentralWidget(self.videoPlayerWidget)

    def load_video_file(self, audio_file_name):
        full_file_path = self.video_album_path + audio_file_name
        video_url = QUrl.fromLocalFile(full_file_path)
        content = QMediaContent(video_url)
        self.mediaPlayer.setMedia(content)

    def reload_audio_file(self):
        self.playing_now = self.playlistWidget.video_album[self.index]
        self.load_video_file(self.playing_now)
        self.pause_video_file()
        self.mediaPlayerWidget.videoFileName.setText(self.playing_now)

    def play_video_file(self):
        if self.mediaPlayer.state() == QMediaPlayer.PausedState or \
                self.mediaPlayer.state() == QMediaPlayer.StoppedState:
            self.mediaPlayer.play()
            self.mediaPlayerWidget.play_btn.setIcon(self.mediaPlayerWidget.pause_icon)

    def pause_video_file(self):
        self.mediaPlayer.pause()
        self.mediaPlayerWidget.play_btn.setIcon(self.mediaPlayerWidget.play_icon)

    def set_pause_icon(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.StoppedState:
            self.mediaPlayerWidget.play_btn.setIcon(self.mediaPlayerWidget.play_icon)

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
        self.video_file_length = duration
        duration_minutes = duration // 60_000
        duration_seconds = ((duration % 60_000) // 1000)
        self.mediaPlayerWidget.media_total_duration.setText(f"{duration_minutes:02}:{duration_seconds:02}")

    def set_slider_position(self, position):
        self.mediaPlayerWidget.media_duration_slider.setValue(position)
        duration_minutes = position // 60_000
        duration_seconds = ((position % 60_000) // 1000)
        self.mediaPlayerWidget.media_played_time.setText(f"{duration_minutes:02}:{duration_seconds:02}")

    def set_volume_slider_value(self, volume):
        self.mediaPlayerWidget.volume_slider.setValue(volume)

    def remove_highlight(self):
        label = self.playlistWidget.video_labels[self.index]
        label.setStyleSheet(""" """)

    def highlight_playing_now_label(self):
        label = self.playlistWidget.video_labels[self.index]
        label.setStyleSheet(""" background-color : azure ; border : 2px solid blue;""")

    def gesture_handler(self, gesture_id):
        if gesture_id == 3:
            self.play_video_file()
        elif gesture_id == 0:
            self.pause_video_file()
        elif gesture_id == 30:
            self.remove_highlight()
            self.index = (self.index - 1) % len(self.playlistWidget.video_album)
            self.highlight_playing_now_label()
            self.reload_audio_file()
        elif gesture_id == 31:
            self.remove_highlight()
            self.index = (self.index + 1) % len(self.playlistWidget.video_album)
            self.reload_audio_file()
            self.highlight_playing_now_label()
        elif gesture_id == 1:  # Close Window
            settings.current_window = 0
            self.close()
        elif gesture_id == 33 or gesture_id == 34:
            self.set_volume(gesture_id)


if __name__ == "__main__":
    music_player_stylesheet.initialize_style()
    my_video_album_path = './videos/'
    app = QApplication(sys.argv)
    media_player = VideoPlayer(my_video_album_path)
    media_player.show()
    app.exec_()
