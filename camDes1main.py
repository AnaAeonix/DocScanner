from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from camDes1 import Ui_MainWindoww, VideoStream
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from datetime import datetime
import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
import cv2
# from sidebarNew_ui import Ui_MainWindow,VideoStream
import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtWidgets import QLabel, QScrollArea, QHBoxLayout, QWidget, QMenu, QFileDialog
from PyQt5.QtCore import QTimer,  Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import tempfile
import threading
from functools import partial
from PyQt5.QtGui import QImage, QPixmap, QFont

class MainWindow1(QMainWindow):
    def __init__(self):
        super(MainWindow1, self).__init__()
        self.ui = Ui_MainWindoww()
        self.ui.setupUi(self)
        self.captured_images=[]
        self.current_camera_index = 0  # Index of the currently selected camera
        self.video_stream = VideoStream(self.ui.cam_label,self.current_camera_index)  # Initialize video stream with default camera
        self.ui.shutter_btn.clicked.connect(self.capture_image) 
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.video_stream.display_camera_feed)
        self.timer.start(50)  # Update camera feed every 50 milliseconds

        self.cap = None
        self.populate_camera_dropdown() 
        # self.ui.shutter_btn.clicked.connect(self.capture_image) 
        
        
    def capture_image(self):
        ret, frame = self.video_stream.video.read()
        
        if ret:
            # Define the cropping geometry
            # crop_x = 987
            # crop_y = 448
            # crop_width = 1828
            # crop_height = 1333
            
            # # Ensure that the cropping rectangle does not exceed the dimensions of the frame
            # max_width = frame.shape[1]
            # max_height = frame.shape[0]
            
            # crop_x = min(crop_x, max_width)
            # crop_y = min(crop_y, max_height)
            # crop_width = min(crop_width, max_width - crop_x)
            # crop_height = min(crop_height, max_height - crop_y)
            
            # # Crop the frame
            # cropped_frame = frame[crop_y:crop_y+crop_height, crop_x:crop_x+crop_width]
            
            # if not cropped_frame.size == 0:  # Check if the cropped frame is not empty
                now = datetime.now()
                timestamp = now.strftime("%Y%m%d_%H%M%S")  # Format timestamp
                filename = f"captured_image_{timestamp}.jpg"
                
                
                # Create a temporary directory
                temp_dir = tempfile.mkdtemp()

                # Specify the filepath within the temporary directory
                filepath = os.path.join(temp_dir, filename)

                try:
                    cv2.imwrite(filepath, frame)  # Save the cropped image with timestamp
                    print("Image saved successfully.")

                    # Append the filepath to the captured images list
                    self.captured_images.append(filepath)

                    # Call display_captured_images to update the display
                    self.display_captured_images()

                except Exception as e:
                    print(f"Error saving image: {e}")
                    
                    

    def display_captured_images(self):
        # Clear existing images
        layout = self.ui.show_label.layout()
        if layout is not None:
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)

        # Ensure that show_label has a layout
        if layout is None:
            layout = QVBoxLayout()
            self.ui.show_label.setLayout(layout)

        # Display captured images if the list is not empty
        if self.captured_images:
            # Create a scroll area
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)
            scroll_area.setWidget(scroll_content)

            # Display captured images
            for index, image_path in enumerate(self.captured_images):
                label = QLabel()
                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaledToHeight(150, Qt.SmoothTransformation)  # Adjust height
                pixmap = pixmap.scaledToWidth(200, Qt.SmoothTransformation)  # Adjust width
                label.setPixmap(pixmap)
                scroll_layout.addWidget(label)

            # Add the scroll area to the main layout
            layout.addWidget(scroll_area)
        
    def image_clicked(self, index):
        print("Clicked on image:", index)

    def clear_displayed_images(self):
        # Clear existing images
        for i in reversed(range(self.ui.show_label.layout().count())):
            self.ui.show_label.layout().itemAt(i).widget().setParent(None)
            
    def populate_camera_dropdown(self):
        global available_cameras
        available_cameras = []
        for i in range(10):
            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            if cap.isOpened():
                backend_id = cap.get(cv2.CAP_PROP_BACKEND)
                camera_name = f"Camera {i} - Backend: {backend_id}"
                available_cameras.append((i, camera_name))
                del cap
        camera_names = [camera_name for _, camera_name in available_cameras]
        self.ui.drop_down.addItems(camera_names)
        self.ui.drop_down.currentIndexChanged.connect(lambda: self._handle_index_change())

    def _handle_index_change(self):
        self.current_camera_index = self.ui.drop_down.currentIndex()  # Access the current index
    # Do something with the new_index value
        self.video_stream.change_camera(self.current_camera_index) # Call your function with the index
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow1()
    window.show()
    sys.exit(app.exec())
