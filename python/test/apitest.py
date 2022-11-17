import requests
from utils import *


def test_register_face_api(id_, name, img):
    # ============test register_face api============
    url = "http://127.0.0.1:10054/register_face"
    # id_ = str(uuid.uuid4()).replace("-")
    id_ = id_
    name = name
    img = cv2.imread(img)
    image = image_to_base64(img)
    data = {"uid": id_, "name": name, "image": image}
    ret = requests.post(url=url, json=data)
    print(ret.json())


def test_delete_face(id_: str):
    # ============test delete_face api============
    url = "http://127.0.0.1:10054/delete_face"
    data = {"uid": id_}
    ret = requests.delete(url=url, json=data)
    print(ret.json())
    # ============test face_recognize api============


def test_face_recognize(imgpath):
    url = "http://192.168.1.149:9026/face_recognize"
    img = cv2.imread(imgpath)
    image = image_to_base64(img)
    data = {"imageBase64": image}
    ret = requests.post(url=url, json=data)
    print(ret.json())


def test_get_face_library(id_=None):
    url = "http://127.0.0.1:10054/get_face_library"
    data = {'uid': id_}
    if id_ is None:
        data = {}
    print(data)
    ret = requests.post(url=url, json=data)
    print(ret.json())


if __name__ == '__main__':
    # test_register_face_api('01', '成龙', './asserts/1.jpg')
    # test_register_face_api('02', '艾超', './asserts/aichao.jpg')
    # test_register_face_api('03', '刘德华', './asserts/liudehua.jpg')
    # test_register_face_api('04', '佟大为', './asserts/tongdawei.jpg')
    # test_register_face_api('06', '奥沫沫', './asserts/oumei.jpg')

    test_face_recognize('./asserts/123.jpg')
    # test_delete_face('04')
    # test_get_face_library('04')
