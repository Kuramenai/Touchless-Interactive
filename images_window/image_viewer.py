import sys
import settings
from os import listdir
from os.path import isfile, join
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QGridLayout, \
    QBoxLayout, QScrollArea, QApplication, QPushButton
from PyQt5.QtGui import QPixmap, QIcon

images_path = '../images_window/images/'


def is_image_file(filename):
    """Check if filename is an image file"""
    valid_img_extensions = \
        ['bmp', 'gif', 'jpg', 'jpeg', 'png', 'pbm', 'pgm', 'ppm', 'xbm', 'xpm']
    if len(filename.split('.')) == 2:
        filename_extension = filename.split('.')[1]
        if filename_extension in valid_img_extensions:
            return True
        else:
            return False
    else:
        return False


class MainViewer(QWidget):
    def __init__(self, first_image):
        super().__init__()
        self.width, self.height = 960, 540
        self.image_label = QLabel(self)
        self.pixmap = QPixmap()
        self.__init_ui(first_image)

    def __init_ui(self, first_image):
        self.setFixedSize(self.width, self.height)
        self.load_image(first_image)
        # self.show()

    def load_image(self, image_path):
        self.pixmap = QPixmap(image_path)
        self.pixmap = \
            self.pixmap.scaled(QSize(self.width, self.height), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.image_label.setPixmap(self.pixmap)


class ImagesThumbnails(QWidget):
    def __init__(self, album_path):
        super().__init__()
        self.__init_attributes(album_path)
        self.__init_ui()

    def __init_attributes(self, album_path):
        self.album_path = album_path
        self.album = [img for img in listdir(album_path) if isfile(join(album_path, img))]
        self.first_image_file_name = self.album[0] if self.album else None

    def __init_ui(self):

        layout = QGridLayout(self)
        layout.setHorizontalSpacing(20)

        column_index = 0

        for image_file_name in self.album:
            if is_image_file(image_file_name):

                image_label = QLabel()
                image_label.setAlignment(Qt.AlignCenter)

                image_path = self.album_path + image_file_name
                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaled(QSize(100, 100), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                image_label.setPixmap(pixmap)
                image_label.mousePressEvent = lambda e, index=column_index, file_path=image_path:\
                    self.on_thumbnail_click(e, index, file_path)

                layout.addWidget(image_label, 0, column_index, Qt.AlignCenter)

                column_index += 1


class ImageViewer(QMainWindow):
    def __init__(self, album_path):
        super().__init__()
        self.__init_attributes(album_path)
        self.__init_ui()

    def __init_attributes(self, album_path):
        self.album_path = album_path
        self.thumbnails = ImagesThumbnails(album_path)
        self.first_image_path = self.album_path + self.thumbnails.first_image_file_name
        self.viewer = MainViewer(self.first_image_path)
        self.index = 0
        self.image_viewer_widget = QWidget()

    def __init_ui(self):
        self.setFixedSize(QSize(1080, 720))

        layout = QGridLayout(self)
        layout.addWidget(self.viewer, 0, 0, Qt.AlignTop | Qt.AlignCenter)
        layout.addWidget(self.thumbnails, 1, 0, Qt.AlignBottom | Qt.AlignCenter)
        layout.setVerticalSpacing(30)

        self.image_viewer_widget.setLayout(layout)
        self.setCentralWidget(self.image_viewer_widget)

    def gesture_handler(self, gesture_id):
        if gesture_id == 30:  # Move Left:
            self.index = (self.index - 1) % len(self.thumbnails.album)
            self.viewer.load_image(self.album_path + self.thumbnails.album[self.index])
        elif gesture_id == 31:  # Move Right:
            self.index = (self.index + 1) % len(self.thumbnails.album)
            self.viewer.load_image(self.album_path + self.thumbnails.album[self.index])
        elif gesture_id == 1:  # Close Window
            settings.current_window = 0
            self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    # viewer = ImagesThumbnails(images_path)
    # viewer = MainViewer('./images/kamehameha3xkaioken.png')
    viewer = ImageViewer(images_path)
    app.exec_()
