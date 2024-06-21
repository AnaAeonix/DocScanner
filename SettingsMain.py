# main.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog
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
        self.ui.browse_btn.clicked.connect(self.select_folder)
        self.AutoSaveFolder = "C:/Users/skuma/OneDrive/Desktop"
        self.ui.storage_label.setText(self.AutoSaveFolder)
        


    def select_folder(self):
        # Open the folder dialog without creating a new QApplication instance
        folder_selected = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_selected:  # Ensure a folder was selected
            self.AutoSaveFolder = folder_selected
            self.ui.storage_label.setText(self.AutoSaveFolder)
            print(folder_selected)

    