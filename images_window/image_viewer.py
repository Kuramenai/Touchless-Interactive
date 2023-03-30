import sys
from os import listdir
from os.path import isfile, join
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QGridLayout, \
    QBoxLayout, QScrollArea, QApplication, QPushButton
from PyQt5.QtGui import QPixmap, QIcon

images_path = './images/'


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
    def __init__(self):
        super().__init__()
        self.width, self.height = 960, 540
        self.__init_ui()

    def __init_ui(self):
        self.setFixedSize(self.width, self.height)
        # self.show()

    def load_image(self, image_path):
        self.pixmap = QPixmap(image_path)
        self.pixmap = \
            self.pixmap.scaled(QSize(self.width, self.height), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.image_label = QLabel(self)
        self.image_label.setPixmap(self.pixmap)


class ImagesThumbnails(QWidget):
    def __init__(self, album_path, viewer_display):
        super().__init__()
        self.__init_attributes(album_path, viewer_display)
        self.__init_ui()

    def __init_attributes(self, album_path, viewer_display):
        self.album_path = album_path
        self.album = [img for img in listdir(album_path) if isfile(join(album_path, img))]
        self.first_image_file_name = self.album[0] if self.album else None
        self.viewer_display = viewer_display

    def __init_ui(self):

        layout = QGridLayout(self)
        layout.setHorizontalSpacing(30)

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

        self.viewer_display.load_image(images_path + self.first_image_file_name)

        self.setLayout(layout)
        # self.show()

    def on_thumbnail_click(self, event, index, file_path):
        self.viewer_display.load_image(file_path)
        print(file_path)


class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__init_attributes()
        self.__init_ui()

    def __init_attributes(self):
        self.viewer = MainViewer()
        self.thumbnails = ImagesThumbnails(images_path, self.viewer)
        self.image_viewer_widget = QWidget()

    def __init_ui(self):
        self.setFixedSize(QSize(1080, 720))

        layout = QGridLayout(self)
        layout.addWidget(self.viewer, 0, 0, Qt.AlignTop | Qt.AlignCenter)
        layout.addWidget(self.thumbnails, 1, 0, Qt.AlignBottom | Qt.AlignCenter)
        layout.setVerticalSpacing(500)

        self.image_viewer_widget.setLayout(layout)
        self.setCentralWidget(self.image_viewer_widget)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # viewer = ImagesThumbnails(images_path)
    viewer = ImageViewer()
    # viewer = MainViewer('./images/kamehameha3xkaioken.png')
    app.exec_()
