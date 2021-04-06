import os
import hashlib
import queue
import sqlite3
import threading
from flask import Flask, request, g
from ocr_model.predict_ocr import predict_image

app = Flask(__name__)
DATABASE = os.getcwd() + '/database.db'
PREDICT_QUEUE = queue.Queue()


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


@app.route('/upload_image', methods=['POST'])
def upload_image():
    """
    Receive image POST from clients.
    :return: sha256 hash digest of the image
    """
    imgstr = request.files.get('image').read()
    hash_digest = hashlib.sha256(imgstr).hexdigest()
    if not find_predictions(hash_digest):
        PREDICT_QUEUE.put(imgstr)
    return hash_digest, 202


def find_predictions(hash_digest):
    """
    Query sqlite, caculate new predictions and insert it 
    to sqlite when it's not in.
    """
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM image WHERE id=?", (hash_digest,))
    rows = cur.fetchall()
    return True if rows else False


@app.route('/get_predictions', methods=['GET'])
def get_predictions():
    """
    Query sqlite and return predictions when it's ready
    or return error if the predictions are not completed.
    """
    hash_digest = request.args.get('hash_digest')

    # query sqlite
    cur = get_db().cursor()
    cur.execute("SELECT * FROM image WHERE id=?", (hash_digest,))
    rows = cur.fetchall()

    # if predictions exist
    if rows:
        letters = rows[0][1]
        preds = {'content': list(letters)}
        return preds, 200
    else:
        return {"msg": "Please wait for a second and retry."}, 423


def predict():
    db = sqlite3.connect(DATABASE)
    while True:
        if not PREDICT_QUEUE.empty():
            imgstr = PREDICT_QUEUE.get()
            # predict letters in image and save in dict
            preds = predict_image(imgstr)

            # save image and prediction in sqlite
            sql_insert_image = '''
                                INSERT INTO image (id, letters) VALUES (?, ?)
                                '''
            db.cursor().execute(sql_insert_image,
                                (hashlib.sha256(imgstr).hexdigest(), 
                                ''.join(preds)))
            db.commit()


def setup_app(app):
    """
    Set up at the start of the server.
    :param app: this Flask app
    """
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

    # a background thread to handle the prediction process
    threading.Thread(target=predict, daemon=True).start()


setup_app(app)
