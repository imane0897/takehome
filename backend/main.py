from flask import Flask, request
from ocr_model.predict_ocr import predict_image
app = Flask(__name__)


@app.route('/ocr_image', methods=['POST'])
def ocr_image():
    # read image
    imgstr = request.files.get('image').read()

    # predict letters in image and return dict(JSON)
    get_letters = predict_image(imgstr)
    letters = {'content': get_letters}

    return letters
