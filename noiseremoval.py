import cv2

def remove_noise(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Apply removal blur
    inv = cv2.bitwise_not(image)
    gray = cv2.cvtColor(inv, cv2.COLOR_BGR2GRAY)
    #_, thresholded = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    dilated = cv2.dilate(gray, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)
    morphed = cv2.morphologyEx(eroded, cv2.MORPH_OPEN, kernel)
    denoised = cv2.medianBlur(morphed, 1)
    inverted_image = cv2.bitwise_not(denoised)

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # enh = cv2.equalizeHist(gray)
    # blur = cv2.GaussianBlur(enh,(5,5),1.5)
    # dilate = cv2.dilate(blur,(3,3),2)
    # denoise= cv2.fastNlMeansDenoising(dilate,10)
    # canny = cv2.Canny(gray,125,175)

    cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Denoised Image", cv2.WINDOW_NORMAL)

    # Display the original and denoised images
    cv2.imshow("Original Image", image)
    cv2.imshow("Denoised Image", inverted_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = input("enter image location:")

denoised_image = remove_noise(image_path)

ocr_result = pytesseract.image_to_string(denoised_image)
print(ocr_result)