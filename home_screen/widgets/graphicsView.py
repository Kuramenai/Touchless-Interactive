from PyQt5.QtCore import Qt
from PyQt5.QtGui  import QPixmap, QColor, QBrush, QRadialGradient
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView


class SingleImageGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.__aspectRatioMode = Qt.KeepAspectRatio
        self.__gradient_enabled = False
        self.__initVal()
    
    def __initVal(self):
        self._scene = QGraphicsScene(0, 0, 400, 400)
        self._picture = QPixmap()
        self._item = ''
        
    
    def addPictureToScene(self, filename:str):
        self._picture = QPixmap(filename)
        self._scene = QGraphicsScene(0, 0, 400, 400)
        self._item = self._scene.addPixmap(self._picture)
        self._item.setPos(100, 100)

        self.setScene(self._scene)
       
    
    def setAspectRatioMode(self, mode):
        self.__aspectRatioMode = mode
    
    def setGradientEnabled(self, f:bool):
        self.__gradient_enabled = f
    
    def __setGradient(self):
            center_point = self.mapToScene(self.rect().center())
            gradient = QRadialGradient(center_point, (self.height()+self.width())//2)
            # print(self.width(), center_point, self.geometry().center())
            gradient.setColorAt(0, QColor(255, 255, 255, 0))
            gradient.setColorAt(1, QColor(0, 0, 0, 255))
            brush = QBrush(gradient)
            self.setForegroundBrush(brush)

    def resizeEvent(self, e):
        if self._item:
            self.fitInView(self.sceneRect(), self.__aspectRatioMode)
            if self.__gradient_enabled:
                self.__setGradient()
        return super().resizeEvent(e)
