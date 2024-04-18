from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
# from camDesign import Ui_MainWindoww, VideoStream
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from datetime import datetime
import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QVBoxLayout, QCheckBox
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
import cv2
# from sidebarNew_ui import Ui_MainWindow,VideoStream
from ariNewUi import Ui_MainWindow, VideoStream
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
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import cv2
import os
import tempfile
from datetime import datetime
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QCheckBox
from datetime import datetime
import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtCore import pyqtSlot, QFile, QTextStream
import cv2
from PyQt5.QtWidgets import QLabel, QScrollArea, QHBoxLayout, QWidget, QMenu, QFileDialog
from PyQt5.QtCore import QTimer,  Qt
from PyQt5.QtGui import QPixmap
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QObject
import tempfile
import threading
from functools import partial
from PyQt5.QtGui import QImage, QPixmap, QFont
# from camDes1main import MainWindow1
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QInputDialog, QComboBox
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageEnhance, ImageOps
import cv2
import numpy as np
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.showMaximized()
        global image_list

        self.image_click_counter = {}

        image_list = []
        self.crop_size=[]
        self.latestImage = []

        # Create a dictionary to store references to labels corresponding to image paths
        self.image_labels = {}
        self.image = None  # Track the currently displayed image
        self.imageIndex = None
        self.rotation_state = 0  # Initial rotation state
        self.current_displayed_image = None  # Track the currently displayed image

        self.selected_images = []  # Store selected images
        self.all_checkboxes = []   # Store references to all checkboxes
        self.current_camera_index = 0
        self.captured_images = []
        self.ui.edit_btn.clicked.connect(self.image_double_clicked)
        # Initialize video stream with default camera
        self.video_stream = VideoStream(
            self.ui.cam_label, self.current_camera_index)
        self.ui.shutter_btn.clicked.connect(self.capture_image)
        self.ui.rotateleft_btn.clicked.connect(self.rotate_image_left)
        self.ui.rotateright_btn.clicked.connect(self.rotate_image_right)
        # self.ui.done_btn.clicked.connect(self.clicked_done_btn)
        self.ui.pdf_btn.clicked.connect(self.make_pdf)
        self.ui.cam_back.clicked.connect(self.returntocamera)
        self.ui.adjust_btn.clicked.connect(self.clicked_adjust_btn)
        self.ui.color_btn.clicked.connect(self.clicked_color_btn)
        self.ui.rotate_btn.clicked.connect(self.clicked_rotate_btn)
        self.ui.enhance_btn.clicked.connect(self.AutoEnhance)
        self.ui.crop_btn.clicked.connect(self.crop_image)
        self.ui.settings_btn.clicked.connect(self.crop_image_settings)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.video_stream.display_camera_feed)
        self.timer.start(50)  # Update camera feed every 50 milliseconds

        self.cap = None
        self.populate_camera_dropdown()

    def clicked_done_btn(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def clicked_pdf(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def returntocamera(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def clicked_adjust_btn(self):
        self.ui.edit_stack.setCurrentIndex(0)

    def clicked_color_btn(self):
        self.ui.edit_stack.setCurrentIndex(1)

    def clicked_rotate_btn(self):
        self.ui.edit_stack.setCurrentIndex(2)

    def make_pdf(self):
        # Ask the user for the save path
        save_path, _ = QFileDialog.getSaveFileName(
            None, "Save PDF", "", "PDF Files (*.pdf)")
        if save_path:
            if self.selected_images:
                pdf_canvas = canvas.Canvas(save_path, pagesize=letter)
                for image_path in self.selected_images:
                    image = cv2.imread(image_path)
                    if image is not None:
                        height, width, _ = image.shape
                        # Set the PDF page size same as image size
                        pdf_canvas.setPageSize((width, height))
                        # Place image on PDF
                        pdf_canvas.drawImage(image_path, 0, 0, width, height)
                        pdf_canvas.showPage()  # End current page
                pdf_canvas.save()
                print("PDF saved successfully.")
                # self.clear_displayed_images()
                # self.captured_images.clear()
            else:
                print("No images to save.")
        else:
            print("Save operation cancelled by the user.")

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
        self.ui.cam_drop_down.currentIndexChanged.connect(
            lambda: self._handle_index_change())

    def _handle_index_change(self):
        # Access the current index
        self.current_camera_index = self.ui.cam_drop_down.currentIndex()
    # Do something with the new_index value
        # Call your function with the index
        self.video_stream.change_camera(self.current_camera_index)

    def rotate_image_right(self):
        if self.read() is not None:
            self.rotation_state -= 90
            if self.rotation_state < 0:
                self.rotation_state = 270
            rotated_image = self.read().copy()
            for _ in range(abs(self.rotation_state // 90)):
                rotated_image = cv2.rotate(
                    rotated_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.latestImage.append(rotated_image)
            # self.image = rotated_image
            self.write(rotated_image)
            self.load_image()

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
            image_resolution = frame.shape[:2]  # Get only the rows and columns

            print("Image resolution:", image_resolution)

            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")  # Format timestamp
            filename = f"captured_image_{timestamp}.jpg"

            # Create a temporary directory
            temp_dir = tempfile.mkdtemp()

            # Specify the filepath within the temporary directory
            filepath = os.path.join(temp_dir, filename)

            try:
                # Save the cropped image with timestamp
                cv2.imwrite(filepath, frame)
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
                pixmap = pixmap.scaledToHeight(
                    150, Qt.SmoothTransformation)  # Adjust height
                pixmap = pixmap.scaledToWidth(
                    200, Qt.SmoothTransformation)  # Adjust width
                label.setPixmap(pixmap)
                scroll_layout.addWidget(label)

            # Add the scroll area to the main layout
            layout.addWidget(scroll_area)

    # def display_captured_images_main(self):
    #     global image_list
    #     image_list = self.captured_images
    #     print(image_list)
    #     # Clear existing images
    #     layout = self.ui.additional_label.layout()
    #     # Assuming self.ui.show_page is a QWidget
    #     if layout is not None:
    #         for i in reversed(range(layout.count())):
    #             layout.itemAt(i).widget().setParent(None)

    #     # Clear the list of checkboxes
    #     self.all_checkboxes = []

    #     # Ensure that display_image_frame has a layout
    #     if layout is None:
    #         layout = QVBoxLayout()
    #         self.ui.additional_label.setLayout(layout)

    #     # Display captured images if the list is not empty
    #     if image_list:
    #         # Check which images are already displayed
    #         displayed_images = [layout.itemAt(i).widget().findChild(QLabel) for i in range(layout.count())]

    #         # Create a scroll area
    #         scroll_area = QScrollArea()
    #         scroll_area.setWidgetResizable(True)

    #         # Create a widget to contain the layout
    #         scroll_content = QWidget()
    #         scroll_layout = QVBoxLayout(scroll_content)

    #         # Create a "Select All" checkbox
    #         select_all_checkbox = QCheckBox("Select All")
    #         select_all_checkbox.stateChanged.connect(self.select_all_images)
    #         scroll_layout.addWidget(select_all_checkbox)

    #         # Display captured images that are not already displayed
    #         for index, image_path in enumerate(image_list):
    #             if image_path not in displayed_images:
    #                 # Create a custom widget to display image, timestamp, and checkbox
    #                 image_widget = QWidget()
    #                 image_layout = QVBoxLayout(image_widget)

    #                 label = QLabel()
    #                 pixmap = QPixmap(image_path)
    #                 pixmap = pixmap.scaledToHeight(150, Qt.SmoothTransformation)  # Adjust height
    #                 pixmap = pixmap.scaledToWidth(200, Qt.SmoothTransformation)  # Adjust width
    #                 label.setPixmap(pixmap)

    #                 # Add timestamp label
    #                 timestamp_label = QLabel()
    #                 now = datetime.now()
    #                 timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    #                 timestamp_label.setText(timestamp)

    #                 # Add checkbox
    #                 checkbox = QCheckBox("Select")
    #                 checkbox.stateChanged.connect(lambda state, index=index: self.update_selected_images(state, index))
    #                 image_layout.addWidget(checkbox)

    #                 self.all_checkboxes.append(checkbox)

    #                 # Add widgets to the layout
    #                 image_layout.addWidget(label)
    #                 image_layout.addWidget(timestamp_label)

    #                 # Add the custom widget to the scroll layout
    #                 scroll_layout.addWidget(image_widget)

    #                 # Store a reference to the label corresponding to the image path
    #                 displayed_images.append(image_path)

    #                 # Connect the click event of each image to the image_clicked method
    #                 label.mousePressEvent = lambda event, index=index: self.image_clicked(label, index)

    #         # Set the scroll content widget
    #         scroll_area.setWidget(scroll_content)

    #         # Add the scroll area to the main layout
    #         layout.addWidget(scroll_area)

    # def display_captured_images_main(self):
    #     global image_list
    #     image_list = self.captured_images
    #     print(image_list)

    #     # Clear existing images
    #     layout = self.ui.additional_label.layout()
    #     if layout is not None:
    #         for i in reversed(range(layout.count())):
    #             layout.itemAt(i).widget().setParent(None)

    #     # Clear the list of checkboxes
    #     self.all_checkboxes = []

    #     # Create a scroll area to contain the images
    #     scroll_area = QtWidgets.QScrollArea()
    #     scroll_area.setWidgetResizable(True)
    #     scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)  # Remove frame shape

    #     # Create a widget to contain the layout of the images
    #     scroll_content = QtWidgets.QWidget()
    #     scroll_layout = QtWidgets.QVBoxLayout(scroll_content)

    #     # Ensure that additional_label has a layout
    #     if layout is None:
    #         layout = QtWidgets.QVBoxLayout()
    #         self.ui.additional_label.setLayout(layout)

    #     # Display captured images if the list is not empty
    #     if image_list:
    #         # Display captured images
    #         for index, image_path in enumerate(image_list):
    #             # Create QLabel for image
    #             label = QtWidgets.QLabel()
    #             pixmap = QtGui.QPixmap(image_path)
    #             # Scale image to fit additional_label
    #             pixmap = pixmap.scaledToHeight(150, QtCore.Qt.SmoothTransformation)
    #             pixmap = pixmap.scaledToWidth(200, QtCore.Qt.SmoothTransformation)
    #             label.setPixmap(pixmap)

    #             # Add QLabel to the layout
    #             scroll_layout.addWidget(label, alignment=QtCore.Qt.AlignTop)

    #     # Set the scroll content widget
    #     scroll_area.setWidget(scroll_content)

    #     # Add the scroll area to additional_label
    #     layout.addWidget(scroll_area)

    def rotate_image_left(self):
        if self.read() is not None:
            if self.rotation_state == 270:
                self.rotation_state = 0
            else:
                self.rotation_state += 90
            rotated_image = self.read().copy()
            for _ in range(self.rotation_state // 90):
                rotated_image = cv2.rotate(
                    rotated_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.latestImage.append(rotated_image)
            # self.image = rotated_image
            self.write(rotated_image)
            self.load_image()
    # def display_captured_images_main(self):
    #     global image_list
    #     image_list = self.captured_images
    #     print(image_list)
    #     self.all_checkboxes = []
    #     # Clear existing images and checkboxes
    #     layout = self.ui.additional_label.layout()
    #     if layout is not None:
    #         for i in reversed(range(layout.count())):
    #             widget = layout.itemAt(i).widget()
    #             if isinstance(widget, QtWidgets.QWidget):
    #                 widget.setParent(None)

    #     # Ensure that additional_label has a layout
    #     if layout is None:
    #         layout = QtWidgets.QVBoxLayout()
    #         self.ui.additional_label.setLayout(layout)

    #     # Create a scroll area to contain the images and checkboxes

    #     # Add "Select All" checkbox

    #     # Display captured images if the list is not empty
    #     if image_list:
    #         displayed_images = [layout.itemAt(i).widget().findChild(QLabel) for i in range(layout.count())]
    #         select_all_checkbox = QtWidgets.QCheckBox("Select All")
    #         select_all_checkbox.stateChanged.connect(self.select_all_images)
    #         scroll_area = QtWidgets.QScrollArea()
    #         scroll_area.setWidgetResizable(True)
    #         scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)  # Remove frame shape

    #         # Create a widget to contain the layout of the images and checkboxes
    #         scroll_content = QtWidgets.QWidget()
    #         scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
    #         scroll_layout.addWidget(select_all_checkbox)
    #         # Create a horizontal layout for each image and checkbox
    #         for index, image_path in enumerate(image_list):
    #             if image_path not in displayed_images:
    #                 # Create a widget to contain the image and checkbox
    #                 image_widget = QtWidgets.QWidget()

    #                 # Create QLabel for image
    #                 label = QtWidgets.QLabel()
    #                 pixmap = QtGui.QPixmap(image_path)
    #                 # Scale image to fit additional_label
    #                 pixmap = pixmap.scaledToHeight(150, QtCore.Qt.SmoothTransformation)
    #                 pixmap = pixmap.scaledToWidth(150, QtCore.Qt.SmoothTransformation)
    #                 label.setPixmap(pixmap)

    #                 # Create checkbox
    #                 checkbox = QtWidgets.QCheckBox("Select")
    #                 checkbox.stateChanged.connect(lambda state, index=index: self.update_selected_images(state, index))
    #                 self.all_checkboxes.append(checkbox)
    #                 label.mouseDoubleClickEvent = lambda event, index=index: self.image_double_clicked(image_path)

    #                 # Create layout for image and checkbox
    #                 layout_image_checkbox = QtWidgets.QVBoxLayout()
    #                 layout_image_checkbox.addWidget(checkbox)
    #                 layout_image_checkbox.addWidget(label)
    #                 image_widget.setLayout(layout_image_checkbox)

    #                 # Add image widget to the scroll layout
    #                 scroll_layout.addWidget(image_widget)

    #     # Set the scroll content widget
    #     scroll_area.setWidget(scroll_content)

    #     # Add the scroll area to additional_label
    #     layout.addWidget(scroll_area)

    def display_captured_images_main(self):
        global image_list
        image_list = self.captured_images
        print(image_list)
        self.all_checkboxes = []
        # Clear existing images and checkboxes
        layout = self.ui.additional_label.layout()
        if layout is not None:
            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i).widget()
                if isinstance(widget, QtWidgets.QWidget):
                    widget.setParent(None)

        # Ensure that additional_label has a layout
        if layout is None:
            layout = QtWidgets.QVBoxLayout()
            self.ui.additional_label.setLayout(layout)

        # Display captured images if the list is not empty
        if image_list:
            displayed_images = [layout.itemAt(i).widget().findChild(
                QtWidgets.QLabel) for i in range(layout.count())]

            # Create a scroll area to contain the images and checkboxes
            scroll_area = QtWidgets.QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setFrameShape(
                QtWidgets.QFrame.NoFrame)  # Remove frame shape

            # Create a widget to contain the layout of the images and checkboxes
            scroll_content = QtWidgets.QWidget()
            scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
            scroll_layout.setAlignment(QtCore.Qt.AlignTop)  # Align to top

            # Add "Select All" checkbox
            select_all_checkbox = QtWidgets.QCheckBox("Select All")
            select_all_checkbox.stateChanged.connect(self.select_all_images)
            scroll_layout.addWidget(
                select_all_checkbox, alignment=QtCore.Qt.AlignLeft)

            # Create a horizontal layout for each image and checkbox
            for index, image_path in enumerate(image_list):
                if image_path not in displayed_images:
                    # Create a widget to contain the image and checkbox
                    image_widget = QtWidgets.QWidget()

                    # Create QLabel for image
                    label = QtWidgets.QLabel()
                    pixmap = QtGui.QPixmap(image_path)
                    # Scale image to fit additional_label
                    pixmap = pixmap.scaledToHeight(
                        150, QtCore.Qt.SmoothTransformation)
                    pixmap = pixmap.scaledToWidth(
                        150, QtCore.Qt.SmoothTransformation)
                    label.setPixmap(pixmap)

                    # Create checkbox
                    checkbox = QtWidgets.QCheckBox("Select")
                    checkbox.stateChanged.connect(
                        lambda state, idx=index: self.update_selected_images(state, idx))
                    self.all_checkboxes.append(checkbox)
                    # label.mouseDoubleClickEvent = lambda event, index=index: self.image_double_clicked(
                    # image_path)

                    # Create a layout for checkbox
                    checkbox_layout = QtWidgets.QHBoxLayout()
                    # Align checkbox to right
                    checkbox_layout.addWidget(
                        checkbox, alignment=QtCore.Qt.AlignLeft)

                   # Create layout for image and checkbox layout
                    layout_image_checkbox = QtWidgets.QVBoxLayout()
                    layout_image_checkbox.addLayout(checkbox_layout)
                    layout_image_checkbox.addWidget(label)
                    image_widget.setLayout(layout_image_checkbox)

                    # Add image widget to the scroll layout
                    scroll_layout.addWidget(image_widget)
                    label.mouseDoubleClickEvent = lambda event, path=image_path: self.image_double_clicked(
                        path)
                    # label.customContextMenuRequested.connect(
                    #     lambda point, index=index, label=label: self.open_context_menu(point, index, label))

            # Set the scroll content widget
            scroll_area.setWidget(scroll_content)

            # Add the scroll area to additional_label
            layout.addWidget(scroll_area)

    def image_double_clicked(self):
        # Increment the click counter for the clicked image
        if self.selected_images:
            self.image = self.selected_images[0]
            self.ui.stackedWidget.setCurrentIndex(1)
            self.load_image()

    def update_selected_images(self, state, index):
        if state == Qt.Checked:
            image_path = image_list[index]
            if image_path not in self.selected_images:
                self.selected_images.append(image_path)
        else:
            image_path = image_list[index]
            if image_path in self.selected_images:
                self.selected_images.remove(image_path)

    def image_clicked(self, label, index):
        # Get the image path corresponding to the clicked label
        # image_path = self.image_labels.get(label)

        # Load the clicked image into the show_image label
        self.image_labels[label] = image_list[index]
        self.image = image_list[index]
        self.imageIndex = index
        self.latestImage.append(self.read())
        self.load_image()

    def load_image(self):
        pixmap = QPixmap(self.image)
        pixmap = pixmap.scaled(391, 541, Qt.KeepAspectRatio)

        # Set alignment to center
        self.ui.show_image.setAlignment(Qt.AlignCenter)
        self.ui.show_image.setPixmap(pixmap)

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

    def select_all_images(self, state):
        for checkbox in self.all_checkboxes:
            checkbox.setChecked(state == Qt.Checked)

            if state == Qt.Checked:
                image_path = image_list[self.all_checkboxes.index(checkbox)]
                if image_path not in self.selected_images:
                    self.selected_images.append(image_path)
            else:
                image_path = image_list[self.all_checkboxes.index(checkbox)]
                if image_path in self.selected_images:
                    self.selected_images.remove(image_path)

    def delete_image(self):
        global image_list
        image_list = [
            elem for elem in image_list if elem not in self.selected_images]
        self.revert_image_clicked()

    def adjust_contrast(self):

        if self.image is not None:
            # Convert NumPy array to PIL image
            pil_image = Image.fromarray(
                cv2.cvtColor(self.read(), cv2.COLOR_BGR2RGB))

            # Apply contrast enhancement
            contrast_value = 1.5
            contrast_enhancer = ImageEnhance.Contrast(pil_image)
            enhanced_image = contrast_enhancer.enhance(contrast_value)

            # Convert the enhanced image back to a NumPy array
            enhanced_image_np = cv2.cvtColor(
                np.array(enhanced_image), cv2.COLOR_RGB2BGR)

            # Display the enhanced image
            self.latestImage.append(enhanced_image_np)
            # self.image = enhanced_image_np
            self.write(enhanced_image_np)
            self.load_image()

    def write(self, imagee):
        cv2.imwrite(self.image, imagee)

    def read(self):
        return cv2.imread(self.image)

    def undo(self):
        if len(self.latestImage) > 1:
            self.latestImage.pop()
            self.write(self.latestImage[-1])
            self.load_image()

    def open_context_menu(self, point, index, label):
        menu = QMenu()
        crop_action = menu.addAction("Crop")
        delete_action = menu.addAction("Delete")
        action = menu.exec_(label.mapToGlobal(point))
        if action == crop_action:
            self.crop_image(index)
        elif action == delete_action:
            self.delete_image(index)

    def crop_image(self):
            if self.image:
                # Load the image using the stored path
                image = cv2.imread(self.image)
                if image is not None:
                    # Clone the image
                    clone = image.copy()

                    # Initialize the list of reference points and boolean indicating cropping
                    refPt = []
                    cropping = False

                    def click_and_crop(event, x, y, flags, param):
                        nonlocal refPt, cropping, image
                        # If the left mouse button was clicked, record the starting (x, y) coordinates
                        if event == cv2.EVENT_LBUTTONDOWN:
                            refPt = [(x, y)]
                            cropping = True
                        # If the left mouse button was released, record the ending (x, y) coordinates
                        elif event == cv2.EVENT_LBUTTONUP:
                            refPt.append((x, y))
                            cropping = False
                            # Draw a rectangle around the region of interest
                            cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
                            cv2.imshow("image", image)

                    # Setup the mouse callback function
                    cv2.namedWindow("image")
                    cv2.setMouseCallback("image", click_and_crop)

                    while True:
                        # Display the image and wait for a keypress
                        cv2.imshow("image", image)
                        key = cv2.waitKey(1) & 0xFF
                        # If the 'r' key is pressed, reset the cropping region
                        if key == ord("r"):
                            image = clone.copy()
                            cv2.destroyAllWindows()
                            break

                    # If there are two reference points, crop the region of interest from the image and display it
                    if len(refPt) == 2:
                        roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
                        cv2.imshow("ROI", roi)
                        cv2.waitKey(0)

                        # Save the cropped image
                        cropped_image_path = "cropped_image.jpg"  # Modify the path as needed
                        cv2.imwrite(cropped_image_path, roi)

                        # Update self.image with the path to the cropped image
                        self.image = cropped_image_path
                        self.load_image()
                        self.selected_images[0]=self.image
                        # global image_list
                        self.display_captured_images_main()
                        

                    # Close all open windows
    def crop_image_settings(self):
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
            image_resolution = frame.shape[:2]  # Get only the rows and columns

            print("Image resolution:", image_resolution)

            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")  # Format timestamp
            filename = f"captured_image_{timestamp}.jpg"

            # Create a temporary directory
            temp_dir = tempfile.mkdtemp()

            # Specify the filepath within the temporary directory
            filepath = os.path.join(temp_dir, filename)

            try:
                # Save the cropped image with timestamp
                cv2.imwrite(filepath, frame)
                print("Image saved successfully.")
                          # Load the image using the stored path
                image = cv2.imread(filepath)
                if image is not None:
                # Clone the image
                    clone = image.copy()

                # Initialize the list of reference points and boolean indicating cropping
                refPt = []
                cropping = False

                def click_and_crop(event, x, y, flags, param):
                        nonlocal refPt, cropping, image
                        # If the left mouse button was clicked, record the starting (x, y) coordinates
                        if event == cv2.EVENT_LBUTTONDOWN:
                            refPt = [(x, y)]
                            cropping = True
                        # If the left mouse button was released, record the ending (x, y) coordinates
                        elif event == cv2.EVENT_LBUTTONUP:
                            refPt.append((x, y))
                            cropping = False
                            # Draw a rectangle around the region of interest
                            cv2.rectangle(
                                image, refPt[0], refPt[1], (0, 255, 0), 2)
                            cv2.imshow("image", image)

                    # Setup the mouse callback function
                cv2.namedWindow("image")
                cv2.setMouseCallback("image", click_and_crop)

                while True:
                        # Display the image and wait for a keypress
                        cv2.imshow("image", image)
                        key = cv2.waitKey(1) & 0xFF
                        # If the 'r' key is pressed, reset the cropping region
                        if key == ord("r"):
                            image = clone.copy()
                            cv2.destroyAllWindows()
                            break
                    # If there are two reference points, crop the region of interest from the image and display it
                if len(refPt) == 2:
                    self.crop_size = refPt
                    roi = clone[self.crop_size[0][1]:self.crop_size[1]
                                [1], self.crop_size[0][0]:self.crop_size[1][0]]
                    cv2.imshow("ROI", roi)
                    cv2.waitKey(0)
                    # Save the cropped image
                    cropped_image_path = "cropped_image.jpg"  # Modify the path as needed
                    cv2.imwrite(cropped_image_path, roi)

                    # Update self.image with the path to the cropped image
                    # self.image = cropped_image_path
                    # self.load_image()
                    # self.selected_images[0] = self.image
                    #   # global image_list
                    # self.display_captured_images_main()
                # Append the filepath to the captured images list
                # self.captured_images.append(filepath)

                # Call display_captured_images to update the display
                # self.display_captured_images_main()

            except Exception as e:
                print(f"Error saving image: {e}")

    def save(self):
        global image_list
        if self.imageIndex is not None:
            image_list[self.imageIndex] = self.image

    def adjust_sharpness(self):

        if self.image is not None:
            # Convert NumPy array to PIL image
            pil_image = Image.fromarray(
                cv2.cvtColor(self.read(), cv2.COLOR_BGR2RGB))

            # Apply sharpness enhancement
            sharpness_value = 2.0
            sharpness_enhancer = ImageEnhance.Sharpness(pil_image)
            enhanced_image = sharpness_enhancer.enhance(sharpness_value)

            # Convert the enhanced image back to a NumPy array
            enhanced_image_np = cv2.cvtColor(
                np.array(enhanced_image), cv2.COLOR_RGB2BGR)

            # Display the enhanced image
            self.latestImage.append(enhanced_image_np)
            # self.image = enhanced_image_np
            self.write(enhanced_image_np)
            self.load_image()

    def revert_image_clicked(self):
        if self.image is not None:
            # Remove the image path from self.image_labels
            self.image = None
            self.imageIndex = None

            # Remove the latest image from self.latestImage
            if self.latestImage:
                self.latestImage.pop()

            # Reload the previously displayed image if available
            if self.latestImage:
                self.load_image()

    def AutoEnhance(self):
        pil_image = Image.fromarray(
            cv2.cvtColor(self.read(), cv2.COLOR_BGR2RGB))

        # Apply color enhancement
        enhanced_image = ImageEnhance.Color(pil_image).enhance(1.5)

        # Convert the enhanced image back to a NumPy array
        enhanced_image_np = cv2.cvtColor(
            np.array(enhanced_image), cv2.COLOR_RGB2BGR)

        # Display the enhanced image
        self.latestImage.append(enhanced_image_np)
        # self.image = enhanced_image_np
        self.write(enhanced_image_np)
        self.load_image()

    def blackAndWhite(self):
        bw_image = cv2.cvtColor(self.read(), cv2.COLOR_BGR2GRAY)
        self.latestImage.append(bw_image)
        # self.image = bw_image
        self.write(bw_image)
        self.load_image()

    def grayscale(self):
        grayscale_image = cv2.cvtColor(self.read(), cv2.COLOR_BGR2GRAY)
        self.latestImage.append(grayscale_image)
        # self.image = grayscale_image
        self.write(grayscale_image)
        self.load_image()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
