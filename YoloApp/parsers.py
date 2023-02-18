from flask_restful import reqparse
import werkzeug

detection_parser = reqparse.RequestParser()
detection_parser.add_argument("file", type=werkzeug.datastructures.FileStorage,
                    location="files",
                    required=True,
                    help="provide a file")
detection_parser.add_argument("modelId", type=int, location="form", required=True, help="provide a model id")
detection_parser.add_argument('allowedClasses', type=int, action="append", location='form')
detection_parser.add_argument('confidenceThreshold', type=float, location='form', default=.5)
detection_parser.add_argument('nmsThreshold', type=float, location='form', default=.5)

model_info_parser = reqparse.RequestParser()
model_info_parser.add_argument("modelId", type=int, location="form", required=True, help="provide a model id")
