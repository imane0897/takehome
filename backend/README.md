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
|  ├──3.png
|  └──4.png
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
docker-compose up
```

使用
```shell
cd backend
curl -F "image=@test_images/1.png" localhost:5000/ocr_image
```

## API

```shell
POST /ocr_image
```

## References
[1] [OCR with Keras, TensorFlow, and Deep Learning](https://www.pyimagesearch.com/2020/08/17/ocr-with-keras-tensorflow-and-deep-learning/)

[2] [OCR: Handwriting recognition with OpenCV, Keras, and TensorFlow](https://www.pyimagesearch.com/2020/08/24/ocr-handwriting-recognition-with-opencv-keras-and-tensorflow/)