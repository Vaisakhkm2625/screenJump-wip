import cv2
import numpy as np

# Read the screenshot image
screenshot = cv2.imread('winsome.png')
result = "hello.png"
# Convert the image to grayscale
gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

# Apply edge detection or other preprocessing techniques as needed
# For simplicity, we'll use Canny edge detection in this example
edges = cv2.Canny(gray, 50, 150)
#cv2.imwrite(result, result+"edge.png")


# Find contours in the edge-detected image
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a blank image to draw the bounding boxes and red dots
result_image = np.zeros_like(screenshot)
#:result_image = screenshot

# Iterate through the contours and draw bounding boxes
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    
    # Draw bounding box
    cv2.rectangle(result_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Calculate center point
    center_x = x + w // 2
    center_y = y + h // 2
    
    # Draw red dot at the center point
    cv2.circle(result_image, (center_x, center_y), 5, (0, 0, 255), -1)

# Display the result
#cv2.imshow('Result', result_image)

cv2.imwrite(result, result_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
