from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QButtonGroup, QSizePolicy
from widgets.graphicsView import SingleImageGraphicsView
from widgets.svgButton import SvgButton

class HomeMenu(QWidget):
    def __init__(self):
        super.__init__()
        self.__initVal()
        self.__initUi()
    
    def __initVal(self):
        self.__btn = []
        self.__filenames = []
        self.__interval = 5000

    def __initUi(self):
        self.__view = SingleImageGraphicsView()
        self.__view.setAspectRatioMode(Qt.KeepAspectRatioByExpanding)
        self.__view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__view.setStyleSheet('QGraphicsView { background : transparant; border: none; }')
        self.__viewInstallEventFilter(self)

        # Previous and Next Buttons
        self.__btnGroup = QButtonGroup()
        self.__btnGroup.buttonlicked.connect(self.showImageOfIdx)

        self.__btnWidget = QWidget()

        self.__prevBtn = SvgButton()
        self.__prevBtn.setIcon('icons/left.svg')
        self.__prevBtn.setFixedSize(30, 50)
        self.__prevBtn.clicked.connect(self.__prev)
        self.__prevBtn.setEnabled(False)

        self.__nextBtn = SvgButton()
        self.__nextBtn.setIcon('icons/right.svg')
        self.__nextBtn.setFixedSize(30, 50)
        self.__nextBtn.clicked.connect(self.__nextClicked)

        lay = QHBoxLayout()
        lay.addWidget(self.__prevBtn, alignment = Qt.AlignLeft)
        lay.addWidget(self.__nextBtn, alignment = Qt.AlignRight)

        self.__navWidget = QWidget()
        self.__navWidget.setLayout(lay)

        lay = QGridLayout()
        lay.addWidget(self.__view, 0, 0, 3, 1)
        lay.addWidget(self.__navWidget, 0, 0, 3, 1)
        lay.addWidget(self.__btnWidget, 2, 0, 1, 1, Qt.AlignCenter)
        self.setLayout(lay)

        self.__timer = QTimer(self)
        self.__timer.setInterval(self.__interval)
        self.__timer.timeout.connect(self.__nextByTimer)
        self.timer.start()
    
    def __showImageOfIndex(self, btn):
        idx = self.__btnGroup.id(btn)
        self.__view.addPictureToScene(self.__filenames[idx])
        self.__prevNextBtnToggled(idx)
        self.__timer.start()
    
    def __prev(self):
        if len(self.__filenames) > 0:
            idx = max(0, self.__btnGroup.checkedId() - 1)
            self.__updateViewAndBtnBasedOnIdx(idx)
            self.__timer.start()
    
    def __nextByTimer(self):
        if len(self.__filenames) > 0:
            self.__next()
    
    def __next(self):
        idx = (self.__btnGroup.checkedId() + 1) % len(self.__btnGroup.buttons())
        self.__updateViewAndBtnBasedOnIdx(idx)
    
    def __updateViewAndBtnBasedOnIdx(self, idx):
        self.__btnGroup.button(idx).setChecked(True)
        self.__view.addPictureToScene(self.__filenames[idx])
        self.prevNextBtnToggled(idx)
    
    def __prevNextBtnToggled(self, idx):
        self.__prevBtn.setEnabled(idx != 0)
        self.__nextBtn.setEnabled(idx != len(self.__btnGroup.buttons()) - 1)
    
    def setInterval(self, milliseconds : int):
        self.__timer.setInterval(milliseconds)
    
    def addPictures(self, filenames : list):
        pass

    def setNavigationButtonVisible(self, f: bool):
        self.__navWidget.setVisible(f)
    
    def setBottomButtonVisible(self, f: bool):
        self.__btnWidget.setVisible(f)

    def setTimerEnabled(self, f: bool):
        if f :
            self.__timer.start()
        else:
            self.__timer.stop()
    
    def setGradientEnabled(self, f: bool):
        pass

    def getButtonGroup(self):
        return self.__btnGroup
    
    def getBtnWidget(self):
        return self.__btnWidget
    
    def getPrevBtn(self):
        self.__prevBtn

    def getNextBtn(self):
        self.__nextBtn




