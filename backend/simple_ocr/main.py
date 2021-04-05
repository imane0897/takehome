from flask import Flask, request
app = Flask(__name__)


@app.route('/ocr_image', methods=['POST'])
def ocr_image():
    image = request.files.get('image')
    print(image)

    get_letters = []
    letters = {'content': get_letters}
    return letters
