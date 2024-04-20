from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process_file', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file received.'}), 400

    file = request.files['file']

    # Perform your file processing and OCR here
    # For this example, we assume the data is already extracted
    extracted_data = {
        'name': 'John Doe',
        'address': '123 Main Street',
        'vehicleNumber': 'ABC123'
    }

    return jsonify(extracted_data)

if __name__ == '__main__':
    app.run()
