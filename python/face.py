import os
import cv2
import pickle
import numpy as np
import os.path as oph
from base.log import logger
from base.config import settings
from api.faceapi import SeetaFace
from models.models import FaceInfo

# ------------------initial----------------
MODEL_PATH = os.path.join(settings.ROOT_DIR, "model")
FACE_IMAGE_DIR = os.path.join(settings.BASE_DIR, "facelib")
FACE_LIBS_FILE = os.path.join(FACE_IMAGE_DIR, "facelib.pkl")
FACE_FEATURE_LIBS = dict()
device = 2 if settings.USE_GPU else 1
seetaFace = SeetaFace(settings.FUNCTIONS, device=device, id=settings.GPU_ID)
seetaFace.SetTrackResolution(*settings.TRACKING_SIZE)
seetaFace.init_engine(MODEL_PATH)


async def initial_face_libraries_sub():
    global FACE_FEATURE_LIBS
    with open(FACE_LIBS_FILE, "rb") as f:
        FACE_FEATURE_LIBS = pickle.load(f)


async def register_face_sub(face, uid: str, name: str = None, is_initial=False):
    if isinstance(face, np.ndarray):
        img = face.copy()
    elif isinstance(face, str):
        if face.split(".")[-1].lower() in settings.ALLOW_IMAGES:
            img = cv2.imread(face)
        else:
            logger.error(f"仅支持{str(settings.ALLOW_IMAGES)}图像格式文件")
            return -1
    else:
        logger.error("图像格式必须是np.ndarray类型或str类型")
        return -1
    det_result = seetaFace.Detect(img)
    if det_result.size == 0:
        logger.warning("未检测到人脸")
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
        logger.info("删除人脸成功, uid: " + uid + "name: " + face_info["name"])
        return 0
    else:
        logger.warning("face is not existing,face uid is :" + uid)
        return -1


def face_recognize_sub(img: np.ndarray):
    det_result = seetaFace.Detect(img)
    if det_result.size == 0:
        logger.warning("未检测到人脸...")
        return
    # 仅识别画面中最大的人脸
    face_areas = []
    for i in range(det_result.size):
        face_data = det_result.data[i]
        face = face_data.pos
        face_areas.append(face.width * face.height)
    # 排序
    face_areas.sort(reverse=True)
    # 选取最大的人脸
    face_data = det_result.data[0]
    face = face_data.pos
    points = seetaFace.mark5(img, face)
    # 0: 真实人脸
    # 1: 攻击人脸（假人脸）
    # 2: 无法判断（人脸成像质量不好）
    if settings.IS_ANTI_SPOOF:
        livnees = seetaFace.Predict(img, face, points)
        if livnees == 1:
            logger.warning("攻击人脸...")
            return -2
    feature = seetaFace.Extract(img, points)
    max_similar = 0
    max_key = ""
    # todo(aichao) 理论上人脸库过大会严重影响效率，采用faiss索引的方式进行
    for key in FACE_FEATURE_LIBS.keys():
        similar = seetaFace.compare_feature_np(seetaFace.get_feature_numpy(feature), FACE_FEATURE_LIBS[key]["feature"])
        if similar > max_similar:
            max_similar = similar
            max_key = key
    # 阈值
    if max_similar > settings.REC_THRESHOLD:
        name = FACE_FEATURE_LIBS[max_key]["name"]
        uid = max_key
        return uid, name
    else:
        logger.warning("当前人脸不在人脸库中")
        return -1


def age_predict(image, points):
    age = seetaFace.PredictAgeWithCrop(image, points)
    return age
