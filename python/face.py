import os
import cv2
import pickle
import numpy as np
import os.path as oph
from base.utils import run_time
from base.log import logger
from base.config import settings
from api.faceapi import SeetaFace
from models.models import FaceInfo
from index import IndexManager


class FaceAPI:
    def __init__(self):
        # ------------------initial----------------
        self.FACE_LIB_DIR = os.path.join(settings.BASE_DIR, "facelib")
        self.FACE_IMAGE_DIR = os.path.join(self.FACE_LIB_DIR, "images")
        self.INDEX_DIR = os.path.join(self.FACE_LIB_DIR, "index")
        self.FACE_LIBS_FILE = os.path.join(self.FACE_LIB_DIR, "facelib.pkl")
        # 初始化项目路径
        self.initial_directory()
        # 初始化人脸特征库对象
        self.FACE_FEATURE_LIBS = dict()
        # 初始化索引
        self.index_manager = IndexManager(self.INDEX_DIR)
        # 声明seetaFace对象
        self.seetaFace = None
        self.init_model()

    def initial_directory(self):
        if not os.path.exists(self.FACE_LIB_DIR):
            os.mkdir(self.FACE_LIB_DIR)

        if not os.path.exists(self.FACE_IMAGE_DIR):
            os.mkdir(self.FACE_IMAGE_DIR)

        if not os.path.exists(self.INDEX_DIR):
            os.mkdir(self.INDEX_DIR)

    @run_time
    def init_model(self):
        model_dir = os.path.join(settings.BASE_DIR, "model")
        if not os.path.exists(model_dir):
            logger.error("模型路径不存在，请先将模型所在文件夹【model】放置于，启动文件同级目录下")
            exit(-1)
        device = 2 if settings.USE_GPU else 1
        self.seetaFace = SeetaFace(settings.FUNCTIONS, device=device, id=settings.GPU_ID)
        self.seetaFace.SetTrackResolution(*settings.TRACKING_SIZE)
        self.seetaFace.init_engine(model_dir)
        self.initial_face_libraries_sub()

    def get_seetaface(self):
        return self.seetaFace

    def initial_face_libraries_sub(self):
        if not os.path.exists(self.FACE_LIBS_FILE):
            return
        with open(self.FACE_LIBS_FILE, "rb") as f:
            self.FACE_FEATURE_LIBS = pickle.load(f)
        # 初始化阶段构建索引库
        self.index_manager.build_index(self.FACE_FEATURE_LIBS)

    @run_time
    async def register_face_sub(self, face, uid: str, name: str = None):
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
        det_result = self.seetaFace.Detect(img)
        if det_result.size == 0:
            logger.warning("未检测到人脸，请确保画面中存在人脸...")
            return -1
        face = det_result.data[0].pos
        points = self.seetaFace.mark5(img, face)
        feature = self.seetaFace.Extract(img, points)
        # update face libraries
        self.FACE_FEATURE_LIBS.update({uid: {"name": name, "feature": self.seetaFace.get_feature_numpy(feature)}})
        # 保存并覆盖
        with open(self.FACE_LIBS_FILE, "wb") as f:
            pickle.dump(self.FACE_FEATURE_LIBS, f)
        # ------------------ 重新构建索引-------------------
        self.index_manager.build_index(self.FACE_FEATURE_LIBS)
        img_url = "/facelib/images/" + uid + ".jpg"
        img_path = oph.join(self.FACE_IMAGE_DIR, uid + ".jpg")
        # 判断人脸是否存在，存在
        face = await FaceInfo.filter(uid=uid).first()
        if face is None:
            await FaceInfo.create(uid=uid, name=name, face_path=img_path, face_url=img_url)
        else:
            await FaceInfo.filter(uid=uid).update(name=name, face_path=img_path, face_url=img_url)
        # 保存照片
        cv2.imwrite(img_path, img)
        return 0

    @run_time
    async def delete_face_sub(self, uid: str):
        face = await FaceInfo.filter(uid=uid).first()
        if face is not None:
            # 删除数据库记录
            await FaceInfo.filter(uid=uid).delete()
            # 删除缓存
            face_info = self.FACE_FEATURE_LIBS.pop(uid)
            # 删除图片
            if oph.exists(face.face_url):
                os.remove(face.face_url)
            # 保存人脸库
            with open(self.FACE_LIBS_FILE, "wb") as f:
                pickle.dump(self.FACE_FEATURE_LIBS, f)
            # ------------------ 重新构建索引-------------------
            self.index_manager.build_index(self.FACE_FEATURE_LIBS)
            logger.info("删除人脸成功, uid: " + uid + "name: " + face_info["name"])
            return 0
        else:
            logger.warning("人脸不存在，uid :" + uid)
            return -1

    @run_time
    def face_recognize_sub(self, img: np.ndarray):
        det_result = self.seetaFace.Detect(img)
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
        points = self.seetaFace.mark5(img, face)
        # 0: 真实人脸
        # 1: 攻击人脸（假人脸）
        # 2: 无法判断（人脸成像质量不好）
        if settings.IS_ANTI_SPOOF:
            livnees = self.seetaFace.Predict(img, face, points)
            if livnees == 1:
                logger.warning("攻击人脸...")
                return -2
        feature = self.seetaFace.Extract(img, points)
        # 向量查找[HNSW32]以空间换时间，召回率高
        distances, indexs = self.index_manager.search_result(self.seetaFace.get_feature_numpy(feature))
        # 阈值
        if distances[0][0] > settings.REC_THRESHOLD:
            uid = str(indexs[0][0])
            # 比如uid为"023"经过索引后变成23这样会找不到id
            if uid not in self.FACE_FEATURE_LIBS.keys():
                logger.warning("当前人脸不在人脸库中, 人脸库可能出现混乱, 请重新梳理人脸库, 或者人脸id异常，注意：【人脸id必须是整形，并且，不能是以0开头】")
                return -1
            name = self.FACE_FEATURE_LIBS[uid]["name"]
            return uid, name
        else:
            logger.warning("当前人脸不在人脸库中")
            return -1

    def age_predict(self, image, points):
        age = self.seetaFace.PredictAgeWithCrop(image, points)
        return age

    def unload_engine(self):
        self.seetaFace.unload_engine()
