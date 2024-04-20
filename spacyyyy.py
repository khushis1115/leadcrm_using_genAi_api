import pytesseract
import os
from PIL import ImageEnhance
import numpy as np
import fitz
from PIL import Image
import cv2
import openai

#openai.api_key ='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'



# Specify the path to the PDF file
pdf_path = 'C:/Users/amits/AppData/Local/Temp/Temp13_Sample Files.zip/Sample Files/Policy/ICICI Lombard.pdf'

# Open the PDF file
pdf = fitz.open(pdf_path)

# Convert each page to an image and perform OCR
for page_num in range(pdf.page_count):
    page = pdf.load_page(page_num)

    # Get the default resolution (usually 72 DPI)
    default_resolution = 72

    # Get the dimensions of the page
    width = int(page.rect.width)
    height = int(page.rect.height)

    # Calculate the desired DPI based on the maximum dimension of the page
    max_dimension = max(width, height)
    dpi = int(max_dimension / 8)  # Adjust the divisor as needed

    # Render the page as an image with the desired resolution
    pix = page.get_pixmap(matrix=fitz.Matrix(dpi / default_resolution, dpi / default_resolution))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Enhance the image resolution
    enhanced_img = img.resize((img.width * 4, img.height * 4), resample=Image.LANCZOS)

    # Enhance image contrast
    enhancer = ImageEnhance.Contrast(enhanced_img)
    enhanced_img = enhancer.enhance(2.0)

    # Convert the enhanced image to grayscale
    img_gray = img.convert('L')

    # Perform binarization using OpenCV
    #_, binary_img = cv2.threshold(np.array(img_gray), 120, 255, cv2.THRESH_BINARY)

    ocr_result = pytesseract.image_to_string(enhanced_img)
    with open("ocr_result.txt", "w") as file:
        file.write(ocr_result)
    print(ocr_result)

    # Display the image
    enhanced_img.show()

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
