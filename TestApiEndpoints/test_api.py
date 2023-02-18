import requests


MODELS_LIST = ['BasketBallModel', 'KoalaModel', 'VehiclesModel', 'Yolov4']
MODELS_INFO = {0: {'Name': 'BasketBallModel', 'Classes': ['Basket ball', 'Basket'], 'Description': 'Model for detecting baskets and basketballs.'},
               1: {'Name': 'KoalaModel', 'Classes': ['koala'], 'Description': 'Model for detecting koalas.'},
               2: {'Name': 'VehiclesModel', 'Classes': ['car', 'truck', 'bus'], 'Description': 'Model for detecting buses, cars and trucks.'},
               3: {'Name': 'Yolov4', 'Classes': ['person', 'bicycle', 'car', 'motorbike', 'aeroplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'sofa', 'pottedplant', 'bed', 'diningtable', 'toilet', 'tvmonitor', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'], 'Description': 'Model for general use (81 classes).'}}
BASE_URL = "http://127.0.0.1:5000"


def test_list_models():
    resp = requests.get(f"{BASE_URL}/detection/listModels")
    data = resp.json()

    for model in data["models"].values():
        assert model in MODELS_LIST, f"Model {model} not found in {MODELS_LIST}"


def test_model_info():
    for index, model_name in enumerate(MODELS_LIST):
        response = requests.get(f"{BASE_URL}/detection", data={"modelId": index})
        data = response.json()

        assert data["Name"] == MODELS_INFO[index]["Name"],\
            f"Model name {model_name} do not match {MODELS_INFO[index]['Name']}"
        assert len(data["Classes"]) == len(MODELS_INFO[index]["Classes"]), \
            f"Amount of classes in {model_name} model do not match ({len(data['Classes'])}" \
            f" != {len(MODELS_INFO[index]['Classes']),}"


def test_model_detection():
    files = {'file': open(r'2.jpg', 'rb')}
    response = requests.post(f"{BASE_URL}/detection", files=files, data={"modelId": 2})
    data = response.json()

    assert len(data["detections"]) != 0, "There is no detections"




