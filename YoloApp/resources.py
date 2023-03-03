from flask_restful import Resource, abort, marshal_with
import cv2
import base64
import numpy as np

from ApiYoloDetector.YoloApp.detector import Detector
from ApiYoloDetector.YoloApp import models_list, models_info, model_files
from ApiYoloDetector.YoloApp.fields import detection_fields, model_info_field
from ApiYoloDetector.YoloApp.parsers import detection_parser, model_info_parser


class DetectionListModels(Resource):
    def get(self):
        models_available = {}

        for i, model in enumerate(models_list):
            models_available[i] = model

        return {"models": models_available}, 200


class Detection(Resource):
    @marshal_with(model_info_field)
    def get(self):
        model_id = model_info_parser.parse_args()["modelId"]
        if model_id not in models_info.keys():
            abort(404, message=f"There is no model with id {model_id}. Check models list using"
                               f" /detection/listModels get method")

        return models_info[model_id], 200

    @marshal_with(detection_fields)
    def post(self):
        img_stream, model_id, allowed_classes, confidence_threshold, nms_threshold = detection_parser.parse_args().values()

        if model_id not in models_info.keys():
            abort(404, message=f"There is no model with id {model_id}. Check models list using"
                               f" /detection/listModels get method")

        detector = Detector(
            weights_file_path=model_files[model_id]["weights"],
            config_file_path=model_files[model_id]["config"],
            classes_file_path=model_files[model_id]["classes"],
            confidence_threshold=confidence_threshold,
            nms_threshold=nms_threshold
        )

        if allowed_classes is None:
            allowed_classes = False
        else:
            classes_available = models_info[model_id]["Classes"]
            if not all(item in classes_available for item in allowed_classes):
                abort(404, message="This class id is not available")

        stream = img_stream.read()
        np_img = np.frombuffer(stream, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_UNCHANGED)

        if img is None:
            abort(404, message=f"Failed to process your file, make sure this file is an image")

        detections = detector.detect(img, allowed_classes=allowed_classes)

        detections_response = []
        confidence_response = []
        classes_response = []
        for detection in detections:
            x1, y1 = detection.x, detection.y
            x2, y2 = detection.x + detection.w, detection.y + detection.h

            detections_response.append([x1, y1, detection.w, detection.h])
            confidence_response.append(round(detection.detections_conf, 2))
            classes_response.append(detection.class_name)

            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.putText(img, f"{detection.class_name} {int(round(detection.detections_conf, 2) * 100)}%",
                        (x1, y1 - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        del detector  # not sure if it's needed

        retval, buffer = cv2.imencode('.jpg', img)
        jpg_as_text = base64.b64encode(buffer)

        return {"image": jpg_as_text.decode("utf-8"),
                "model": model_files[model_id]["name"],
                "detections": detections_response,
                "confidence": confidence_response,
                "classes": classes_response}, 200
