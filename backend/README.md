# Backend Projects


## Directory structure

```plain
.
├──ocr_model
│  ├──__init__.py
│  ├──a-z_dataset.py
│  ├──predict_ocr.py
│  ├──train_ocr_model.py
│  └──ocr.model
│
├──test_images
|  ├──1.png
|  ├──2.png
|  └──3.png
│
├──main.py
|
├──database.db
│
├──Dockerfile
│
└──requirements.txt
```

## Usage

部署
```shell
cd backend
export FLASK_APP=main.py
flask run
```

使用
```shell
cd backend
curl -F "image=@test_images/1.png" localhost:5000/ocr_image
[GET] localhost:5000/get_predictions?hash_digest=[hash_digest]
```

## API

```shell
POST /upload_image
GET /get_predictions?hash_digest=[hash_digest]
```

## References
[1] [OCR with Keras, TensorFlow, and Deep Learning](https://www.pyimagesearch.com/2020/08/17/ocr-with-keras-tensorflow-and-deep-learning/)

[2] [OCR: Handwriting recognition with OpenCV, Keras, and TensorFlow](https://www.pyimagesearch.com/2020/08/24/ocr-handwriting-recognition-with-opencv-keras-and-tensorflow/)