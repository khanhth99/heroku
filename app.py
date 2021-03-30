import base64
import json
import pytesseract
from flask import Flask, jsonify, request #import objects from the Flask model
app = Flask(__name__) #define app using Flask
from PIL import Image
from io import BytesIO
from detectTextInImage import detectText

# languages = []
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

@app.route('/', methods=['GET'])
def test():
	return jsonify({'message' : 'It works!'})

@app.route('/lang', methods=['GET'])
def returnAll():
	y = json.dumps(languages)
	for i in languages:
		im = Image.open(BytesIO(base64.b64decode(i['imageBase64'])))
		im.save('image1.png', 'PNG')
	return y

@app.route('/lang', methods=['POST'])
def addOne():
	# languages = {}
	imageBase64 = request.json['imageBase64']
	# imageBase64 = request.values.get('imageBase64')
	idUser = request.json['idUser']
	# img = Image.open(BytesIO(base64.b64decode(imageBase64)))
	result = detectText(imageBase64)
	# boxes = pytesseract.image_to_string(img,lang='eng')
	# return request.json['idUser']
	# result = result.split("\n")
	# print(result, sep="\n")

	result = json.dumps(result.split("\n"))
	result = json.loads(result)
	for i in result:
		if (i == ''):
			result.remove('')
		elif (i == ' '):
			result.remove(' ')
		elif (i == '  '):
			result.remove('  ')
		elif (i == '  '):
			result.remove('  ')

	print(type(result))
	print(result)
	return json.dumps(result)

if __name__ == '__main__':
  app.run(debug=True, port=11799)