import PyPDF2
import openai
import os

#openai.api_key ='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'



def convert_pdf_to_text(pdf_path):
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    text = ""
    for page_number in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_number]
        text += page.extract_text()

    pdf_file.close()

    return text

# Specify the path to your PDF file
pdf_path = 'C:/Users/amits/AppData/Local/Temp/Temp11_Sample Files.zip/Sample Files/Policy/BajajAllianzMotor_TW_OG201904180600032196.pdf'

# Call the function to convert the PDF to text and print the extracted text
extracted_text = convert_pdf_to_text(pdf_path)
print(extracted_text)

response = openai.ChatCompletion.create(
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
)
# Extracting and printing the model response
model_response = response['choices'][0]['message']['content']
print("Model Response:")
print(model_response)
