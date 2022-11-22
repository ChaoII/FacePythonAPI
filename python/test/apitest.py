import requests
import os, sys
import cv2
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from base.utils import *


def test_register_face_api(id_, name, img):
    # ============test register_face api============
    url = "http://localhost:9026/register_face"
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
    url = "http://localhost:9026/face_recognize"
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
    test_register_face_api('71', '成龙', '../../images/1.jpg')
    test_register_face_api('72', '艾超', '../../images/aichao.jpg')
    test_register_face_api('73', '刘德华', '../../images/liudehua.jpg')
    test_register_face_api('74', '佟大为', '../../images/tongdawei.jpg')
    test_register_face_api('75', '奥沫沫', '../../images/oumei.jpg')
    test_register_face_api('76', 'chao2', '../../images/img.png')

    # test_face_recognize('../../images/img.png')
    # test_delete_face('04')
    # test_get_face_library('04')
