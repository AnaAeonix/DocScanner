import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from StackDesign import Ui_MainWindow  # replace 'your_ui_file' with the name of your UI file


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.adjust_btn.clicked.connect(self.clicked_adjust_btn)
        self.ui.color_btn.clicked.connect(self.clicked_color_btn)
        self.ui.rotate_btn.clicked.connect(self.clicked_rotate_btn)
        self.ui.back_btn.clicked.connect(self.clicked_back_btn)
        self.ui.back_btn_2.clicked.connect(self.clicked_back_btn)
        self.ui.back_btn_3.clicked.connect(self.clicked_back_btn)



    def clicked_adjust_btn(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def clicked_color_btn(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    
    def clicked_rotate_btn(self):
        self.ui.stackedWidget.setCurrentIndex(3)
    
    def clicked_back_btn(self):
        self.ui.stackedWidget.setCurrentIndex(0)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
