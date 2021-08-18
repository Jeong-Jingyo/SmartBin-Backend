from flask import Flask, request, Response
import cv2
import numpy as np
import importlib
import importlib
import json
detector = importlib.import_module("SmartBin-Detector")
classifier = importlib.import_module("SmartBin-Classifier")
app = Flask(__name__)

Classifier = classifier.Classifier()
petDetector = detector.Detector("pet")


@app.route('/ai', methods=['POST'])
def mainAPI():
    image_file = request.files['file']
    image_array = np.asarray(bytearray(image_file.read()), dtype=np.uint8)

    classification = Classifier.classify(image_array)
    classification = classification.tolist()[0]

    detection = petDetector.detect(image_array)

    body = {"trashType": classification, "foreignSubst": detection}
    body = json.dumps(body)

    return Response(body, mimetype="application/javascript")


@app.route('/ai')
def main():
    return '<html><body><form action = "http://localhost:5000/ai" method = "POST"'\
         'enctype = "multipart/form-data"><input type = "file" name = "file" />'\
         '<input type = "submit"/></form></body></html>'


app.run(debug=False)
