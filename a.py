import cv2
import numpy as np

def find_squares(image_path):
    # Read the input image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply GaussianBlur to reduce noise and help with contour detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use Canny edge detector to find edges
    edges = cv2.Canny(blurred, 50, 150)
    
    # Find contours in the edged image
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    squares = []

    for cnt in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # Check if the polygon has 4 vertices (approximately a square)
        if True: #len(approx) == 4:
            # Check if the area of the contour is large enough
            area = cv2.contourArea(approx)
            if area > 1000:  # Adjust this threshold based on your image
                squares.append(approx)
                
    return squares

def display_squares(image_path, squares):
    image = cv2.imread(image_path)
    
    # Draw the detected squares on the image
    for square in squares:
        cv2.polylines(image, [square], True, (0, 255, 0), 2)

    # Display the image with detected squares
    cv2.imshow('Detected Squares', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def draw_squares(image, squares):
    # Draw the detected squares on the image
    for square in squares:
        cv2.polylines(image, [square], True, (0, 255, 0), 2)

def save_image_with_squares(image_path, output_path, squares):
    image = cv2.imread(image_path)
    draw_squares(image, squares)
    
    # Save the image with detected squares
    cv2.imwrite(output_path, image)


if __name__ == "__main__":
    image_path = "./winsome.png"
    output_path = "hello.png"
    
    detected_squares = find_squares(image_path)
    print(f"Number of detected squares: {len(detected_squares)}")
    
    save_image_with_squares(image_path, output_path, detected_squares)
    print(f"Result saved to {output_path}")
