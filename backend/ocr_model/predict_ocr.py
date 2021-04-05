from tensorflow.keras.models import load_model
from imutils.contours import sort_contours
import numpy as np
import argparse
import imutils
import cv2


def predict_image(file_path):
    """
    Used to be called externally to OCR letters from image.

    :param file_path: file path of the image to be OCR(ed)
    :return: list of letter strings
    """
    preds = predict(file_path)
    return get_predictions(preds)


def predict(file_path):
    """
    Read image, pre-process, predict with trained Tensorflow model.

    :param file_path: file path of image
    :return: list of predictions in floats
    """
    model = load_model('ocr.model')
    image = cv2.imread(file_path)

    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # edge detection
    edged = cv2.Canny(blurred, 30, 150)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sort_contours(cnts, method="left-to-right")[0]

    chars = []

    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(c)

        # filter out bounding boxes, ensuring they are neither too small
        # nor too large
        if (w >= 5 and w <= 150) and (h >= 15 and h <= 120):
            roi = gray[y:y + h, x:x + w]
            thresh = cv2.threshold(roi, 0, 255,
                          cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            (tH, tW) = thresh.shape

            # if the width is greater than the height, resize along the
            # width dimension
            if tW > tH:
                thresh = imutils.resize(thresh, width=32)

            # otherwise, resize along the height
            else:
                thresh = imutils.resize(thresh, height=32)

            # re-grab the image dimensions to be 32x32
            (tH, tW) = thresh.shape
            dX = int(max(0, 32 - tW) / 2.0)
            dY = int(max(0, 32 - tH) / 2.0)

            padded = cv2.copyMakeBorder(thresh, top=dY, bottom=dY,
                               left=dX, right=dX, borderType=cv2.BORDER_CONSTANT,
                               value=(0, 0, 0))
            padded = cv2.resize(padded, (32, 32))
            padded = padded.astype("float32") / 255.0
            padded = np.expand_dims(padded, axis=-1)

            # update our list of characters that will be OCR'd
            chars.append((padded, (x, y, w, h)))

    # extract the bounding box locations and padded characters
    boxes = [b[1] for b in chars]
    chars = np.array([c[0] for c in chars], dtype="float32")

    # OCR the characters using our handwriting recognition model
    return model.predict(chars)
    

def get_predictions(preds):
    """
    Get predictions of letters according to the caculations of Tensorflow trained model.

    :param preds: predictions in floats
    :return: list of predictions in letter
    """
    # define the list of label names
    labelNames = "0123456789"
    labelNames += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    labelNames = [l for l in labelNames]

    # return list of the predictions with labelNames
    pred_list = [labelNames[np.argmax(pred)] for pred in preds]
    return pred_list


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True, 
                    help="path to input image")
    args = vars(ap.parse_args())
    print(predict_image(args["image"]))
