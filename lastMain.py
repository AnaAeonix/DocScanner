from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
import sys
# from camDesign import Ui_MainWindoww, VideoStream
from PyQt5.QtCore import QTimer, Qt
from datetime import datetime
import os
import sys
import cv2
# from sidebarNew_ui import Ui_MainWindow,VideoStream
from CropApp import CropApp
import tkinter as tk
from ariNewUi import Ui_MainWindow, VideoStream
# from test import Ui_MainWindow,  VideoStream
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtWidgets, QtGui, QtCore
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
# from camDes1main import MainWindow1
from PIL import Image, ImageEnhance, ImageOps, ImageQt
import cv2
import numpy as np
from smartCrop import SmartCrop
import win32com.client


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.image_click_counter = {}
        self.crop_size = []
        self.latestImage = []
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")  # Format timestamp
        filename = f"captured_image_{timestamp}.jpg"
        self.auto_crop = None
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # Specify the filepath within the temporary directory
        self.imagepath = os.path.join(temp_dir, filename)
        # self.prevlab = None
        # self.prevlabIndex = None
        # Create a dictionary to store references to labels corresponding to image paths
        self.image = None  # Track the currently displayed image
        self.imageIndex = None
        self.sharp_img= None
        self.contrasted_image= None
        self.rotation_state = 0  # Initial rotation state
        self.dpi = 72

        self.selected_images = []  # Store selected images
        self.all_checkboxes = []   # Store references to all checkboxes
        self.current_camera_index = 0
        self.captured_images = []
        self.captured_images_crop = []
        self.captured_images_main = []
        self.export = 0

        self.ui.edit_btn.clicked.connect(self.editing)
        # Initialize video stream with default camera
        self.video_stream = VideoStream(
            self.ui.cam_label, self.current_camera_index)
        self.ui.shutter_btn.clicked.connect(self.capture_image)
        self.ui.rotateleft_btn.clicked.connect(self.rotate_image_left)
        self.ui.rotateright_btn.clicked.connect(self.rotate_image_right)
        self.ui.adjust_btn.clicked.connect(self.clicked_adjust_btn)
        self.ui.color_btn.clicked.connect(self.clicked_color_btn)
        self.ui.rotate_btn.clicked.connect(self.clicked_rotate_btn)
        self.ui.pdf_btn.clicked.connect(self.exportTo)
        self.ui.cam_back.clicked.connect(self.returntocamera)
        self.ui.enhance_btn.clicked.connect(self.AutoEnhance)
        self.ui.crop_btn.clicked.connect(self.askQuestion)
        self.ui.settings_btn.clicked.connect(self.askQuestion_settings)
        self.ui.delete_btn.clicked.connect(self.delete_image)
        self.ui.horizontalSlider_2.valueChanged.connect(self.update_sharpness)
        self.ui.horizontalSlider.valueChanged.connect(self.update_contrast)
        # self.ui.delete_btn.clicked.connect(self.delete)
        self.ui.ai_btn.toggled.connect(self.video_stream.toggle_contour_detection)
        self.ui.foc_drop.currentIndexChanged.connect(
            self.video_stream.set_focus)
        self.ui.dpi_drop.currentIndexChanged.connect(
            self.getDpi)
        self.ui.resolution_drop.currentIndexChanged.connect(
            self.resolution_set  )


        self.ui.export_drop.currentIndexChanged.connect(
            self.export_change)
        self.setFocusPolicy(Qt.StrongFocus)
        self.ui.save_btn.clicked.connect(self.save)
        self.ui.undo_btn.clicked.connect(self.undo)
        self.ui.discard_btn.clicked.connect(self.discard)
        # self.ui.jpeg_btn.clicked.connect(self.export_image)
        self.ui.ok_btn.clicked.connect(self.ok_btn_clicked)
        self.ui.ok1_btn.clicked.connect(self.ok1_btn_clicked)

        self.ui.mag1_btn.clicked.connect(self.magic1)
        self.ui.mag2_btn.clicked.connect(self.magic2)
        
        self.setWindowFlags(Qt.FramelessWindowHint)  # Hide default title bar
        self.ui.minimize.clicked.connect(self.showMinimized)
        self.ui.close.clicked.connect(self.close)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.video_stream.update_frame)
        self.timer.start(50)  # Update camera feed every 50 milliseconds

        self.cap = None
        self.populate_camera_dropdown()
    # for path file to array convert and viceversa

    def write(self, imagee):
        self.image = cv2.imread(imagee)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_C and self.ui.stackedWidget.currentIndex() == 0:
            self.capture_image()  # Call your function here
        else:
            super().keyPressEvent(event)


    def delete(self):
        print(self.captured_images_crop)
        print(self.captured_images_main)
        print(self.captured_images)
        

    def get_resolutions_for_camera(self, camera_id):
        # Dummy function to get resolutions for a given camera ID
        # Replace this with your actual implementation
        resolutions = {
            "USB\\VID_BC07&PID_1801&MI_00\\7&647E327&0&0000": ["3264x2448", "4160x3120", "4000x3000", "4208x3120", "2592x1944", "2320x1744", "2304x1728"],
            "USB\\VID_BC15&PID_2C1B&MI_00\\6&23BABD32&0&0000": ["3264x2448", "2592x1944", "2560x1440", "1920x1080", "1280x720", "640x480"]
        }
        res =["1920x1080", "1280x720", "640x480"]
        res1 = resolutions.get(camera_id, [])
        if res1 is not None:
            return resolutions.get(camera_id, [])
        else:
            return res
    
    def resolution_set(self,index):
        
        global indexRes
        indexRes = index
        
                
            
    
    
    
    def getDpi(self,index):
        if index==0:
            self.dpi = 72
        if index == 1:
            self.dpi = 96
        if index == 2:
            self.dpi = 150
        if index == 3:
            self.dpi = 200
        if index == 4:
            self.dpi = 300 

# common section code

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
            # temp = temp.reverse()
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
            if save_path != '':
                pdf_canvas.save()
        else:
            # Inform the user if no images are selected

            QMessageBox.information(self, "No Selection",
                                    "No image selected for making PDF.")

    def create_pdf_with_images(self):
        save_path, _ = QFileDialog.getSaveFileName(
            None, "Save PDF", "", "PDF Files (*.pdf)")
        if self.selected_images:
            temp = self.selected_images.copy()
            temp.reverse()
            # Determine maximum image size
            max_width = max([Image.open(image_path).width for _,
                            image_path in self.selected_images])
            max_height = max(
                [Image.open(image_path).height for _, image_path in self.selected_images])

            # Create PDF with page size matching the largest image
            pdf_canvas = canvas.Canvas(
                save_path, pagesize=(max_width, max_height))
            for _, image_path in temp:
                img = Image.open(image_path)
                img_width, img_height = img.size
                x_offset = (max_width - img_width) / 2
                y_offset = (max_height - img_height) / 2

                # Draw white background
                pdf_canvas.setFillGray(1)
                pdf_canvas.rect(0, 0, max_width, max_height, fill=1)

                # Draw image
                pdf_canvas.drawImage(
                    image_path, x_offset, y_offset, width=img_width, height=img_height)
                pdf_canvas.showPage()  # End current page
            if save_path != '':
                pdf_canvas.save()
        else:
            # Inform the user if no images are selected
            QMessageBox.information(None, "No Selection",
                                    "No image selected for making PDF.")

    def export_image(self):
        if len(self.selected_images) == 1:
            save_path, _ = QFileDialog.getSaveFileName(
               None, "Save JPEG", "", "JPEG Files (*.jpeg *.jpg)")
            if save_path:
                self.selected_images = sorted(self.selected_images, key=lambda x: x[0])
                for index, image_path in self.selected_images:
                    image = cv2.imread(image_path)
                    if image is not None:
                        height, width, _ = image.shape
                        # Convert OpenCV image to PIL Image
                        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        pil_image = Image.fromarray(image_rgb)
                        # Save image as JPEG
                        pil_image.save(save_path) 
        # Check the number of selected images
        elif len(self.selected_images)>1:
            temp = self.selected_images.copy()
            temp.reverse()
            # Ask the user for the save directory
            save_directory = QFileDialog.getExistingDirectory(
                None, "Select Save Directory", "")
            i = 0
            if save_directory:
                try:
                    for (index, filepath) in temp:
                        # Generate the filename with sequential numbering and .jpeg extension
                        filename = f"{i}.jpeg"
                        i += 1
                        save_path = os.path.join(save_directory, filename)

                        image = QImage(filepath)

                        # Convert the QImage to a QPixmap
                        pixmap = QPixmap.fromImage(image)
                        if pixmap:
                            # Save the QPixmap as JPEG
                            pixmap.save(save_path, "JPEG")
                            print(f"Image {index} saved as", save_path)
                        else:
                            print(f"Failed to convert image {index}.")
                except Exception as e:
                    print(f"Error exporting images: {e}")
            else:
                print("Save operation cancelled by the user.")
        else :
            # Inform the user if no images are selected
            QMessageBox.information(
                self, "No Selection", "No images selected for export.")

    def export_change(self, index):
        self.export = index

    def exportTo(self, export_format):
        export_format = self.export
        if export_format == 0:
            # Export as PDF
            save_path, _ = QFileDialog.getSaveFileName(
                None, "Save PDF", "", "PDF Files (*.pdf)")
            if self.selected_images:
                temp = self.selected_images.copy()
                temp.reverse()
                # Determine maximum image size
                max_width = max([Image.open(image_path).width for _,
                                image_path in self.selected_images])
                max_height = max(
                    [Image.open(image_path).height for _, image_path in self.selected_images])

                # Create PDF with page size matching the largest image
                pdf_canvas = canvas.Canvas(
                    save_path, pagesize=(max_width, max_height))
                for _, image_path in temp:
                    img = Image.open(image_path)
                    img_width, img_height = img.size
                    x_offset = (max_width - img_width) / 2
                    y_offset = (max_height - img_height) / 2

                    # Draw white background
                    pdf_canvas.setFillGray(1)
                    pdf_canvas.rect(0, 0, max_width, max_height, fill=1)

                    # Draw image
                    pdf_canvas.drawImage(
                        image_path, x_offset, y_offset, width=img_width, height=img_height)
                    pdf_canvas.showPage()  # End current page
                if save_path != '':
                    pdf_canvas.save()
            else:
                # Inform the user if no images are selected
                QMessageBox.information(
                    None, "No Selection", "No image selected for making PDF.")
        elif export_format == 1:
            # Export as JPEG
            if len(self.selected_images) == 1:
                save_path, _ = QFileDialog.getSaveFileName(
                    None, "Save JPEG", "", "JPEG Files (*.jpeg *.jpg)")
                if save_path:
                    self.selected_images = sorted(
                        self.selected_images, key=lambda x: x[0])
                    for index, image_path in self.selected_images:
                        image = cv2.imread(image_path)
                        if image is not None:
                            height, width, _ = image.shape
                            # Convert OpenCV image to PIL Image
                            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                            pil_image = Image.fromarray(image_rgb)
                            # Save image as JPEG
                            pil_image.save(save_path, dpi=(self.dpi, self.dpi))
            elif len(self.selected_images) > 1:
                temp = self.selected_images.copy()
                temp.reverse()
                save_directory = QFileDialog.getExistingDirectory(
                    None, "Select Save Directory", "")
                i = 0
                if save_directory:
                    try:
                        for (index, filepath) in temp:
                            filename = f"{i}.jpeg"
                            i += 1
                            save_path = os.path.join(save_directory, filename)

                            # image = QImage(filepath)
                            # buffer = image.bits()
                            # buffer.setsize(image.byteCount())
                            # arr = np.array(buffer).reshape((image.height(), image.width(), 4))
                            # # Convert the array to RGB mode (ignoring the alpha channel)
                            # arr_rgb = arr[:, :, :3]

                            # # Convert numpy array to PIL Image
                            # pil_image = Image.fromarray(arr_rgb)

                            # # Save image as JPEG with DPI
                            # pil_image.save(save_path, dpi=(self.dpi, self.dpi))
                            
                            # Read the image using OpenCV
                            image = cv2.imread(filepath)

                            # Convert BGR image to RGB
                            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                            # Convert the RGB numpy array to PIL Image
                            pil_image = Image.fromarray(image_rgb)

                            # Save image as JPEG with DPI
                            pil_image.save(save_path, dpi=(self.dpi, self.dpi))

                            # # Convert the QImage to a QPixmap
                            # pixmap = QPixmap.fromImage(image)
                            # if pixmap:
                            #     pixmap.save(save_path, "JPEG")
                            #     print(f"Image {index} saved as", save_path)
                            # else:
                            #     print(f"Failed to convert image {index}.")
                    except Exception as e:
                        print(f"Error exporting images: {e}")
                else:
                    print("Save operation cancelled by the user.")
            else:
                QMessageBox.information(
                    self, "No Selection", "No images selected for export.")
        elif export_format == 2:
            # Export as TIFF
            save_path, _ = QFileDialog.getSaveFileName(
                None, "Save TIFF", "", "TIFF Files (*.tiff *.tif)")
            if save_path:
                self.selected_images = sorted(
                    self.selected_images, key=lambda x: x[0])
                for index, image_path in self.selected_images:
                    image = cv2.imread(image_path)
                    if image is not None:
                        height, width, _ = image.shape
                        # Convert OpenCV image to PIL Image
                        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        pil_image = Image.fromarray(image_rgb)
                        # Save image as TIFF
                        pil_image.save(
                            save_path, format="TIFF", dpi=(self.dpi, self.dpi))
        else:
            QMessageBox.information(None, "Invalid Format",
                                    "The specified format is not supported.")
    
    def editing(self):
        # Increment the click counter for the clicked image
        if len(self.selected_images) == 1:
            self.write(self.selected_images[0][1])
            self.latestImage.clear()
            self.latestImage.append(self.image)
            self.imageIndex = self.selected_images[0][0]
            self.ui.stackedWidget.setCurrentIndex(1)
            self.load_image()
        elif len(self.selected_images) > 1:
            # Inform the user if no images are selected
            QMessageBox.information(self, " Selection",
                                    "More than one image is selected")
        else:

            # Inform the user if no images are selected
            QMessageBox.information(self, "No Selection",
                                    "No image selected for editing.")

    def are_images_equal(self, image1, image2):
        # Check if both images have the same shape
        if image1.shape != image2.shape:
            return False

        # Compare each pixel value in the images
        comparison = image1 == image2
        if comparison.all():
            return True
        else:
            return False

    def image_double_clicked(self, label, path, index):
        # if self.image is not None and self.are_images_equal(self.image, self.latestImage[-1]) is False:
        #     msg_box = QMessageBox()
        #     msg_box.setIcon(QMessageBox.Warning)
        #     msg_box.setText("Please do undo or save.")
        #     msg_box.setWindowTitle("Alert")
        #     msg_box.setStandardButtons(QMessageBox.Ok)
        #     msg_box.exec_()
        # else:

        if self.imageIndex != index:
            self.write(path)
            self.imageIndex = index
            cv2.imwrite(self.imagepath, self.image)
            self.latestImage.clear()
            self.latestImage.append(self.image)
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
            select_all_widget = QtWidgets.QWidget()
            select_all_layout = QtWidgets.QHBoxLayout(select_all_widget)

            select_all_checkbox = QtWidgets.QCheckBox("Select All")
            select_all_checkbox.stateChanged.connect(self.select_all_images)
            select_all_checkbox.setStyleSheet(
                "color: #3020ee; font-weight: bold; font-family: Arial;")  # Add this line
            select_all_layout.addWidget(
                select_all_checkbox, alignment=QtCore.Qt.AlignLeft)

            # Add label to show number of images
            num_images_label = QtWidgets.QLabel(
                f" ({len(self.captured_images)} images)")
            num_images_label.setStyleSheet(
                "color: #808080; font-family: Arial;")
            select_all_layout.addWidget(
                num_images_label, alignment=QtCore.Qt.AlignLeft)

            scroll_layout.addWidget(select_all_widget)

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
                    checkbox.setStyleSheet(
                        "QCheckBox::indicator { width: 20px; height: 20px; border: none; background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8a2be2, stop:0.5 #0e86f6, stop:1 #a78bfa); }")
                    checkbox.setStyleSheet(
                        "color: #3020ee; font-weight: bold; font-family: Arial;")  # Add this line

                    # Create layout for checkbox
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
                    label.mouseDoubleClickEvent = lambda state, ind=index, lab=label, path=image_path: self.image_double_clicked(lab,
                                                                                                                                 path, ind)

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

                self.captured_images = [elem for elem in self.captured_images if elem not in [
                    x[1] for x in self.selected_images]]

                # Clear the list of selected images
                if any(index == self.imageIndex for index, _ in self.selected_images):
                    print("ok")
                    self.ui.stackedWidget.setCurrentIndex(0)
                    self.imageIndex = None
                    self.image = None

                self.selected_images.clear()
                # Update the display
                self.display_captured_images_main()
        else:
            # Inform the user if no images are selected
            QMessageBox.information(self, "No Selection",
                                    "No images selected for deletion.")

    def crop_settings(self):
        ret, frame = self.video_stream.video.read()
        show_window = True
        print(tk.TkVersion)

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

                root = tk.Tk()
                root.title("Auto Crop")
                img_file_name = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cv2.imwrite("Hello2.jpg", img_file_name)
                # coordinates = [[5, 5], [1029, 5], [742, 209], [5, 773]]
                if self.auto_crop == None or len(self.auto_crop) == 6:
                    App = CropApp(root, img_file_name)
                else:
                    App = CropApp(root, img_file_name, inplace=True,
                                  coordinates=self.auto_crop)
                root.mainloop()
 
                A = np.asarray(App.NW.coords) * App.scale_factor
                B = np.asarray(App.NE.coords) * App.scale_factor
                C = np.asarray(App.SE.coords) * App.scale_factor
                D = np.asarray(App.SW.coords) * App.scale_factor
                self.auto_crop = [A, B, C, D]
                self.auto_crop = [(int(A[0]), int(A[1]))
                                  for A in self.auto_crop]
                print(self.auto_crop)
                self.video_stream.points = self.auto_crop
                print(A)
                print(B)
                print(C)
                print(D)

            except Exception as e:
                print(f"Error saving image: {e}")

    def crop_settings_6(self):
        ret, frame = self.video_stream.video.read()
        show_window = True
        # print(tk.TkVersion)

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

                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                root = tk.Tk()
                root.title("Auto Crop")
                if self.auto_crop == None or len(self.auto_crop) == 4:
                    obj = SmartCrop(image, root)
                else:
                    obj = SmartCrop(image, root,
                                    points=self.auto_crop)
                # obj = SmartCrop(image, root)
                obj.run()
                corners = obj.get_draggable_points()

                split1, split2, warpped_image = obj.get_warpped(corners)
                # cv2.imwrite("1714054747202_warpped_1.jpg",
                #             cv2.cvtColor(split1, cv2.COLOR_BGR2RGB))
                # cv2.imwrite("1714054747202_warpped_2.jpg",
                #             cv2.cvtColor(split2, cv2.COLOR_BGR2RGB))
                # cv2.imwrite("1714054747202_warpped.jpg", cv2.cvtColor(
                #     warpped_image, cv2.COLOR_BGR2RGB))
                self.auto_crop = corners
                self.video_stream.points = corners
                print(corners)
            except Exception as e:
                print(f"Error saving image: {e}")


# camerafeed window


    # def populate_camera_dropdown(self):
    #     global available_cameras
    #     available_cameras = []
    #     for i in range(10):
    #         cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    #         if cap.isOpened(): 
    #             backend_id = cap.get(cv2.CAP_PROP_BACKEND)
    #             camera_name = f"Camera {i} - Backend: {backend_id}"
    #             available_cameras.append((i, camera_name))
    #             del cap

    #     # Clear any selected item in the dropdown
    #     self.ui.cam_drop_down.clear()
    #     # Set the placeholder text
    #     self.ui.cam_drop_down.setPlaceholderText("Please select a camera")

    #     # Assuming available_cameras is a list of tuples containing camera indices and names
    #     camera_names = [camera_name for _, camera_name in available_cameras]

    #     # Add camera names to the dropdown
    #     self.ui.cam_drop_down.addItems(camera_names)

    #     # Connect the currentIndexChanged signal
    #     self.ui.cam_drop_down.currentIndexChanged.connect(
    #         lambda: self._handle_index_change())
    #     # self.ui.cam_drop_down.currentIndexChanged.connect(
    #     #     lambda: self._handle_index_change1())

    def list_cameras(self):
        index = 0
        arr = []
        i = 10
        while i > 0:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
            index += 1
            i -= 1
        return arr


    def list_usb_cameras(self):
        strComputer = "."
        objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        objSWbemServices = objWMIService.ConnectServer(strComputer, "root\\cimv2")

        colItems = objSWbemServices.ExecQuery(
            "Select * from Win32_PnPEntity where DeviceID like '%VID_%&PID_%'")

        cameras = []
        for objItem in colItems:
            if "camera" in objItem.Description.lower() or "video" in objItem.Description.lower():
                camera_info = {
                    'description': objItem.Description,
                    'device_id': objItem.DeviceID,
                    'manufacturer': objItem.Manufacturer,
                    'name': objItem.Name,
                    'status': objItem.Status
                }
                cameras.append(camera_info)
        return cameras


    def populate_camera_dropdown(self):
        global available_cameras
        available_cameras = []

        # List available camera indices
        camera_indices = self.list_cameras()
        global usb_cameras 
        usb_cameras = self.list_usb_cameras()
        
        # Creating a dictionary for USB camera details keyed by name
        camera_details = {camera['device_id']: camera for camera in usb_cameras}

        i=0
        for index in camera_indices:
            
            cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            if cap.isOpened():
                backend_id = cap.get(cv2.CAP_PROP_BACKEND) 
                name = usb_cameras[index]['device_id']
                details = camera_details.get(name, {})
                description = details.get('device_id', 'Unknown')
                manufacturer = details.get('manufacturer', 'Unknown')
                camera_name = f"{name} ({description})"
                available_cameras.append((index, camera_name))
                cap.release()

        # Match camera indices with USB camera details
        # camera_details = {}
        # for camera in usb_cameras:
        #     camera_details[camera['name']] = camera

        # Clear any selected item in the dropdown
        self.ui.cam_drop_down.clear()
        # Set the placeholder text
        self.ui.cam_drop_down.setPlaceholderText("Please select a camera")

        # Add camera names and details to the dropdown
        # camera_names = []
        # for index, name in available_cameras:
        #     if name in camera_details:
        #         details = camera_details[name]
        #         camera_name = f"{name} ({details['description']}, {
        #             details['manufacturer']})"
        #     else:
        #         camera_name = name
        #     camera_names.append(camera_name)
        # Add camera names to the dropdown
        camera_names = [camera_name for _, camera_name in available_cameras]
        self.ui.cam_drop_down.addItems(camera_names)

        # resolutions = self.get_resolutions_for_camera(self.current_camera_index)
        # self.ui.resolution_drop.addItems(resolutions)
        # Connect the currentIndexChanged signal
        self.ui.cam_drop_down.currentIndexChanged.connect(
            lambda: self._handle_index_change())


    def load_image(self):
        cv2.imwrite(self.imagepath, self.image)
        pixmap = QPixmap(self.imagepath)
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
        self.ui.resolution_drop.clear()
        self.video_stream.change_camera(self.current_camera_index)
        resolutions= self.get_resolutions_for_camera(usb_cameras[self.current_camera_index]["device_id"])
        self.ui.resolution_drop.addItems(resolutions)

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
                original_res = (frame.shape[1], frame.shape[0])
                height,width = self.getRes()
                if(height is None):
                    height = 2448
                    width = 3264
                frame = cv2.resize(
                    frame, (width, height), interpolation=cv2.INTER_AREA)
                self.captured_images_main.insert(0, frame)
                if self.video_stream.checked==True:
                    if self.video_stream.ai_crop is not None:
                        frame = self.warp_perspective(
                            frame, self.video_stream.ai_crop)
                # Save the cropped image with timestamp
                if self.auto_crop is not None:
                    if len(self.auto_crop) == 4:
                        temp = self.scale_crop_coordinates(
                            self.auto_crop, original_res, (width, height))
                        frame = self.crop_cutting(
                            frame, temp[0], temp[1], temp[2], temp[3])
                    else:
                        temp = self.scale_crop_coordinates_6(
                            self.auto_crop, original_res, (width, height))
                        frame = self.cutting_6(Image.fromarray(
                            frame), temp[0], temp[1], temp[2], temp[3], temp[4], temp[5])
                cv2.imwrite(filepath, frame)

                if(self.auto_crop != None):
                    self.captured_images_crop.insert(0, self.auto_crop)
                else:
                    self.captured_images_crop.insert(0, [0,0])
                # Append the filepath to the captured images list
                self.captured_images.insert(0, filepath)
                self.selected_images.clear()
                # Call display_captured_images to update the display
                self.display_captured_images_main()

            except Exception as e:
                print(f"Error saving image: {e}")

    def scale_crop_coordinates_6(self, crop, original_res, new_res):
        original_width, original_height = original_res
        new_width, new_height = new_res

        scale_x = new_width / original_width
        scale_y = new_height / original_height

        x, y, w, h ,a , b= crop
        xwidth, xheight = x
        new_x = (int(xwidth * scale_x), int(xheight * scale_y))
        ywidth, yheight = y
        new_y = (int(ywidth * scale_x), int(yheight * scale_y))
        wwidth, wheight = w
        new_w = (int(wwidth * scale_x), int(wheight * scale_y))
        hwidth, hheight = h
        new_h = (int(hwidth * scale_x), int(hheight * scale_y))
        awidth, aheight = a
        new_a = (int(awidth * scale_x), int(aheight * scale_y))
        bwidth, bheight = b
        new_b = (int(bwidth * scale_x), int(bheight * scale_y))

        return [new_x, new_y, new_w, new_h,new_a,new_b]
    def scale_crop_coordinates(self, crop, original_res, new_res):
        original_width, original_height = original_res
        new_width, new_height = new_res

        scale_x = new_width / original_width
        scale_y = new_height / original_height

        x, y, w, h = crop
        xwidth, xheight = x
        new_x = (int(xwidth * scale_x), int(xheight * scale_y))
        ywidth, yheight = y
        new_y = (int(ywidth * scale_x), int(yheight * scale_y))
        wwidth, wheight = w
        new_w = (int(wwidth * scale_x), int(wheight * scale_y))
        hwidth, hheight = h
        new_h = (int(hwidth * scale_x), int(hheight * scale_y))

        return [new_x, new_y, new_w, new_h]
    
    def getRes(self):
        global indexRes
        device = usb_cameras[self.current_camera_index]["device_id"]
        if device == "USB\\VID_BC07&PID_1801&MI_00\\7&647E327&0&0000":
            if indexRes == 3:
                width = 4208
                height = 3120
                return height,width
            if indexRes == 1:
                width = 4160
                height = 3120
                return height, width
            if indexRes == 2:
                width = 4000
                height = 3000
                return height,width
            if indexRes == 0:
                width = 3264
                height = 2448
                return height,width
            if indexRes == 4:
                width = 2592
                height = 1944
                return height, width
            if indexRes == 5:
                width = 2320
                height = 1744
                return height,width
            if indexRes == 6:
                width = 2304
                height = 1728
                return height, width

        elif device == "USB\\VID_BC15&PID_2C1B&MI_00\\6&23BABD32&0&0000":
            if indexRes == 0:
                width = 3264
                height = 2448
                return height, width
            if indexRes == 1:
                width = 2592
                height = 1944
                return height,width
            if indexRes == 2:
                width = 2560
                height = 1440
                return height,width
            if indexRes == 3:
                width = 1920
                height = 1080
                return height, width
            if indexRes == 4:
                width = 1280
                height = 720
                return height, width
            if indexRes == 5:
                width = 640
                height = 480
                return height, width
            else:
                if indexRes == 0:
                    width = 1920
                    height = 1080
                    return height,width
                if indexRes == 1:
                    width = 1280
                    height = 720
                    return height,width
                if indexRes == 2:
                    width = 640
                    height = 480
                    return height, width
                
    def capture_image_resChange(self, height, width):
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
                frame = cv2.resize(
                    frame, (width, height), interpolation=cv2.INTER_AREA)
                self.captured_images_main.insert(0, frame)
                if self.video_stream.checked == True:
                    if self.video_stream.ai_crop is not None:
                        frame = self.warp_perspective(
                            frame, self.video_stream.ai_crop)
                # Save the cropped image with timestamp
                if self.auto_crop is not None:
                    if len(self.auto_crop) == 4:
                        frame = self.crop_cutting(
                            frame, self.auto_crop[0], self.auto_crop[1], self.auto_crop[2], self.auto_crop[3])
                    else:
                        frame = self.cutting_6(Image.fromarray(
                            frame), self.auto_crop[0], self.auto_crop[1], self.auto_crop[2], self.auto_crop[3], self.auto_crop[4], self.auto_crop[5])
                cv2.imwrite(filepath, frame)

                if (self.auto_crop != None):
                    self.captured_images_crop.insert(0, self.auto_crop)
                else:
                    self.captured_images_crop.insert(0, [0, 0])
                # Append the filepath to the captured images list
                self.captured_images.insert(0, filepath)
                self.selected_images.clear()
                # Call display_captured_images to update the display
                self.display_captured_images_main()

            except Exception as e:
                print(f"Error saving image: {e}")

    def get_image_coordinates(self, image_array):
        height, width = image_array.shape[:2]

        # Define the coordinates of the four corners
        top_left = np.array([0, 0])
        top_right = np.array([width - 1, 0])
        bottom_left = np.array([0, height - 1])
        bottom_right = np.array([width - 1, height - 1])

        # Stack the coordinates vertically to form a bidimensional array
        coordinates = np.vstack(
            (top_left, top_right, bottom_right, bottom_left))

        return coordinates


# for editing purpose


    def returntocamera(self):
        self.imageIndex = None
        self.image = None
        self.ui.stackedWidget.setCurrentIndex(0)

    def clicked_adjust_btn(self):
        self.ui.edit_stack.setCurrentIndex(0)

    def clicked_color_btn(self):
        self.ui.edit_stack.setCurrentIndex(1)

    def clicked_rotate_btn(self):
        self.ui.edit_stack.setCurrentIndex(2)

    def rotate_image_right(self):
        if self.image is not None:
            self.rotation_state -= 90
            if self.rotation_state < 0:
                self.rotation_state = 270
            rotated_image = self.image
            rotated_image = cv2.rotate(
                rotated_image, cv2.ROTATE_90_CLOCKWISE)
            # self.latestImage.append(rotated_image)
            # self.image = rotated_image
            self.image = rotated_image
            self.load_image()

    def rotate_image_left(self):
        if self.image is not None:
            if self.rotation_state == 270:
                self.rotation_state = 0
            else:
                self.rotation_state += 90
            rotated_image = self.image.copy()
            rotated_image = cv2.rotate(
                rotated_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            # self.latestImage.append(rotated_image)
            # self.image = rotated_image
            self.image = rotated_image
            # self.display_captured_images_main()
            self.load_image()

    # def adjust_contrast(self, value):
    #     try:
    #         if self.image is not None:
    #             # Load the image from the file path
    #             image = cv2.imread(self.image)

    #             if image is not None:
    #                 # Convert the image to grayscale if it's not already
    #                 if len(image.shape) == 3:
    #                     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #                 else:
    #                     gray_image = image

    #                 # Calculate the contrast factor
    #                 contrast_factor = (value + 100) / 100.0

    #                 # Adjust the contrast using convertScaleAbs
    #                 adjusted_image = cv2.convertScaleAbs(
    #                     gray_image, alpha=contrast_factor, beta=0)

    #                 # Display the adjusted image
    #                 self.image = adjusted_image

    #                 self.load_image()
    #             else:
    #                 raise ValueError("Unable to load the image.")
    #         else:
    #             raise ValueError("No image path provided.")
    #     except Exception as e:
    #         print("Error:", e)

    def display_image(self, image):
        pixmap = QPixmap.fromImage(QImage(
            image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888))
        self.ui.show_image.setPixmap(pixmap.scaled(
            self.ui.show_image.size(), Qt.KeepAspectRatio))

    def undo(self):
        self.image = self.latestImage[-1]
        if len(self.latestImage) > 1:
            self.latestImage.pop()
        self.load_image()

    def discard(self):
        self.image = self.latestImage[0]
        while len(self.latestImage) > 1:
            self.latestImage.pop()
        self.load_image()

    def askQuestion_settings(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Crop Type")
        msgBox.setText("What type of crop do you want?")
        yes_button = msgBox.addButton(QMessageBox.Yes)
        yes_button.setText("Single Page Crop")
        no_button = msgBox.addButton(QMessageBox.No)
        no_button.setText("Double Page Crop")

        msgBox.exec()

        if msgBox.clickedButton() == yes_button:
            self.crop_settings()
        elif msgBox.clickedButton() == no_button:
            self.crop_settings_6()

    def askQuestion(self):
        if self.captured_images_crop[self.imageIndex] == [0, 0]:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Crop Type")
            msgBox.setText("What type of crop do you want?")
            yes_button = msgBox.addButton(QMessageBox.Yes)
            yes_button.setText("Single Page Crop")
            no_button = msgBox.addButton(QMessageBox.No)
            no_button.setText("Double Page Crop")

            msgBox.exec()

            msgBox.rejected.connect(self.handle_msg_box_closed)

            if msgBox.clickedButton() == yes_button:
                self.crop_image_4()
            elif msgBox.clickedButton() == no_button:
                self.crop_image_6()
        elif len(self.captured_images_crop[self.imageIndex]) == 6:
            self.crop_image_6()
        else:
            self.crop_image_4()

    def handle_msg_box_closed(self):
        # Implement this function to handle the case when the message box is closed without any button being clicked
        pass  # You can leave it empty or provide any specific behavior you want

    def crop_image_4(self):
        root = tk.Tk()
        root.title("Crop")
        img_file_name = cv2.cvtColor(
            self.captured_images_main[self.imageIndex], cv2.COLOR_BGR2RGB)
        # coordinates = [[5, 5], [1029, 5], [742, 209], [5, 773]]
        # if np.array_equal(self.get_image_coordinates(cv2.imread(self.captured_images[self.imageIndex])), self.captured_images_crop[self.imageIndex]):
        if self.captured_images_crop[self.imageIndex] == [0, 0]:
                App = CropApp(root, img_file_name)
        else:
            App = CropApp(root, img_file_name, inplace=True,
                          coordinates= self.captured_images_crop[self.imageIndex])
        root.mainloop()
        print(App.crop_pressed)
        if App.crop_pressed:
            A = np.asarray(App.NW.coords) * App.scale_factor
            B = np.asarray(App.NE.coords) * App.scale_factor
            C = np.asarray(App.SE.coords) * App.scale_factor
            D = np.asarray(App.SW.coords) * App.scale_factor

            print(A)
            print(B)

            print(C)
            print(D)
            coordinates = [A, B, C, D]
            final = self.crop_cutting(
                self.captured_images_main[self.imageIndex], A, B, C, D)
            cv2.imwrite('DistortSample1Output.jpg', final)
            self.captured_images_crop[self.imageIndex] = coordinates
            self.image = final
            self.load_image()
            print(final)

    def crop_image_6(self):
        image = Image.fromarray(cv2.cvtColor(
            self.captured_images_main[self.imageIndex], cv2.COLOR_BGR2RGB))
        root = tk.Tk()
        root.title("Crop")
        if self.captured_images_crop[self.imageIndex] == [0, 0]:
                obj = SmartCrop(
                    image, root)
        else:
            obj = SmartCrop(image, root,
                            points=self.captured_images_crop[self.imageIndex])
        # obj = SmartCrop(image, root)
        obj.run()
        if obj.crop_pressed:
            corners = obj.get_draggable_points()

            split1, split2, warpped_image = obj.get_warpped(corners)
            # cv2.imwrite("1714054747202_warpped_1.jpg",
            #             cv2.cvtColor(split1, cv2.COLOR_BGR2RGB))
            # cv2.imwrite("1714054747202_warpped_2.jpg",
            #             cv2.cvtColor(split2, cv2.COLOR_BGR2RGB))
            # cv2.imwrite("1714054747202_warpped.jpg", cv2.cvtColor(
            #     warpped_image, cv2.COLOR_BGR2RGB))
            print(corners)
            # root = tk.Tk()
            # img_file_name = img_file_name = cv2.cvtColor(
            #     self.captured_images_main[self.imageIndex], cv2.COLOR_BGR2RGB)
            # # coordinates = [[5, 5], [1029, 5], [742, 209], [5, 773]]
            # if np.array_equal(self.get_image_coordinates(cv2.imread(self.captured_images[self.imageIndex])), self.captured_images_crop[self.imageIndex]):
            #     App = CropApp(root, img_file_name)
            # else:
            #     App = CropApp(root, img_file_name, inplace=True,
            #                   coordinates=self.captured_images_crop[self.imageIndex])
            # root.mainloop()

            # A = np.asarray(App.NW.coords) * App.scale_factor
            # B = np.asarray(App.NE.coords) * App.scale_factor
            # C = np.asarray(App.SE.coords) * App.scale_factor
            # D = np.asarray(App.SW.coords) * App.scale_factor

            # print(A)
            # print(B)
            # print(C)
            # print(D)
            # coordinates = [A, B, C, D]
            # final = self.crop_cutting(
            #     self.captured_images_main[self.imageIndex], A, B, C, D)
            # cv2.imwrite('DistortSample1Output.jpg', final)
            self.captured_images_crop[self.imageIndex] = corners
            self.image = cv2.cvtColor(warpped_image, cv2.COLOR_RGB2BGR)
            self.load_image()
            print(warpped_image)

    def crop_cutting(self, image_path, A, B, C, D):
        coordinates = [A, B, C, D]
        widthA = np.sqrt(((C[0] - D[0]) ** 2) + ((C[1] - D[1]) ** 2))
        widthB = np.sqrt(((B[0] - A[0]) ** 2) + ((B[1] - A[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        # Finding the maximum height.
        heightA = np.sqrt(((B[0] - C[0]) ** 2) + ((B[1] - C[1]) ** 2))
        heightB = np.sqrt(((A[0] - D[0]) ** 2) + ((A[1] - D[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        # Final destination co-ordinates.
        destination_corners = [
            [0, 0],
            [maxWidth, 0],
            [maxWidth, maxHeight],
            [0, maxHeight]]
        homography = cv2.getPerspectiveTransform(
            np.float32(coordinates), np.float32(destination_corners))

        # Perspective transform using homography.
        final = cv2.warpPerspective(image_path, np.float32(
            homography), (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)

        return final
    
    def warp_perspective(self, image, p):
        r = np.zeros((4, 2), dtype="float32")
        s = np.sum(p, axis=1)
        r[0] = p[np.argmin(s)]
        r[2] = p[np.argmax(s)]
        d = np.diff(p, axis=1)
        r[1] = p[np.argmin(d)]
        r[3] = p[np.argmax(d)]
        (tl, tr, br, bl) = r

        wA = np.sqrt((tl[0] - tr[0])**2 + (tl[1] - tr[1])**2)
        wB = np.sqrt((bl[0] - br[0])**2 + (bl[1] - br[1])**2)
        maxW = max(int(wA), int(wB))

        hA = np.sqrt((tl[0] - bl[0])**2 + (tl[1] - bl[1])**2)
        hB = np.sqrt((tr[0] - br[0])**2 + (tr[1] - br[1])**2)
        maxH = max(int(hA), int(hB))

        ds = np.array(
            [[0, 0], [maxW - 1, 0], [maxW - 1, maxH - 1], [0, maxH - 1]], dtype="float32")

        transformMatrix = cv2.getPerspectiveTransform(r, ds)
        scan = cv2.warpPerspective(image, transformMatrix, (maxW, maxH))

        # T = threshold_local(scan, 21, offset=10, method="gaussian")
        # scanBW = (scan > T).astype("uint8") * 255

        return scan
    
    
    def cutting_6(self, image_path, A, B, C, D, E, F):
        corners = [A, B, C, D, E, F]
        (tl1, tr1, br1, bl1) = (corners[0], corners[1], corners[4], corners[5])
        (tl2, tr2, br2, bl2) = (corners[1], corners[2], corners[3], corners[4])
        # Finding the maximum width.
        widthA = np.sqrt(((br1[0] - bl1[0]) ** 2) + ((br1[1] - bl1[1]) ** 2))
        widthB = np.sqrt(((tr1[0] - tl1[0]) ** 2) + ((tr1[1] - tl1[1]) ** 2))
        widthC = np.sqrt(((br2[0] - bl2[0]) ** 2) + ((br2[1] - bl2[1]) ** 2))
        widthD = np.sqrt(((tr2[0] - tl2[0]) ** 2) + ((tr2[1] - tl2[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB), int(widthC), int(widthD))

        # Finding the maximum height.
        heightA = np.sqrt(((tr1[0] - br1[0]) ** 2) + ((tr1[1] - br1[1]) ** 2))
        heightB = np.sqrt(((tl1[0] - bl1[0]) ** 2) + ((tl1[1] - bl1[1]) ** 2))
        heightC = np.sqrt(((tr2[0] - br2[0]) ** 2) + ((tr2[1] - br2[1]) ** 2))
        heightD = np.sqrt(((tl2[0] - bl2[0]) ** 2) + ((tl2[1] - bl2[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB), int(heightC), int(heightD))
        # Final destination co-ordinates.
        destination_corners = [
            [0, 0],
            [maxWidth, 0],
            [maxWidth, maxHeight],
            [0, maxHeight]]

        # Getting the homography.
        homography1 = cv2.getPerspectiveTransform(np.float32(
            [tl1, tr1, br1, bl1]), np.float32(destination_corners))
        homography2 = cv2.getPerspectiveTransform(np.float32(
            [tl2, tr2, br2, bl2]), np.float32(destination_corners))
        # Perspective transform using homography.
        final1 = cv2.warpPerspective(np.array(image_path), np.float32(
            homography1), (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)
        final2 = cv2.warpPerspective(np.array(image_path), np.float32(
            homography2), (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)
        return np.concatenate((final1, final2), axis=1)

    def save(self):
        self.latestImage.append(self.image)
        if self.imageIndex is not None:
            cv2.imwrite(self.captured_images[self.imageIndex], self.image)

        self.selected_images.clear()
        self.display_captured_images_main()
        self.load_image()

    # def adjust_sharpness(self):

    #     if self.image is not None:
    #         # Convert NumPy array to PIL image
    #         pil_image = Image.fromarray(
    #             cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))

    #         # Apply sharpness enhancement
    #         sharpness_value = 2.0
    #         sharpness_enhancer = ImageEnhance.Sharpness(pil_image)
    #         enhanced_image = sharpness_enhancer.enhance(sharpness_value)

    #         # Convert the enhanced image back to a NumPy array
    #         enhanced_image_np = cv2.cvtColor(
    #             np.array(enhanced_image), cv2.COLOR_RGB2BGR)

    #         self.image = enhanced_image_np
    #         self.load_image()

    def update_sharpness(self, value):
        sharpness = value / 100.0
        self.sharp_img = self.sharpen_image(self.image, sharpness)
        # self.image = sharpened_image
        cv2.imwrite(self.imagepath, self.sharp_img)
        pixmap = QPixmap(self.imagepath)
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


    def sharpen_image(self, image, sharpness):
        blurred = cv2.GaussianBlur(image, (0, 0), 3)
        sharpened = cv2.addWeighted(
            image, 1.0 + sharpness, blurred, -sharpness, 0)
        return sharpened
    
    def update_contrast(self, value):
        contrast = value
        self.contrasted_image = self.adjust_contrast(self.image, contrast)
        # self.image = sharpened_image
        cv2.imwrite(self.imagepath, self.contrasted_image)
        pixmap = QPixmap(self.imagepath)
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

    def adjust_contrast(self, image, contrast):
        alpha = (100.0 + contrast) / 100.0
        adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=0)
        return adjusted

    def ok1_btn_clicked(self):
        if self.sharp_img is not None:
            self.image=self.sharp_img
            self.load_image()
            self.sharp_img= None
        
            
    def ok_btn_clicked(self):
        if self.contrasted_image is not None:
            self.image = self.contrasted_image
            self.load_image()
            self.contrasted_image = None

    def AutoEnhance(self):
        pil_image = Image.fromarray(
            cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))

        # Apply color enhancement
        enhanced_image = ImageEnhance.Color(pil_image).enhance(1.5)

        # Convert the enhanced image back to a NumPy array
        enhanced_image_np = cv2.cvtColor(
            np.array(enhanced_image), cv2.COLOR_RGB2BGR)

        self.image = enhanced_image_np
        self.load_image()

    def magic1(self, image_path):
        # Read the image
        # image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        if len(self.image.shape) == 3 and self.image.shape[2] == 3:
            # Image is in BGR format, convert to grayscale
            image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        elif len(self.image.shape) == 2:
            # Image is already grayscale
            image = self.image

        # Check if the image was read successfully
        if image is None:
            print("Error: Unable to read the image.")
            return None

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(image, (1, 1), 0)

        # Apply adaptive thresholding with inverted binary threshold
        enhanced_image = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 4)

        self.image = enhanced_image
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
            input_image = self.image

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
                self.image = enhanced_image

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
