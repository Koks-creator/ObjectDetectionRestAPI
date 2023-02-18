from flask_restful import fields

detection_fields = {
    "image": fields.String,
    "model": fields.String,
    "detections": fields.List(fields.List(fields.Integer)),
    "confidence": fields.List(fields.Float),
    "classes": fields.List(fields.String),
}

model_info_field = {
    "Name": fields.String,
    "Classes": fields.List(fields.String),
    "Description": fields.String
}
