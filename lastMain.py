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


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.showMaximized()

        self.image_click_counter = {}
        self.crop_size = []
        self.latestImage = []

        # Create a dictionary to store references to labels corresponding to image paths
        self.image = None  # Track the currently displayed image
        self.imageIndex = None
        self.rotation_state = 0  # Initial rotation state

        self.selected_images = []  # Store selected images
        self.all_checkboxes = []   # Store references to all checkboxes
        self.current_camera_index = 0
        self.captured_images = []
        self.ui.edit_btn.clicked.connect(self.editing)
        # Initialize video stream with default camera
        self.video_stream = VideoStream(
            self.ui.cam_label, self.current_camera_index)
        self.ui.shutter_btn.clicked.connect(self.capture_image)
        self.ui.rotateleft_btn.clicked.connect(self.rotate_image_left)
        self.ui.rotateright_btn.clicked.connect(self.rotate_image_right)
        # self.ui.done_btn.clicked.connect(self.clicked_done_btn)
        self.ui.adjust_btn.clicked.connect(self.clicked_adjust_btn)
        self.ui.color_btn.clicked.connect(self.clicked_color_btn)
        self.ui.rotate_btn.clicked.connect(self.clicked_rotate_btn)
        self.ui.pdf_btn.clicked.connect(self.make_pdf)
        self.ui.cam_back.clicked.connect(self.returntocamera)
        self.ui.enhance_btn.clicked.connect(self.AutoEnhance)
        self.ui.crop_btn.clicked.connect(self.crop_image)
        self.ui.settings_btn.clicked.connect(self.crop_image_settings)
        self.ui.delete_btn.clicked.connect(self.delete_image)
        self.ui.save_btn.clicked.connect(self.save)
        self.ui.undo_btn.clicked.connect(self.undo)
        self.ui.discard_btn.clicked.connect(self.discard)
        self.ui.jpeg_btn.clicked.connect(self.export_image)
        # self.p = r"C:\Users\sdas\OneDrive\Desktop\aeonix\DocScanner\temp_image.png"
        self.ui.mag1_btn.clicked.connect(self.magic1)
        self.ui.mag2_btn.clicked.connect(self.magic2)
        self.ui.horizontalSlider.valueChanged.connect(self.adjust_contrast)
        self.setWindowFlags(Qt.FramelessWindowHint)  # Hide default title bar
        self.ui.minimize.clicked.connect(self.showMinimized)
        self.ui.close.clicked.connect(self.close)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.video_stream.display_camera_feed)
        self.timer.start(50)  # Update camera feed every 50 milliseconds

        self.cap = None
        self.populate_camera_dropdown()
    #for path file to array convert and viceversa
    def write(self, imagee):
        cv2.imwrite(self.image, imagee)

    def read(self):
        return cv2.imread(self.image)




















###common section code 

    def make_pdf(self):
        # Ask the user for the save path
        # save_path, _ = QFileDialog.getSaveFileName(
        #     None, "Save PDF", "", "PDF Files (*.pdf)")
        # if save_path:
            if self.selected_images:
                # Ask the user for the save path
                save_path, _ = QFileDialog.getSaveFileName(
                None, "Save PDF", "", "PDF Files (*.pdf)")
                self.selected_images = sorted(
                    self.selected_images, key=lambda x: x[0])
                pdf_canvas = canvas.Canvas(save_path, pagesize=letter)
                for (index, image_path) in self.selected_images:
                    image = cv2.imread(image_path)
                    if image is not None:
                        height, width, _ = image.shape
                        # Set the PDF page size same as image size
                        pdf_canvas.setPageSize((width, height))
                        # Place image on PDF
                        pdf_canvas.drawImage(image_path, 0, 0, width, height)
                        pdf_canvas.showPage()  # End current page
                if save_path!='':
                    pdf_canvas.save()
            else:
                # Inform the user if no images are selected
                
                QMessageBox.information(self, "No Selection",
                                    "No image selected for making PDF.")
                
    def export_image(self):
        # Check the number of selected images
        if len(self.selected_images) == 1:
            # Ask the user for the save path
            save_path, _ = QFileDialog.getSaveFileName(
                None, "Save Image", "", "JPEG Files (*.jpg)")
            if save_path:
                image = QImage(self.selected_images[0][1])

                # Convert the QImage to a QPixmap
                pixmap = QPixmap.fromImage(image)
                if pixmap and save_path!='':
                    pixmap.save(save_path, "JPEG")
                    print("Image saved as", save_path)
                else:
                    print("No image to save.")
            else :
                print("Save operation cancelled by the user.")
        elif len(self.selected_images) == 0:
            QMessageBox.information(self, "No Selection",
                                    "No image selected for making JPG.")
        else:
            # Show a message box indicating more than one image is selected
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText("More than one image is selected.")
            msg_box.setWindowTitle("Multiple Images Selected")
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()


    def editing(self):
            # Increment the click counter for the clicked image
        if len(self.selected_images) ==1:
            self.image = self.selected_images[0][1]
            self.latestImage.clear()
            self.latestImage.append(self.read())
            self.imageIndex = self.selected_images[0][0]
            self.ui.stackedWidget.setCurrentIndex(1)
            self.load_image()
        elif len(self.selected_images) >1:
            # Inform the user if no images are selected
            QMessageBox.information(self, " Selection",
                                    "More than one image is selected")
        else:
            
            # Inform the user if no images are selected
            QMessageBox.information(self, "No Selection",
                                    "No image selected for editing.")

    def image_double_clicked(self, path, index):
        # Increment the click counter for the clicked image
        # if self.selected_images:
        self.image = path
        self.imageIndex = index
        self.latestImage.clear()
        self.latestImage.append(self.read())
        self.ui.stackedWidget.setCurrentIndex(1)
        self.load_image()
        
    def display_captured_images_main(self):
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
        if self.captured_images:
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
            select_all_checkbox.setStyleSheet(
                "color: #3020ee; font-weight: bold; font-family: Arial;")  # Add this line
            scroll_layout.addWidget(
                select_all_checkbox, alignment=QtCore.Qt.AlignLeft)

            # Create a horizontal layout for each image and checkbox
            for index, image_path in enumerate(self.captured_images):
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
                    # checkbox.setStyleSheet(
                    #     "QCheckBox::indicator { width: 20px; height: 20px; border: 10px solid qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa); }")
                    checkbox.setStyleSheet(
                        "QCheckBox::indicator { width: 20px; height: 20px; border: none; background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa); }")

                    checkbox.setStyleSheet(
                        "color: #3020ee; font-weight: bold; font-family: Arial;")  # Add this line
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
                    label.mouseDoubleClickEvent = lambda event, ind = index, path=image_path: self.image_double_clicked(
                        path, ind)
                    # label.customContextMenuRequested.connect(
                    #     lambda point, index=index, label=label: self.open_context_menu(point, index, label))

            # Set the scroll content widget
            scroll_area.setWidget(scroll_content)

            # Add the scroll area to additional_label
            layout.addWidget(scroll_area)

    def update_selected_images(self, state, index):
        image_path = self.captured_images[index]
        if state == Qt.Checked:
            # Append a tuple containing both the index and image path
            if (index, image_path) not in self.selected_images:
                self.selected_images.append((index, image_path))
        else:
            # Remove the tuple containing both the index and image path
            if (index, image_path) in self.selected_images:
                self.selected_images.remove((index, image_path))

    def select_all_images(self, state):
        for checkbox in self.all_checkboxes:
            checkbox.setChecked(state == Qt.Checked)
            index = self.all_checkboxes.index(checkbox)
            if state == Qt.Checked:
                image_path = self.captured_images[index]
                if (index, image_path) not in self.selected_images:
                    self.selected_images.append((index, image_path))
            else:
                image_path = self.captured_images[index]
                if (index, image_path) in self.selected_images:
                    self.selected_images.remove((index, image_path))

    
    def delete_image(self):
            # Check if there are selected images
        if self.selected_images:
            # Ask for confirmation
            confirm_dialog = QMessageBox()
            confirm_dialog.setIcon(QMessageBox.Question)
            confirm_dialog.setText(
                "Are you sure you want to delete the selected image(s)?")
            confirm_dialog.setWindowTitle("Confirmation")
            confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

            # Execute based on user's choice
            choice = confirm_dialog.exec_()
            if choice == QMessageBox.Yes:
                # Delete selected images from captured_images
                self.captured_images = [elem for elem in self.captured_images if elem not in [
                    x[1] for x in self.selected_images]]
                # Clear the list of selected images
                self.selected_images.clear()
                # Update the display
                self.display_captured_images_main()
        else:
            # Inform the user if no images are selected
            QMessageBox.information(self, "No Selection",
                                    "No images selected for deletion.")

    def crop_image_settings(self):
        ret, frame = self.video_stream.video.read()

        if ret:
            image_resolution = frame.shape[:2]  # Get only the rows and columns

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
                        if not np.array_equal(image, clone):
                            image[:] = clone[:]
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

                    # Save the cropped image
                    cropped_image_path = "cropped_image.jpg"  # Modify the path as needed
                    cv2.imwrite(cropped_image_path, roi)

            except Exception as e:
                print(f"Error saving image: {e}")
        
        
        
        
        
        
        
        
        
        
        






###camerafeed window
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
        
    def load_image(self):
        pixmap = QPixmap(self.image)
        # pixmap = pixmap.scaled(391, 541, Qt.KeepAspectRatio)

        # Set alignment to center
        self.ui.show_image.setAlignment(Qt.AlignCenter)
        self.ui.show_image.setPixmap(pixmap)

        # Set alignment to center
        self.ui.show_image.setAlignment(Qt.AlignCenter)

        # Set aspect ratio mode to keep the aspect ratio
        self.ui.show_image.setScaledContents(True)
        self.ui.show_image.setPixmap(pixmap.scaled(
            self.ui.show_image.size(), Qt.KeepAspectRatio))

    def _handle_index_change(self):
        # Access the current index
        self.current_camera_index = self.ui.cam_drop_down.currentIndex()
    # Do something with the new_index value
        # Call your function with the index
        self.video_stream.change_camera(self.current_camera_index)

    def capture_image(self):
        ret, frame = self.video_stream.video.read()

        if ret:
            image_resolution = frame.shape[:2]  # Get only the rows and columns


            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")  # Format timestamp
            filename = f"captured_image_{timestamp}.jpg"

            # Create a temporary directory
            temp_dir = tempfile.mkdtemp()

            # Specify the filepath within the temporary directory
            filepath = os.path.join(temp_dir, filename)

            try:
                # Save the cropped image with timestamp
                if self.crop_size != []:
                    frame = frame[self.crop_size[0][1]:self.crop_size[1]
                                  [1], self.crop_size[0][0]:self.crop_size[1][0]]
                cv2.imwrite(filepath, frame)

                # Append the filepath to the captured images list
                self.captured_images.append(filepath)

                # Call display_captured_images to update the display
                self.display_captured_images_main()

            except Exception as e:
                print(f"Error saving image: {e}")



















##for editing purpose


    def returntocamera(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def clicked_adjust_btn(self):
        self.ui.edit_stack.setCurrentIndex(0)

    def clicked_color_btn(self):
        self.ui.edit_stack.setCurrentIndex(1)

    def clicked_rotate_btn(self):
        self.ui.edit_stack.setCurrentIndex(2)

    def rotate_image_right(self):
        if self.read() is not None:
            self.rotation_state -= 90
            if self.rotation_state < 0:
                self.rotation_state = 270
            rotated_image = self.read().copy()
            rotated_image = cv2.rotate(
                    rotated_image, cv2.ROTATE_90_CLOCKWISE)
            # self.latestImage.append(rotated_image)
            # self.image = rotated_image
            self.write(rotated_image)
            self.load_image()


    def rotate_image_left(self):
        if self.read() is not None:
            if self.rotation_state == 270:
                self.rotation_state = 0
            else:
                self.rotation_state += 90
            rotated_image = self.read().copy()
            rotated_image = cv2.rotate(rotated_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # self.latestImage.append(rotated_image)
            # self.image = rotated_image
            self.write(rotated_image)
            self.load_image()


    def adjust_contrast(self, value):
        try:
            if self.image is not None:
                # Load the image from the file path
                image = cv2.imread(self.image)

                if image is not None:
                    # Convert the image to grayscale if it's not already
                    if len(image.shape) == 3:
                        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    else:
                        gray_image = image

                    # Calculate the contrast factor
                    contrast_factor = (value + 100) / 100.0

                    # Adjust the contrast using convertScaleAbs
                    adjusted_image = cv2.convertScaleAbs(
                        gray_image, alpha=contrast_factor, beta=0)

                    # Display the adjusted image
                    self.write(adjusted_image)
                    self.load_image()
                else:
                    raise ValueError("Unable to load the image.")
            else:
                raise ValueError("No image path provided.")
        except Exception as e:
            print("Error:", e)

    def display_image(self, image):
        pixmap = QPixmap.fromImage(QImage(
            image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888))
        self.ui.show_image.setPixmap(pixmap.scaled(
            self.ui.show_image.size(), Qt.KeepAspectRatio))

    def undo(self):
        self.write(self.latestImage[-1])
        if len(self.latestImage) > 1:
            self.latestImage.pop()
        self.load_image()

    def discard(self):
        if len(self.latestImage) > 1:
            self.latestImage.pop()
            self.write(self.latestImage[0])
            self.load_image()
            
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
                        if not np.array_equal(image, clone):
                            image[:] = clone[:]
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
                    roi = clone[refPt[0][1]:refPt[1]
                                [1], refPt[0][0]:refPt[1][0]]

                    # Save the cropped image
                    cropped_image_path = "cropped_image.jpg"  # Modify the path as needed
                    cv2.imwrite(cropped_image_path, roi)

                    # Update self.image with the path to the cropped image
                    self.image = cropped_image_path
                    self.load_image()

                # Close all open windows


    def save(self):
        self.latestImage.append(self.read())
        if self.imageIndex is not None:
            self.captured_images[self.imageIndex] = self.image
        self.display_captured_images_main()
        self.load_image()
        
        
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

            self.write(enhanced_image_np)
            self.load_image()


    def AutoEnhance(self):
        pil_image = Image.fromarray(
            cv2.cvtColor(self.read(), cv2.COLOR_BGR2RGB))

        # Apply color enhancement
        enhanced_image = ImageEnhance.Color(pil_image).enhance(1.5)

        # Convert the enhanced image back to a NumPy array
        enhanced_image_np = cv2.cvtColor(
            np.array(enhanced_image), cv2.COLOR_RGB2BGR)

        self.write(enhanced_image_np)
        self.load_image()


    def magic1(self,image_path):
        # Read the image
        image = cv2.imread(self.image, cv2.IMREAD_GRAYSCALE)

        # Check if the image was read successfully
        if image is None:
            print("Error: Unable to read the image.")
            return None

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(image, (1, 1), 0)

        # Apply adaptive thresholding with inverted binary threshold
        enhanced_image = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 4)

        self.write(enhanced_image)
        self.load_image()


    # def magic2(self,image, alpha=1.1, beta=0):
    #     """
    #     Enhance the contrast of an image using brightness and contrast adjustments.
    #     :param image: Input image
    #     :param alpha: Contrast control (1.0-3.0)
    #     :param beta: Brightness control (0-100)
    #     :return: Enhanced image
    #     """
    #     # input_image = cv2.imread(str(self.image))
    #     enhanced_image = cv2.convertScaleAbs(self.read, alpha=alpha, beta=beta)
    #     self.write(enhanced_image)
    #     self.load_image()
        

    def magic2(self, image, alpha=1.1, beta=0):
        """
        Enhance the contrast of an image using brightness and contrast adjustments.
        :param image: Input image
        :param alpha: Contrast control (1.0-3.0)
        :param beta: Brightness control (0-100)
        :return: Enhanced image
        """
        try:
            # Load the image from the file path
            input_image = cv2.imread(str(self.image))

            if input_image is not None:
                # Convert the image to grayscale if it's not already
                if len(input_image.shape) == 3:
                    gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
                else:
                    gray_image = input_image

                # Adjust contrast and brightness
                enhanced_image = cv2.convertScaleAbs(
                    gray_image, alpha=alpha, beta=beta)

                # Write the enhanced image
                self.write(enhanced_image)

                # Reload the image
                self.load_image()
            else:
                print("Error: Unable to load the image.")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())
