# **人脸识别综合应用**

## 1. 简介

项目基于`SeetaFace6`，分发不同使用场景：
- 提供基于cuda编译的tennis前向推理引擎库（windows，cuda11.2）
- 根据pybind11进行python接口封装，使用面向对象的方式，让接口更加自然合理，使用更加便捷 
- 封装的进行extern C 的纯C封装方式，并使用 ctypes 调用提供python接口，解除不同版本python使用上的限制，使用简便，性能与原始c++模块基本一致，基于C，支持更多语言拓展
- 基于ctypes python接口的提供fastapi的服务化部署方式，支持接口限流、异步orm尽可能提高QPS的工作负载，此外集成faiss向量索引方式，理论上百万级别人脸库1:N搜索耗时为ms级别。
- 项目采用CMake进行构建，支持windows/linux/macos
- 支持python3.6+版本

## 2.下载模型（已下载则忽略）

[点击查看下载模型](./model/README.md)
## 3. SeetaFace6预编译库下载
本项目已经提供了预编译库，包含windows|linux|macos(均为x86_64CPU架构，其它架构请自行编译)，其中windows下提供GPU编译库，由于系统差异巨大导致的二进制文件无法使用，请进行源码编译，编译详情参考[SeetaFace6Open](https://github.com/SeetaFace6Open/index)
## 4. 源码编译
### 4.1 基础环境
- CMake
- 各平台的编译工具
- 具体安装方式不在本文档的说明范畴内
### 4.2 拉取源码
```bash
git clone --recursive https://github.com/ChaoII/FacePythonAPI.git
```
仓库包含部分二进制文件，可能比较大，如果拉不下来，请自行百度
其中--recursive 可以同步拉取pybind11项目子模块
### 4.3 CPU版本编译
其中项目CPU、GPU主要依赖于tennis引擎，但是选择不同的编译方式可以自动的进行库的选择，并添加cuda路径配置
```bash
cmake ..
cmake --build . --config Release --target FaceAPI -j4
```
其中cmake .. 后面可跟-G参数指定生成器，如果不会请自行参考百度
**Note:**windows 上如果是MSVC请打开VS开发命令提示符，执行上述命令，别傻乎乎的打开IDE折腾
### 4.4 GPU版本
```
cmake .. -DBUILD_WITH_GPU=ON -DCUDA_DIR="xxx"
cmake --build . --config Release --target FaceAPI -j4
```
最终编译得到`FaceAPI.dll(windows) | libFaceAPI.so(windows) | libFaceAPI.dylib(macos)
## 5. 基础运行

### 5.1  确认硬件基础
1. 确认CPU以及操作系统为64位
2. 下载cpu-z或者其它软件查看CPU是否支持 AVX | SSE | FMA
3. 确认机器是够装有NVIDIA显卡，并且已经安装好CUDA和对应CUDNN（提供11.x的GPU库，如果不同请往上看自行编译）
****
如果：
- 条件1不满足，或者操作系统比较古老，请自行编译
- 条件2不满足，请将仓库中third/seeta/lib/{你的平台}/tennis_pentium.xx改成tennis.xx(因为奔腾CPU不支持AVX指令集)
- 条件3不满足，请老老实实用CPU去玩
### 5.2依赖安装
既然人脸识别属于视觉范畴，所以不得不准备opencv库，其安装方式为：
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python
# 部分机器存在问题，可能是图形截面导致的，可以安装headless类型opencv
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python-headless
```
### 5.3 库路径设置
由于编译文件依赖于第三方的库，需要将第三方库放置于环境变量中（非windows）
`linux/macos`需要添加库路径
- 临时
```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${seetaFace6Python目录路径}/seetaface/lib/linux
``` 
- 永久
```shell script
sudo echo  ${编译目录}/lib/linux  > /etc/ld.so.conf.d/facepythonapi.conf
sudo ldconfig    
``` 
windows下将依赖库文件放在与编译生成的FaceAPI.dll同目录即可
### 5.4 示例代码
部分代码如下，想看更详细使用方式(查看[serving 使用方式](./serving/README.md)或者查看api.py文档
```python
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
    def register_face_sub(self, face, uid: str, name: str = None):
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
    def delete_face_sub(self, uid: str):
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
        ret = self.index_manager.search_result(self.seetaFace.get_feature_numpy(feature))
        if ret is None:
            logger.warning("人脸索引异常...")
            return -1
        distances, indexs = ret
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
```



