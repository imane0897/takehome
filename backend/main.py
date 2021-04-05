import os
import hashlib
import sqlite3
from flask import Flask, request, g
from ocr_model.predict_ocr import predict_image

app = Flask(__name__)
DATABASE = os.getcwd() + '/database.db'
print(DATABASE)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/ocr_image', methods=['POST'])
def ocr_image():
    # read image and hash it with sha256
    imgstr = request.files.get('image').read()
    hash_digest = hashlib.sha256(imgstr).hexdigest()

    # predict letters in image and save in dict
    get_letters = predict_image(imgstr)
    letters = {'content': get_letters}

    # save image and prediction in sqlite
    sql_insert_image = '''INSERT INTO image (id, letters) VALUES (?, ?)'''
    db = get_db()
    db.cursor().execute(sql_insert_image, 
                        (hash_digest, ''.join(get_letters)))
    db.commit()

    return letters


def setup_app(app):
    # create table to save image and predictions
    sql_create_image_table = '''CREATE TABLE IF NOT EXISTS image(
                                id VARCHAR(64) PRIMARY KEY,
                                letters TEXT
                                );'''
    try:
        db = get_db()
        db.cursor().execute(sql_create_image_table)
        db.commit()
    except Exception as e:
        print(e)


setup_app(app)
