from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import QSettings, Qt, QPoint, QStandardPaths
from SettingsUi import Ui_MainWindow1

class SetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow1()
        self.ui.setupUi(self)
        
        self.settings = QSettings("YourOrganization", "YourApplication")
        
        self.setWindowFlags(Qt.FramelessWindowHint)  # Hide default title bar
        self.ui.minimize_btn.clicked.connect(self.showMinimized)
        self.ui.close_btn.clicked.connect(self.close)
        self.ui.browse_btn.clicked.connect(self.select_folder)

        self.cached_string_retrieved = self.settings.value("AutoSaveFolder", "")
        print(self.cached_string_retrieved)
        
        self.AutoSaveFolder = ""
        if self.cached_string_retrieved:
            self.AutoSaveFolder = self.cached_string_retrieved
        else:
            self.AutoSaveFolder = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
        
        self.ui.storage_label.setText(self.AutoSaveFolder)
        self.old_pos = None

    def select_folder(self):
        # Open the folder dialog without creating a new QApplication instance
        folder_selected = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_selected:  # Ensure a folder was selected
            self.AutoSaveFolder = folder_selected
            self.ui.storage_label.setText(self.AutoSaveFolder)
            self.settings.setValue("AutoSaveFolder", self.AutoSaveFolder)
            # print(folder_selected)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None