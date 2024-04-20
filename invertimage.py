
from PIL import Image
import cv2
# Open the image file
image1 = input("enter image location:")
#image = Image.open(image1)
#image.show()
# Display image properties
#print("Image format:", image.format)
#print("Image size:", image.size)
#print("Image mode:", image.mode)
#inverting a file
image = cv2.imread(image1)

    # Invert the image
inverted_image = cv2.bitwise_not(image)

# Create windows with image size
cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
cv2.namedWindow("Inverted Image", cv2.WINDOW_NORMAL)


    # Display the original and inverted images
cv2.imshow("Original Image", image)
cv2.imshow("Inverted Image", inverted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


''' response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": "You will be provided with unstructured data, and your task is to identify the insured name and address and display it seperately."
    },
    {
      "role": "user",
      "content": extracted_text
    }
  ],
  temperature=0,
  max_tokens=1000,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
) '''
