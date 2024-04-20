import cv2
import os
def binarize_image(image_path):
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("Error: Failed to load the image.")
        return

    # Apply binary thresholding
    _, binary_image = cv2.threshold(image, 120, 250, cv2.THRESH_BINARY)

    cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Binary Image", cv2.WINDOW_NORMAL)
    # Display the original and binary images
    cv2.imshow("Original Image", image)
    cv2.imshow("Binary Image", binary_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = input("enter image location:")


binarize_image(image_path)