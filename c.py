import cv2
import numpy as np

def find_buttons(image_path):
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
    
    buttons = []

    for cnt in contours:
        # Approximate the contour to a polygon
        epsilon = 0.04 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # Check if the polygon has 4 vertices (approximately a rectangle)
        if len(approx) == 4:
            # Check if the aspect ratio is close to 1 (to approximate a square)
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            if 0.8 <= aspect_ratio <= 1.2:
                buttons.append(approx)
                
    return buttons

def draw_buttons(image, buttons):
    # Draw the detected buttons on the image
    for button in buttons:
        cv2.polylines(image, [button], True, (0, 255, 0), 2)

def save_image_with_buttons(image_path, output_path, buttons):
    image = cv2.imread(image_path)
    draw_buttons(image, buttons)
    
    # Save the image with detected buttons
    cv2.imwrite(output_path, image)

if __name__ == "__main__":
    image_path = "./out.png"
    output_path = "./hello.png"
    
    detected_buttons = find_buttons(image_path)
    print(f"Number of detected buttons: {len(detected_buttons)}")
    
    save_image_with_buttons(image_path, output_path, detected_buttons)
    print(f"Result saved to {output_path}")
