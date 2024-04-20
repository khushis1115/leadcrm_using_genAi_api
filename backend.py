import fitz
import PyPDF2
import pytesseract
import os
from PIL import ImageEnhance
import numpy as np
from PIL import Image
import cv2
import openai

openai.api_key ='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'
file_name = input("Enter the file name: ")

if file_name.lower().endswith(".pdf"):
    #print("The file is a PDF.")
    pdf_document = fitz.open(file_name)

    has_text = False
    has_images = False

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text = page.get_text("text")

        if len(text.strip()) > 200:
            has_text = True
        else:
            images = page.get_images(full=True)
            if images:
                has_images = True

    pdf_document.close()

    if has_text:
        #print("The PDF contains text content.")


        def convert_pdf_to_text(file_name):
            pdf_file = open(file_name, 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            text = ""
            for page_number in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_number]
                text += page.extract_text()

            pdf_file.close()

            return text


        extracted_text = convert_pdf_to_text(file_name)
        #print(extracted_text)

    else:
        #print("The PDF contains scanned images.")

        # Open the PDF file
        pdf = fitz.open(file_name)

        for page_num in range(pdf.page_count):
            page = pdf[page_num]

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
            img_gray = enhanced_img.convert('L')

            # Perform OCR using pytesseract
            extracted_text = pytesseract.image_to_string(img_gray)
            #print(extracted_text)




elif file_name.lower().endswith((".jpeg", ".jpg")):

    #print("The file is an image.")
    image = cv2.imread(file_name)

    # Get the dimensions of the image
    height, width, channels = image.shape

    # Calculate the desired dimensions for enhancement
    new_width = width * 4
    new_height = height * 4

    # Resize the image using OpenCV
    enhanced_resolution = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)

    # Convert the image to grayscale using OpenCV
    grayscale_image = cv2.cvtColor(enhanced_resolution, cv2.COLOR_BGR2GRAY)

    # Apply Binary Threshold using OpenCV
    _, binary_image = cv2.threshold(grayscale_image, 120, 255, cv2.THRESH_BINARY)

    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Image", binary_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Perform OCR using pytesseract
    extracted_text = pytesseract.image_to_string(binary_image)
    #print(extracted_text)




else:
    print("Unsupported file format.")

# Maximum token limit (4090 tokens)
MAX_TOKENS = 4090
# Truncate user input if it exceeds the maximum token limit
user_input_truncated = extracted_text[:MAX_TOKENS]

#openai.api_key ='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'
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": "You will be provided with unstructured data, and your task is to identify whether it is a policy document, rc document or driving license. Once identified, extract the following: If its a policy document, then extracts the Policy No., Start Date, Expiry Date, Issue Date, Insured Name, Insured Address, Nominee Name, Nominee Relation, Vehicle Make, Vehicle Model, Vehicle Variant, Vehicle CC, Vehicle Seating Capacity, Vehicle Year of Manufacture, Vehicle Registration Date, Vehicle Fuel Type, Vehicle RTO (MH05, MH01, etc), Vehicle Chassis No, Vehicle Engine No, Vehicle Registration No, LPG/CNG Kit Installed, LPG/CNG Value, Electronic Accessories Value, Non-Electronic Accessories Value, Vehicle IDV, Hypothecation, Basic Own Damage Premium, Non-Elec. Accessories Premium, Elec. Accessories (IMT-24) Premium, CNG / LPG Kit (IMT-25) Premium, Zero/Nil Depreciation Add-on Premium, No Claim Bonus, Net Own Damage Premium (A), Basic Third Party Liability Premium, Third Party Liability For Bi-Fuel Kit Premium, PA Cover For Owner Driver (IMT-15) Premium, PA Paid Driver Premium, PA Cover For Unnamed Persons (IMT-16) Premium, Legal liability Paid Driver (IMT-28) Premium, Legal liability Unnamed Persons (IMT-29) Premium, Net Liability Premium (B), Total Premium (A+B), Total GST, Gross Premium, Insurer Name (might be difficult to read), Plan/Product Name (might be difficult to read), Payment Ref No., Payment Mode. If its a driving license document, then extracts the Insured Name, Insured Address, Insured Address Pincode, Insured DOB. If its a driving license document, then extract the Vehicle Registration No, Vehicle Type, Vehicle Chassis No, Vehicle Month & Year of Manufacture, Vehicle Fuel Type, Vehicle Registration Date, Vehicle Model, Vehicle Color, Vehicle Engine No, Vehicle CC, Insured Name, Insured Address, First Insurer Name (not sure if Insurer Name gets updated in digital RC), First Policy No (not sure if Policy No gets updated in digital RC), First Policy Expiry Date (not sure if Expiry Date gets updated in digital RC). In case it isnt found leave that title empty."
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
)
# Extracting and printing the model response
model_response = response['choices'][0]['message']['content']
print("Model Response:")
print(model_response)