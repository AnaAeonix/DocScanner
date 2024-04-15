from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
# from camDesign import Ui_MainWindoww, VideoStream
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from datetime import datetime
import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton,QVBoxLayout,QCheckBox
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
import cv2
# from sidebarNew_ui import Ui_MainWindow,VideoStream
from ariNewUi import Ui_MainWindow,VideoStream
# from test import Ui_MainWindow,  VideoStream
import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtWidgets import QLabel, QScrollArea, QHBoxLayout, QWidget, QMenu, QFileDialog
from PyQt5.QtCore import QTimer,  Qt
from PyQt5.QtGui import QPixmap
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import tempfile
import threading
from functools import partial
from PyQt5.QtGui import QImage, QPixmap, QFont


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.showMaximized()
        global image_list
        
        
        
        image_list=[]
        
        self.current_camera_index = 0
        self.captured_images = []
        self.ui.edit_btn.clicked.connect(self.clicked_done_btn) 
        # self.video_stream = VideoStream(self.ui.cam_label,self.current_camera_index)  # Initialize video stream with default camera
        self.ui.shutter_btn.clicked.connect(self.capture_image) 
        # self.ui.done_btn.clicked.connect(self.clicked_done_btn) 
        self.ui.pdf_btn.clicked.connect(self.clicked_pdf)
        self.ui.cam_back.clicked.connect(self.returntocamera)
        # self.ui.adjust_btn.clicked.connect(self.)
        
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.video_stream.display_camera_feed)
        # self.timer.start(50)  # Update camera feed every 50 milliseconds

        self.cap = None
        self.populate_camera_dropdown() 
    
    def clicked_done_btn(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def clicked_pdf(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def returntocamera(self):
        self.ui.stackedWidget.setCurrentIndex(0)

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
        self.ui.cam_drop_down.addItems(camera_names)
        self.ui.cam_drop_down.currentIndexChanged.connect(lambda: self._handle_index_change())


    def _handle_index_change(self):
        self.current_camera_index = self.ui.cam_drop_down.currentIndex()  # Access the current index
    # Do something with the new_index value
        self.video_stream.change_camera(self.current_camera_index) # Call your function with the index
        
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
                    self.display_captured_images_main()

                except Exception as e:
                    print(f"Error saving image: {e}")

    def display_captured_images(self):
        # Clear existing images
        layout = self.ui.show_page.layout()
        if layout is not None:
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)

        # Ensure that show_label has a layout
        if layout is None:
            layout = QVBoxLayout()
            self.ui.show_page.setLayout(layout)

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


    def display_captured_images_main(self):
        global image_list
        image_list = self.captured_images
        print(image_list)
        # Clear existing images
        layout = self.ui.show_page.layout()
        if layout is not None:
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)

        # Clear the list of checkboxes
        self.all_checkboxes = []

        # Ensure that display_image_frame has a layout
        if layout is None:
            layout = QVBoxLayout()
            self.ui.show_page.setLayout(layout)

        # Display captured images if the list is not empty
        if image_list:
            # Check which images are already displayed
            displayed_images = [layout.itemAt(i).widget().findChild(QLabel) for i in range(layout.count())]

            # Create a scroll area
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)

            # Create a widget to contain the layout
            scroll_content = QWidget()
            scroll_layout = QVBoxLayout(scroll_content)

            # Create a "Select All" checkbox
            select_all_checkbox = QCheckBox("Select All")
            # select_all_checkbox.stateChanged.connect(self.select_all_images)
            scroll_layout.addWidget(select_all_checkbox)

            # Display captured images that are not already displayed
            for index, image_path in enumerate(image_list):
                if image_path not in displayed_images:
                    # Create a custom widget to display image, timestamp, and checkbox
                    image_widget = QWidget()
                    image_layout = QVBoxLayout(image_widget)

                    label = QLabel()
                    pixmap = QPixmap(image_path)
                    pixmap = pixmap.scaledToHeight(150, Qt.SmoothTransformation)  # Adjust height
                    pixmap = pixmap.scaledToWidth(200, Qt.SmoothTransformation)  # Adjust width
                    label.setPixmap(pixmap)

                    # Add timestamp label
                    timestamp_label = QLabel()
                    now = datetime.now()
                    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                    timestamp_label.setText(timestamp)

                    # Add checkbox
                    checkbox = QCheckBox("Select")
                    # checkbox.stateChanged.connect(lambda state, index=index: self.update_selected_images(state, index))
                    image_layout.addWidget(checkbox)

                    self.all_checkboxes.append(checkbox)

                    # Add widgets to the layout
                    image_layout.addWidget(label)
                    image_layout.addWidget(timestamp_label)

                    # Add the custom widget to the scroll layout
                    scroll_layout.addWidget(image_widget)

                    # Store a reference to the label corresponding to the image path
                    displayed_images.append(image_path)

                    # Connect the click event of each image to the image_clicked method
                    # label.mousePressEvent = lambda event, index=index: self.image_clicked(label, index)

            # Set the scroll content widget
            scroll_area.setWidget(scroll_content)

            # Add the scroll area to the main layout
            layout.addWidget(scroll_area)
            
    # def update_selected_images(self, state, index):
    #     if state == Qt.Checked:
    #         image_path = image_list[index]
    #         if image_path not in self.selected_images:
    #             self.selected_images.append(image_path)
    #     else:
    #         image_path = image_list[index]
    #         if image_path in self.selected_images:
    #             self.selected_images.remove(image_path)


    # def select_all_images(self, state):
    #     for checkbox in self.all_checkboxes:
    #         checkbox.setChecked(state == Qt.Checked)

    #         if state == Qt.Checked:
    #             image_path = image_list[self.all_checkboxes.index(checkbox)]
    #             if image_path not in self.selected_images:
    #                 self.selected_images.append(image_path)
    #         else:
    #             image_path = image_list[self.all_checkboxes.index(checkbox)]
    #             if image_path in self.selected_images:
    #                 self.selected_images.remove(image_path)

    # def get_selected_images(self):
    #     return self.selected_images


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
