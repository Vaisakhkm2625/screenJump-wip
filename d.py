import cv2
import numpy as np

def find_buttons_and_boxes(image_path):
    # Read the input image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding to deal with variations in lighting
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Use Canny edge detector to find edges
    edges = cv2.Canny(thresh, 50, 150)
    
    # Find contours in the edged image
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    buttons_and_boxes = []

    for cnt in contours:
        # Approximate the contour to a polygon
        epsilon = 0.04 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # Check if the polygon has a specific number of vertices
        if 4 <= len(approx) <= 8:
            # Check if the aspect ratio of the bounding rectangle is within a certain range
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            if 0.5 <= aspect_ratio <= 2.0:
                buttons_and_boxes.append(approx)
                
    return buttons_and_boxes

def draw_elements(image, elements):
    # Draw the detected elements on the image
    for element in elements:
        cv2.polylines(image, [element], True, (0, 255, 0), 2)

def save_image_with_elements(image_path, output_path, elements):
    image = cv2.imread(image_path)
    draw_elements(image, elements)
    
    # Save the image with detected elements
    cv2.imwrite(output_path, image)

if __name__ == "__main__":
    image_path = "./out.png"
    output_path = "./hello.png"
    
    detected_elements = find_buttons_and_boxes(image_path)
    print(f"Number of detected elements: {len(detected_elements)}")
    
    save_image_with_elements(image_path, output_path, detected_elements)
    print(f"Result saved to {output_path}")
