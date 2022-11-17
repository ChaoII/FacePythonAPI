import requests
from utils import *


def face_recognize(imgpath):
    url = "http://127.0.0.1:9026/face_recognize"
    img = cv2.imread(imgpath)
    image = image_to_base64(img)
    data = {"imageBase64": image}
    ret = requests.post(url=url, json=data)
    print(ret.json())


if __name__ == '__main__':
    face_recognize("./asserts/123.jpg")
