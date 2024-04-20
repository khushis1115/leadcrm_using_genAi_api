import pytesseract
import cv2
from PIL import Image
import openai

#openai.api_key ='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'

image1 = input("enter image location:")

img = cv2.imread(image1)
_, binary_image = cv2.threshold(img, 120, 250, cv2.THRESH_BINARY)

cv2.namedWindow("hi", cv2.WINDOW_NORMAL)

cv2.imshow("hi", binary_image)

cv2.waitKey(0)
cv2.destroyAllWindows()

ocr_result = pytesseract.image_to_string(binary_image)
with open("ocr_result.txt", "w") as file:
    file.write(ocr_result)
print(ocr_result)

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": "You will be provided with unstructured data, and your task is to identify the insured name and address and display it seperately."
    },
    {
      "role": "user",
      "content": ocr_result
    }
  ],
  temperature=0,
  max_tokens=1000,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)
# Extracting and printing the model response
model_response = response['choices'][0]['message']['content']
print("Model Response:")
print(model_response)

#doc = nlp(ocr_result)
#print(doc)



