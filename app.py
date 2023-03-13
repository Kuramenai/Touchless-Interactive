from PyQt5.QtWidgets import QApplication
from home_screen import HomeMenu


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)

    home = HomeMenu()
    icons_dir = 'home_screen/icons'
    home.addPictures([f'{icons_dir}/pictures.png', f'{icons_dir}/music.png', f'{icons_dir}/videos.png'])
    for btn in home.getButtonGroup().buttons():
        btn.setFixedSize(40, 20)
    # prevBtn = home.getPrevBtn()
    # prevBtn.setFixedSize(60, 50)
    # nextBtn = home.getNextBtn()
    # nextBtn.setFixedSize(60, 50)
    home.show()
    app.exec_()