from PyQt5.QtCore import Qt, QPropertyAnimation, QObject
from PyQt5.QtGui  import QPixmap, QColor, QBrush, QRadialGradient
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsOpacityEffect, QGraphicsProxyWidget


class SingleImageGraphicsView(QGraphicsView):
    def __init__(self):
        super.__init__()
        self.__aspectRatioMode = Qt.KeepAspectRatio
        self.__initVal()
    
    def __initVal(self):
        self._scene = QGraphicsScene()
        self._picture = QPixmap()
        self._item = ''
    
    def addPictureToScene(self, filename:str):
        self._picture = QPixmap(filename)
        self._item = self._scene.addPixmap(self._picture)

        self.setScene(self._scene)
        self.fitInView(self._item, self.__aspectRatioMode)
    
    def setAspectRatioMode(self, mode):
        self.__aspectRatioMode = mode
    
