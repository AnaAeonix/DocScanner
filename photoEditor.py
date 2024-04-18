import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QInputDialog,QComboBox
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageEnhance, ImageOps
import cv2
import numpy as np
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt

class PhotoEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Editor App")
        self.setGeometry(100, 100, 800, 600)

        self.image_label = QLabel(self)
        self.image_label.setGeometry(50, 50, 600, 400)

        self.upload_button = QPushButton("Upload Photo", self)
        self.upload_button.setGeometry(50, 500, 150, 30)
        self.upload_button.clicked.connect(self.upload_photo)

        self.contrast_button = QPushButton("Adjust Contrast", self)
        self.contrast_button.setGeometry(220, 500, 150, 30)
        self.contrast_button.clicked.connect(self.adjust_contrast)

        self.sharpness_button = QPushButton("Adjust Sharpness", self)
        self.sharpness_button.setGeometry(390, 500, 150, 30)
        self.sharpness_button.clicked.connect(self.adjust_sharpness)

        self.color_mode_label = QLabel("Color Mode:", self)
        self.color_mode_combo = QComboBox(self)
        self.color_mode_combo.addItem("Auto Enhance")
        self.color_mode_combo.addItem("Color")
        self.color_mode_combo.addItem("Black and White")
        self.color_mode_combo.addItem("Grayscale")
        self.color_mode_combo.addItem("No Filters")
        self.color_mode_combo.setGeometry(560, 500, 150, 30)
        self.color_mode_combo.currentIndexChanged.connect(self.adjust_color_mode)

        self.rotate_left_button = QPushButton("Rotate 90° Left", self)
        self.rotate_left_button.setGeometry(50, 550, 150, 30)
        self.rotate_left_button.clicked.connect(self.rotate_image_left)

        self.rotate_right_button = QPushButton("Rotate 90° Right", self)
        self.rotate_right_button.setGeometry(220, 550, 150, 30)
        self.rotate_right_button.clicked.connect(self.rotate_image_right)

        self.image_path = None
        self.image = None
        self.rotation_state = 0  # Initial rotation state


    def upload_photo(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Photo", "", "Image Files (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_path:
            self.image_path = file_path
            self.load_image()

    def load_image(self):
        if self.image_path:
            self.image = cv2.imread(self.image_path)
            pixmap = QPixmap(self.image_path)
            self.image_label.setPixmap(pixmap.scaled(600, 400))

    def adjust_contrast(self):
        # if self.image is not None:
        #     contrast_value = 1.5
        #     contrast_enhancer = ImageEnhance.Contrast(self.image)
        #     enhanced_image = contrast_enhancer.enhance(contrast_value)
        #     self.display_image(enhanced_image)

        if self.image is not None:
            # Convert NumPy array to PIL image
            pil_image = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
            
            # Apply contrast enhancement
            contrast_value = 1.5
            contrast_enhancer = ImageEnhance.Contrast(pil_image)
            enhanced_image = contrast_enhancer.enhance(contrast_value)
            
            # Convert the enhanced image back to a NumPy array
            enhanced_image_np = cv2.cvtColor(np.array(enhanced_image), cv2.COLOR_RGB2BGR)
            
            # Display the enhanced image
            self.display_image(enhanced_image_np)


    def adjust_sharpness(self):
        # if self.image is not None:
        #     sharpness_value = 2.0
        #     sharpness_enhancer = ImageEnhance.Sharpness(self.image)
        #     enhanced_image = sharpness_enhancer.enhance(sharpness_value)
        #     self.display_image(enhanced_image)

        if self.image is not None:
            # Convert NumPy array to PIL image
            pil_image = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
            
            # Apply sharpness enhancement
            sharpness_value = 2.0
            sharpness_enhancer = ImageEnhance.Sharpness(pil_image)
            enhanced_image = sharpness_enhancer.enhance(sharpness_value)
            
            # Convert the enhanced image back to a NumPy array
            enhanced_image_np = cv2.cvtColor(np.array(enhanced_image), cv2.COLOR_RGB2BGR)
            
            # Display the enhanced image
            self.display_image(enhanced_image_np)


    def adjust_color_mode(self):
        # if self.image is not None:
        #     choice = self.color_mode_combo.currentText()
        #     if choice == "Auto Enhance":
        #         enhanced_image = ImageEnhance.Color(self.image).enhance(1.5)
        #         self.display_image(enhanced_image)
        #     elif choice == "Color":
        #         self.display_image(self.image)
        #     elif choice == "Black and White":
        #         bw_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        #         self.display_image(bw_image)
        #     elif choice == "Grayscale":
        #         grayscale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        #         self.display_image(grayscale_image)
        #     elif choice == "No Filters":
        #         self.display_image(self.image)

        if self.image is not None:
            choice = self.color_mode_combo.currentText()
            if choice == "Auto Enhance":
                # Convert NumPy array to PIL image
                pil_image = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
                
                # Apply color enhancement
                enhanced_image = ImageEnhance.Color(pil_image).enhance(1.5)
                
                # Convert the enhanced image back to a NumPy array
                enhanced_image_np = cv2.cvtColor(np.array(enhanced_image), cv2.COLOR_RGB2BGR)
                
                # Display the enhanced image
                self.display_image(enhanced_image_np)
            elif choice == "Color":
                self.display_image(self.image)
            elif choice == "Black and White":
                bw_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                self.display_image(bw_image)
            elif choice == "Grayscale":
                grayscale_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                self.display_image(grayscale_image)
            elif choice == "No Filters":
                self.display_image(self.image)


    # def rotate_image_left(self):
    #     if self.image is not None:
    #         self.rotation_state -= 90
    #         if self.rotation_state < 0:
    #             self.rotation_state = 270
    #         rotated_image = self.image.copy()
    #         for _ in range(self.rotation_state // 90):
    #             rotated_image = cv2.rotate(rotated_image, cv2.ROTATE_90_CLOCKWISE)
    #         self.display_image(rotated_image)
                
    def rotate_image_left(self):
        if self.image is not None:
            if self.rotation_state == 270:
                self.rotation_state = 0
            else:
                self.rotation_state += 90
            rotated_image = self.image.copy()
            for _ in range(self.rotation_state // 90):
                rotated_image = cv2.rotate(rotated_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.display_image(rotated_image)


    def rotate_image_right(self):
        if self.image is not None:
            self.rotation_state -= 90
            if self.rotation_state < 0:
                self.rotation_state = 270
            rotated_image = self.image.copy()
            for _ in range(abs(self.rotation_state // 90)):
                rotated_image = cv2.rotate(rotated_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.display_image(rotated_image)

    def display_image(self, image):
        # temp_image_path = "temp_image.png"
        # cv2.imwrite(temp_image_path, image)
        # pixmap = QPixmap(temp_image_path)
        # self.image_label.setPixmap(pixmap.scaled(600, 400))
        # temp_image_path = "temp_image.png"
        # cv2.imwrite(temp_image_path, image)

        # # Load the image using PIL to get the original dimensions
        # original_image = Image.open(self.image_path)
        # original_width, original_height = original_image.size

        # # Load the rotated image
        # rotated_image = QPixmap(temp_image_path)

        # # Resize the rotated image to match the original dimensions
        # # rotated_image = rotated_image.scaled(original_width, original_height)

        # self.image_label.setFixedSize(original_width, original_height)

        # self.image_label.setPixmap(rotated_image)

        temp_image_path = "temp_image.png"
        cv2.imwrite(temp_image_path, image)

        # Load the image using PIL to get the original dimensions
        original_image = Image.open(self.image_path)
        original_width, original_height = original_image.size

        # Load the rotated image
        rotated_image = QPixmap(temp_image_path)

        # # Calculate the scale factor to fit the image within the label
        scale_factor = min(self.image_label.width() / rotated_image.width(), self.image_label.height() / rotated_image.height())

        # # Resize the image to fit within the label without distortion
        # rotated_image = rotated_image.scaled(rotated_image.width() * scale_factor, rotated_image.height() * scale_factor)

        # Resize the image to fit within the label without distortion
        scaled_width = int(rotated_image.width() * scale_factor)
        scaled_height = int(rotated_image.height() * scale_factor)
        rotated_image = rotated_image.scaled(scaled_width, scaled_height)


        # Create a black background image with the size of the label
        background_image = QPixmap(self.image_label.size())
        background_image.fill(Qt.black)

        # Calculate the position to center the image within the label
        x_offset = (self.image_label.width() - rotated_image.width()) // 2
        y_offset = (self.image_label.height() - rotated_image.height()) // 2

        # Paint the rotated image onto the black background
        painter = QPainter(background_image)
        painter.drawPixmap(x_offset, y_offset, rotated_image)
        painter.end()

        # Set the background image to the label
        self.image_label.setPixmap(background_image)   


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhotoEditorApp()
    window.show()
    sys.exit(app.exec_())
