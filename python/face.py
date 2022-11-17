import os
import pickle

import cv2
import json
import numpy as np
from models.models import FaceInfo
import os.path as oph
from api.faceapi import *
from base.log import logger

# ------------------initial----------------
# 在api中初始化了
# ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(ROOT_DIR, "model")
FACE_IMAGE_DIR = os.path.join(ROOT_DIR, "python", "facelib")
FACE_LIBS_FILE = os.path.join(FACE_IMAGE_DIR, "facelib.pkl")
TRACKING_RESOLUTION = (310, 310)
IS_ANTI_SPOOF = False
FACE_FEATURE_LIBS = dict()
FUNCTAION_LISTS = ["FACE_DETECT",
                   "LANDMARKER5",
                   "LIVENESS",
                   # "LANDMARKER_MASK",
                   # "FACE_AGE",
                   "FACE_GENDER",
                   "FACE_RECOGNITION",
                   # "MOUTH_MASK",
                   "EYE_STATE",
                   "FACE_CLARITY",
                   "FACE_BRIGHT",
                   "FACE_RESOLUTION",
                   # "FACE_POSE",
                   "FACE_INTEGRITY",
                   "FACE_TRACK"]

seetaFace = SeetaFace(FUNCTAION_LISTS, device=0, id=0)
seetaFace.SetTrackResolution(*TRACKING_RESOLUTION)
seetaFace.init_engine(MODEL_PATH)


async def initial_face_libraries_sub():
    global FACE_FEATURE_LIBS
    with open(FACE_LIBS_FILE, "rb") as f:
        FACE_FEATURE_LIBS = pickle.load(f)


async def register_face_sub(face, uid: str, name: str = None, is_initial=False):
    if isinstance(face, np.ndarray):
        img = face.copy()
    elif isinstance(face, str):
        if face.split(".")[-1].lower() in ["jpg", "jpeg", "png", "bmp"]:
            img = cv2.imread(face)
        else:
            logger.error("img file is supported in [jpg, jpeg, png, bmp]")
            return -1
    else:
        logger.error("img must be np.ndarray or img path str")
        return -1
    det_result = seetaFace.Detect(img)
    if det_result.size == 0:
        logger.warning("No face detected")
        return -1
    det_result = seetaFace.Detect(img)
    if det_result.size == 0:
        logger.warning("No face detected")
        return -1
    face = det_result.data[0].pos
    points = seetaFace.mark5(img, face)
    feature = seetaFace.Extract(img, points)
    # update face libraries
    global FACE_FEATURE_LIBS
    FACE_FEATURE_LIBS.update({uid: {"name": name, "feature": seetaFace.get_feature_numpy(feature)}})
    # 保存并覆盖
    with open(FACE_LIBS_FILE, "wb") as f:
        pickle.dump(FACE_FEATURE_LIBS, f)

    img_url = "/facelib/images/" + uid + ".jpg"
    img_path = oph.join(FACE_IMAGE_DIR, "images", uid + ".jpg")
    # 判断人脸是否存在，存在
    face = await FaceInfo.filter(uid=uid).first()
    if face is None:
        await FaceInfo.create(uid=uid, name=name, face_path=img_path, face_url=img_url)
    else:
        await FaceInfo.filter(uid=uid).update(name=name, face_path=img_path, face_url=img_url)
    # 保存照片
    cv2.imwrite(img_path, img)
    return 0


async def delete_face_sub(uid: str):
    face = await FaceInfo.filter(uid=uid).first()
    if face is not None:
        # 删除数据库记录
        await FaceInfo.filter(uid=uid).delete()
        # 删除缓存
        face_info = FACE_FEATURE_LIBS.pop(uid)
        # 删除图片
        if oph.exists(face.face_url):
            os.remove(face.face_url)
        # 保存人脸库
        with open(FACE_LIBS_FILE, "wb") as f:
            pickle.dump(FACE_FEATURE_LIBS, f)
        logger.info("delete face successfully, uid is:" + uid + "name is: " + face_info["name"])
        return 0
    else:
        logger.warning("face is not existing,face uid is :" + uid)
        return -1


def face_recognize_sub(img: np.ndarray, is_register=False):
    det_result = seetaFace.Detect(img)
    if det_result.size == 0:
        logger.warning("No face detected...")
        return
    face_areas = []
    for i in range(det_result.size):
        face_data = det_result.data[i]
        face = face_data.pos
        face_areas.append(face.width * face.height)
    cv2.imwrite("123.jpg", img)
    # sorted by face area
    face_areas.sort(reverse=True)
    # pick largest face as a available face
    face_data = det_result.data[0]
    face = face_data.pos
    points = seetaFace.mark5(img, face)
    # 0: 真实人脸
    # 1: 攻击人脸（假人脸）
    # 2: 无法判断（人脸成像质量不好）
    if IS_ANTI_SPOOF:
        livnees = seetaFace.Predict(img, face, points)
        if livnees == 1:
            logger.warning("anti_spoof face")
            return -2
    feature = seetaFace.Extract(img, points)
    max_similar = 0
    max_key = ""
    for key in FACE_FEATURE_LIBS.keys():
        # similar = seetaFace.CalculateSimilarity(feature, FACE_FEATURE_LIBS[key]["feature"])
        similar = seetaFace.compare_feature_np(seetaFace.get_feature_numpy(feature), FACE_FEATURE_LIBS[key]["feature"])
        if similar > max_similar:
            max_similar = similar
            max_key = key
    if max_similar > 0.7:
        name = FACE_FEATURE_LIBS[max_key]["name"]
        uid = max_key
        return uid, name
    else:
        logger.warning("current face is not in face libraries")
        return -1


def age_predict(image, points):
    age = seetaFace.PredictAgeWithCrop(image, points)
    return age
