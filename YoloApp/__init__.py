import os
import glob
from flask import Flask
from flask_restful import Api

from ApiYoloDetector.YoloApp.config import Config


name_mapping = {
    ".txt": "classes",
    ".cfg": "config",
    ".weights": "weights"
}

model_files = {}
conf = Config()
models_list = os.listdir(conf.MODELS_PATH)

for index, model in enumerate(models_list):
    files = glob.glob(rf"{conf.MODELS_PATH}/{model}/*.*")

    model_files[index] = {}
    model_files[index]["name"] = model

    for file in files:
        _, ext = os.path.splitext(file)
        model_files[index][name_mapping[ext]] = file

models_info = {}
classes = []
descriptions = ["Model for detecting baskets and basketballs.",
                "Model for detecting koalas.",
                "Model for detecting buses, cars and trucks.",
                "Model for general use (81 classes)."]

for item in model_files.values():
    with open(item['classes']) as f:
        classes.append(f.read().splitlines())


for index, model_name in enumerate(os.listdir(conf.MODELS_PATH)):
    models_info[index] = {
        "Name": model_name,
        "Classes": classes[index],
        "Description": descriptions[index],
    }


from ApiYoloDetector.YoloApp.resources import Detection, DetectionListModels


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Detection, "/detection")
    api.add_resource(DetectionListModels, "/detection/listModels")

    return app
