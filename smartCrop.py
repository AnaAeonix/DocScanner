from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np


class SmartCrop:
    def __init__(self, image, root, points=None):
        self.crop_pressed = False
        self.image_orig = image
        max_size = 720  # 1960x1080
        width, height = image.size
        print(image.size)
        # height, width = image.shape[:-1]
        scale_ratio = 0.5
        if max(width, height) > max_size:
            scale_ratio = max_size / float(max(width, height))
        new_width = int(width * scale_ratio)
        new_height = int(height * scale_ratio)
        image = image.resize((new_width, new_height))
        # image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        self.image = image
        self.inv_scaling_factor = 1/scale_ratio
        if points is not None:
            points = np.asarray(points)//self.inv_scaling_factor
        self.width, self.height = new_width, new_height
        self.POINT_RADIUS = 7
        self.POINT_COLOR = 'blue'

        # Create Tkinter window
        self.root = root
        self.root.title("Smart Crop")

        # Create canvas
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        # Display image on canvas
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_container = self.canvas.create_image(
            0, 0, anchor=NW, image=self.photo)

        if points is None:
            self.draggable_points = [{"x": 10, "y": 10}, {"x": self.width//2, "y": 10}, {"x": self.width - 10, "y": 10}, {
                "x": self.width - 10, "y": self.height - 10}, {"x": self.width//2, "y": self.height - 10}, {"x": 10, "y": self.height - 10}]
        else:
            self.draggable_points = [{'x': x, 'y': y} for x, y in points]
        self.pre = self.draggable_points.copy()
        self.polygon_id = self.canvas.create_polygon(
            [(item['x'], item['y']) for item in self.draggable_points], outline='#4788f7', width=2, fill='')

        for item in self.draggable_points:
            item['circle'] = self.canvas.create_oval(item['x'] - self.POINT_RADIUS, item['y'] - self.POINT_RADIUS,
                                                     item['x'] + self.POINT_RADIUS, item['y'] +
                                                     self.POINT_RADIUS,
                                                     fill=self.POINT_COLOR, tags='point')
            self.canvas.tag_bind(
                item['circle'], '<Button1-Motion>', lambda event, item=item: self.drag(event, item))
            
        style = ttk.Style()

        style.configure('TButton',
                        background='#4788f7',
                        foreground='#4788f7',
                        font=('Helvetica', 10, 'bold'),
                        borderwidth=1,
                        # padding=(10, 20)
                        padding=(5, 10))

        # Apply a hover effect (requires ttk 8.6+)
        style.map('TButton',
                  background=[('active', '#073c6d')])

        # Add Done and Reset buttons
        self.done_button = ttk.Button(self.root, text="Crop", style= 'TButton', command=self.crop)
        self.done_button.pack(side=LEFT, padx=5, pady=5)

        self.reset_button = ttk.Button(
            self.root, text="Reset", style='TButton', command=self.reset_points)
        self.reset_button.pack(side=LEFT, padx=5, pady=5)

        # # Add Rotate button
        # self.rotate_button = ttk.Button(
        #     self.root, text="Rotate", style='TButton', command=self.rotate_image)
        # self.rotate_button.pack(side=LEFT, padx=5, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def crop(self):
        self.crop_pressed = True

    def drag(self, event, item):
        x, y = event.x, event.y

        # Ensure new point position is within canvas boundaries
        item['x'] = max(min(x, self.width - self.POINT_RADIUS),
                        self.POINT_RADIUS)
        item['y'] = max(min(y, self.height - self.POINT_RADIUS),
                        self.POINT_RADIUS)

        self.canvas.coords(item['circle'], item['x'] - self.POINT_RADIUS, item['y'] - self.POINT_RADIUS,
                           item['x'] + self.POINT_RADIUS, item['y'] + self.POINT_RADIUS)

        # Update the polygon
        self.update_polygon()

    def update_polygon(self):
        self.canvas.coords(
            self.polygon_id, *sum([(point['x'], point['y']) for point in self.draggable_points], ()))

    def reset_points(self):
        # [0], self.draggable_points[1], self.draggable_points[2], self.draggable_points[3]
        A, P, B, C, Q, D = self.draggable_points
        A['x'], A['y'] = 10, 10
        P['x'], P['y'] = self.width//2, 10
        B['x'], B['y'] = self.width - 10, 10
        C['x'], C['y'] = self.width - 10, self.height - 10
        Q['x'], Q['y'] = self.width//2, self.height - 10
        D['x'], D['y'] = 10, self.height - 10

        for item in self.draggable_points:

            self.canvas.coords(item['circle'], item['x'] - self.POINT_RADIUS, item['y'] - self.POINT_RADIUS,
                               item['x'] + self.POINT_RADIUS, item['y'] + self.POINT_RADIUS)

        self.update_polygon()

    def rotate_image(self):
        # Rotate image by 90 degrees clockwise
        self.image = self.image.rotate(-90, expand=True)
        self.image_orig = self.image_orig.rotate(-90, expand=True)
        self.width, self.height = self.image.size
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.image_container, image=self.photo)
        self.canvas.config(width=self.width, height=self.height)
        self.reset_points()

    def get_draggable_points(self):
        return list(map(self.restore_coord, [(point['x'], point['y']) for point in self.draggable_points]))

    def run(self):
        self.root.mainloop()

    def restore_coord(self, point):  # ,x_crop_offset,y_crop_offset):
        x, y = point
        return (int(x * self.inv_scaling_factor), int(y * self.inv_scaling_factor))

    def get_warpped(self, corners):
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
        final1 = cv2.warpPerspective(np.array(self.image_orig), np.float32(
            homography1), (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)
        final2 = cv2.warpPerspective(np.array(self.image_orig), np.float32(
            homography2), (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)
        return final1, final2, np.concatenate((final1, final2), axis=1)

    # def get_stitched_wrapped(self,corners):
    #     img1 = self.get_warpped([corners[0],corners[1],corners[4],corners[5]])
    #     img2 = self.get_warpped([corners[1],corners[2],corners[3],corners[4]])
    #     return np.concatenate((img1,img2), axis=1)

    def on_closing(self):
        for itemA, itemB in zip(self.pre, self.draggable_points):
            itemB['x'] = itemA['x']
            itemB['y'] = itemA['y']
        self.root.destroy()


# def main():
#     image = Image.open(r"C:\Users\sdas\OneDrive\Desktop\aeonix\DocScanner\test.jpg")
#     obj = SmartCrop(image)
#     obj.run()
#     corners = obj.get_draggable_points()

#     split1,split2,warpped_image  = obj.get_warpped(corners)
#     cv2.imwrite("1714054747202_warpped_1.jpg",cv2.cvtColor(split1, cv2.COLOR_BGR2RGB))
#     cv2.imwrite("1714054747202_warpped_2.jpg",cv2.cvtColor(split2, cv2.COLOR_BGR2RGB))
#     cv2.imwrite("1714054747202_warpped.jpg",cv2.cvtColor(warpped_image, cv2.COLOR_BGR2RGB))
#     print(corners)

# if __name__ == "__main__":
#     main()
