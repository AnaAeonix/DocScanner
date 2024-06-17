import cv2
import threading
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel
import numpy as np


class VideoStream:
    def __init__(self, parent_label: QLabel, camera_index):
        self.video = cv2.VideoCapture()

        self.points = None
        self.firstTime = True
        self.parent_label = parent_label
        self.set_resolution()
        self.timer = None
        self.camera_change_thread = None  # Thread for camera switching
        self.scan_document = False
        self.checked = False
        self.ai_crop = None
        self.current_focus = 0

    def set_resolution(self):
        # Check if camera is open
        if not self.video.isOpened():
            print("Error opening camera")
            return

        # Check if 4K resolution is supported
        # Typo fix in height value
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
        width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print(width)
        print(height)
        # if width == 3840 and height == 2160:
        #     print("Using 4K resolution")
        # else:
        #     self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        #     self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        #     print("Using 1080p resolution")
        # ... (rest of your set_resolution logic)

    # def display_camera_feed(self):
    #     if not self.video.isOpened():
    #         # Display error message if camera not open
    #         font = QFont()
    #         font.setPointSize(30)
    #         self.parent_label.setFont(font)
    #         if self.firstTime:
    #             self.parent_label.setText(
    #                 "<p style='font-size:20pt'>Please Select the Camera...</p>")
    #         else:
    #             self.parent_label.setText(
    #                 "<p style='font-size:20pt'>Changing Camera...</p>")
    #         return

    #     ret, frame = self.video.read()
    #     if ret:
    #         self.firstTime = False

    #         # (h, w) = frame.shape[:2]
    #         # center = (w / 2, h / 2)
    #         # M = cv2.getRotationMatrix2D(center, 45, 1.0)
    #             # rotated_frame = cv2.warpAffine(frame, M, (w, h))
    #         if self.points is not None:
    #             cv2.polylines(frame, [np.array(self.points)], True,(0, 255, 0), 6)
    #         rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         frame_resized = cv2.resize(rgb_image, (640, 480))
    #         h, w, ch = frame_resized.shape
    #         bytes_per_line = ch * w
    #         q_img = QImage(frame_resized.data, w, h,
    #                         bytes_per_line, QImage.Format_RGB888)
    #         pixmap = QPixmap.fromImage(q_img)
    #         self.parent_label.setPixmap(pixmap.scaled(
    #                 self.parent_label.size(), Qt.KeepAspectRatio))

    #             # self.parent_label.setFixedSize(w, h)
    #     else:
    #             # Display loader while camera is changing
    #         self.show_loader()

    def display_camera_feed1(self, checked):
        if not self.video.isOpened():
            # Display error message if camera not open
            font = QFont()
            font.setPointSize(30)
            self.parent_label.setFont(font)
            if self.firstTime:
                self.parent_label.setText(
                    "<p style='font-size:20pt'>Please Select the Camera...</p>")
            else:
                self.parent_label.setText(
                    "<p style='font-size:20pt'>Changing Camera...</p>")
            return

        ret, frame = self.video.read()

        if ret:
            self.firstTime = False

            if self.points is not None:
                cv2.polylines(
                    frame, [np.array(self.points)], True, (0, 255, 0), 6)

            # Check if contour detection is enabled
            if checked:
                document_contour = self.detect_document(frame)

                if document_contour is not None:
            # Calculate the area of the detected contour
                    area = cv2.contourArea(document_contour)

                # # Update the biggest contour if the detected one is larger or if the biggest contour is None
                # if area > max_area or biggest_contour is None:
                #     biggest_contour = document_contour
                #     max_area = area

                # # Update the biggest contour if a smaller valid contour is found
                # elif area < max_area and area > 1000:  # Add a minimum area threshold to avoid noise
                #     biggest_contour = document_contour
                #     max_area = area
                    biggest_contour = document_contour
                # Draw the biggest contour on the frame
                    cv2.drawContours(frame, [biggest_contour], -1, (0, 255, 0), 6)
                    p = self.order_points(biggest_contour.reshape(4, 2))

                # Apply perspective transform

                # self.scan_document = True
                # if self.scan_document:
                #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                #     kernel = np.ones((5, 5), np.uint8)
                #     dilation = cv2.dilate(gray, kernel, iterations=5)
                #     blur = cv2.GaussianBlur(dilation, (3, 3), 0)
                #     blur = cv2.erode(blur, kernel, iterations=5)
                #     edge = cv2.Canny(blur, 100, 200)

                # t = 300
                # j = 0
                # linesP = None
                # while j < 8 and t > 0:
                #     try:
                #         linesP = cv2.HoughLines(edge, 1, np.pi / 180, t)
                #         if linesP is not None:
                #             j = linesP.shape[0]
                #         else:
                #             j = 0
                #     except:
                #         j = 0
                #     t -= 10

                # if linesP is not None:
                #     lines = linesP.reshape(linesP.shape[0], 2)
                #     lu = []
                #     for c, l in enumerate(lines):
                #         rho, theta = l
                #         for lt in lines[c + 1:]:
                #             if lt[0] != l[0]:
                #                 k = abs(lt - l) < [50, 0.5]
                #                 if k[0] and k[1]:
                #                     break
                #         else:
                #             lu.append(l)

                #     if len(lu) >= 4:
                #         lr = np.asarray(lu[:4])
                #         intersections = self.points_inter(lr)

                #         if len(intersections) >= 4:
                #             p = np.array(intersections[:4]).reshape(4, 2)

                #             r = np.zeros((4, 2), dtype="float32")
                #             s = np.sum(p, axis=1)
                #             r[0] = p[np.argmin(s)]
                #             r[2] = p[np.argmax(s)]
                #             d = np.diff(p, axis=1)
                #             r[1] = p[np.argmin(d)]
                #             r[3] = p[np.argmax(d)]
                #             (tl, tr, br, bl) = r
                #             wA = np.sqrt((tl[0] - tr[0]) **
                #                          2 + (tl[1] - tr[1])**2)
                #             wB = np.sqrt((bl[0] - br[0]) **
                #                          2 + (bl[1] - br[1])**2)
                #             maxW = max(int(wA), int(wB))
                #             hA = np.sqrt((tl[0] - bl[0]) **
                #                          2 + (tl[1] - bl[1])**2)
                #             hB = np.sqrt((tr[0] - br[0]) **
                #                          2 + (tr[1] - br[1])**2)
                #             maxH = max(int(hA), int(hB))
                #             ds = np.array(
                #                 [[0, 0], [maxW - 1, 0], [maxW - 1, maxH - 1], [0, maxH - 1]], dtype="float32")
                #             transformMatrix = cv2.getPerspectiveTransform(
                #                 r, ds)
                #             scan = cv2.warpPerspective(
                #                 gray, transformMatrix, (maxW, maxH))
                #             # T = threshold_local(
                #             #     scan, 21, offset=10, method="gaussian")
                #             # scanBW = (scan > T).astype("uint8") * 255

                #             # Drawing detected lines and intersection points on the original image
                #             for line in lr:
                #                 rho, theta = line
                #                 a = np.cos(theta)
                #                 b = np.sin(theta)
                #                 x0 = a * rho
                #                 y0 = b * rho
                #                 pt1 = (int(x0 + 1000 * (-b)),
                #                        int(y0 + 1000 * a))
                #                 pt2 = (int(x0 - 1000 * (-b)),
                #                        int(y0 - 1000 * a))
                #                 # cv2.line(frame, pt1, pt2, (0, 255, 0), 10)

                #             for pt in p:
                #                 cv2.circle(frame, tuple(pt),
                #                            30, (255, 0, 0), -1)

                    self.ai_crop = p

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(rgb_image, (2120, 1280))
            h, w, ch = frame_resized.shape
            bytes_per_line = ch * w
            q_img = QImage(frame_resized.data, w, h,
                           bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.parent_label.setPixmap(pixmap.scaled(
                self.parent_label.size(), Qt.KeepAspectRatio))
        else:
            # Display loader while camera is changing
            self.show_loader()

    def change_camera(self, camera_index):
        # Stop the timer if it's running
        if self.timer is not None:
            self.timer.stop()

        # Create a thread for camera switching (optional, but recommended for responsiveness)
        self.camera_change_thread = threading.Thread(
            target=self._change_camera_in_thread, args=(camera_index,))
        self.camera_change_thread.start()
        # Display loader immediately
        self.show_loader()

    def _change_camera_in_thread(self, camera_index):
        # Release the current video capture
        self.video.release()

        # Open the new camera capture
        self.video = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
        self.set_resolution()

        # Create a QTimer object and connect it to the display_camera_feed function (in main thread)
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_camera_feed1)
        self.timer.start(10)  # Start the timer with a 10ms interval

    def show_loader(self):
        font = QFont()
        font.setPointSize(30)
        self.parent_label.setFont(font)
        self.parent_label.setAlignment(Qt.AlignCenter)
        self.parent_label.setText(
            "<p style='font-size:20pt'>Changing Camera...</p>")

    def l_inter(self, line1, line2):
        r1, t1 = line1
        r2, t2 = line2
        A = np.array([[np.cos(t1), np.sin(t1)], [np.cos(t2), np.sin(t2)]])
        b = np.array([r1, r2])
        if abs(t1 - t2) > 1.3:
            return np.round(np.linalg.solve(A, b)).astype(int)
        return None

    def points_inter(self, lines):
        intersections = []
        for i, g in enumerate(lines[:-1]):
            for g2 in lines[i+1:]:
                inter_pt = self.l_inter(g, g2)
                if inter_pt is not None:
                    intersections.append(inter_pt)
        return intersections

    def update_frame(self):
        self.display_camera_feed1(self.checked)

    def toggle_contour_detection(self, checked):
        self.checked = checked

    def set_focus(self, index):
        # Simulate changing focus
        self.current_focus = (self.current_focus + 10) % 30
        print(f'Focus set to: {self.current_focus}')
        if index == 1:
            if self.current_focus >= 0 and self.current_focus < 20:
                self.video.set(cv2.CAP_PROP_FOCUS, self.current_focus)

        if index == 0:
            if self.current_focus == 20:
                self.video.set(cv2.CAP_PROP_AUTOFOCUS, 1)


    def detect_document(self,frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (1, 1), 0)
        edged = cv2.Canny(gray, 75, 200)
        # Apply morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        edged = cv2.dilate(edged, kernel, iterations=1)
        edged = cv2.erode(edged, kernel, iterations=1)
        contours, _ = cv2.findContours(
            edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                return approx

        return None
    
    
    def order_points(self,pts):
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        print("i")
        print(rect)
        return rect
