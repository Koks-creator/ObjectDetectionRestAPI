import requests
import cv2
import numpy as np
import base64

resp = requests.get("http://127.0.0.1:5000/detection/listModels")
data = resp.json()
print(data)

resp = requests.get("http://127.0.0.1:5000/detection", data={"modelId": 2})
data = resp.json()
print(data)


files = {"file": open(r"images/RzucanieDoKosza2_122.jpg", "rb")}
resp = requests.post("http://127.0.0.1:5000/detection", files=files, data={"modelId": 0})
data = resp.json()
print(data)

encoded = data["image"].encode('ascii')
decoded = base64.b64decode((encoded))
nparr = np.frombuffer(decoded, np.uint8)
img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)


for detection in data["detections"]:
    x1, y1 = detection[0], detection[1]
    x2, y2 = x1 + detection[2], y1 + detection[3]

    cv2.rectangle(img_np, (x1, y1), (x2, y2), (0, 0, 255), 3)
    print(detection)

cv2.imshow("res", img_np)
cv2.waitKey(0)
