import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

class ImageProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        self.epsilon_slider = tk.Scale(root, from_=0, to=1, resolution=0.01, label="Epsilon", orient=tk.HORIZONTAL)
        self.epsilon_slider.set(0.04)
        self.epsilon_slider.pack(pady=10)

        self.aspect_ratio_slider = tk.Scale(root, from_=0, to=5, resolution=0.1, label="Aspect Ratio", orient=tk.HORIZONTAL)
        self.aspect_ratio_slider.set(1.0)
        self.aspect_ratio_slider.pack(pady=10)

        self.area_threshold_slider = tk.Scale(root, from_=0, to=2000, label="Area Threshold", orient=tk.HORIZONTAL)
        self.area_threshold_slider.set(500)
        self.area_threshold_slider.pack(pady=10)

        self.load_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=10)

        self.process_button = tk.Button(root, text="Process Image", command=self.process_image)
        self.process_button.pack(pady=10)

        self.canvas = tk.Canvas(root)
        self.canvas.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.image_path = file_path
            image = Image.open(file_path)
            photo = ImageTk.PhotoImage(image)
            self.canvas.config(width=photo.width(), height=photo.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo

    def find_buttons_and_boxes(self, epsilon, aspect_ratio, area_threshold):
        # Read the input image
        image = cv2.imread(self.image_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding to deal with variations in lighting
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Use Canny edge detector to find edges
        edges = cv2.Canny(thresh, 50, 150)

        # Find contours in the edged image
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        buttons_and_boxes = []

        for i, cnt in enumerate(contours):
            # Approximate the contour to a polygon
            epsilon = epsilon * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            # Check if the polygon has a specific number of vertices
            if 4 <= len(approx) <= 8:
                # Check if the aspect ratio of the bounding rectangle is within a certain range
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio_calc = w / float(h)
                if aspect_ratio <= aspect_ratio_calc <= 1.0/aspect_ratio:
                    # Check if the area of the contour is large enough
                    area = cv2.contourArea(approx)
                    if area > area_threshold:
                        buttons_and_boxes.append((i + 1, approx, (x, y)))

            return buttons_and_boxes

    def process_image(self):
        if not hasattr(self, 'image_path'):
            messagebox.showwarning("Warning", "Please load an image first.")
            return

        epsilon = self.epsilon_slider.get()
        aspect_ratio = self.aspect_ratio_slider.get()
        area_threshold = self.area_threshold_slider.get()

        # Process the image using the specified parameters
        detected_elements = self.find_buttons_and_boxes(epsilon, aspect_ratio, area_threshold)

        # Display the processed image
        processed_image = self.draw_elements(detected_elements)
        self.display_processed_image(processed_image)

        # Print element positions
        self.print_element_positions(detected_elements)


    def draw_elements(self, elements):
        # Draw the detected elements on the image
        processed_image = cv2.imread(self.image_path)

        for label, element, _ in elements:
            cv2.polylines(processed_image, [element], True, (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(processed_image, str(label), (element[0][0][0], element[0][0][1]), font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)

        return processed_image

    def display_processed_image(self, processed_image):
        processed_image = Image.fromarray(processed_image)
        photo = ImageTk.PhotoImage(processed_image)
        self.canvas.config(width=photo.width(), height=photo.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

    def print_element_positions(self, elements):
        print("Label\tX\tY")
        for label, _, (x, y) in elements:
            print(f"{label}\t{x}\t{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessor(root)
    root.mainloop()

