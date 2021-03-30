# import base64
# import json
# import pytesseract
from flask import Flask, jsonify, request #import objects from the Flask model
app = Flask(__name__) #define app using Flask
# from PIL import Image
# from io import BytesIO
# from detectTextInImage import detectText

# languages = []
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

@app.route('/', methods=['GET'])
def test():
	return jsonify({'message' : 'It works!'})

if __name__ == '__main__':
  app.run(debug=True, port=11799)