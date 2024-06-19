# main.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, Qt
from SettingsUi import Ui_MainWindow1



class SetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow1()
        self.ui.setupUi(self)
        # self.lst = MainWindow()
        self.setWindowFlags(Qt.FramelessWindowHint)  # Hide default title bar
        self.ui.minimize_btn.clicked.connect(self.showMinimized)   
        self.ui.close_btn.clicked.connect(self.close)
        

