# **SeetaFace6Open python 绑定**

### 1、CPU编译

```bash
python setup.py build
python setup.py bdist_wheel
```

经过以上两步即可生成`faceapi_python-1.0.1-py3-none-any.whl`

### 2、GPU编译(mac不支持GPU使用)

#### 2.1 windows

```bash
set BUILD_WITH_GPU=ON
set CUDA_DIR="xxx"
```

#### 2.2 linux

``
export BUILD_WITH_GPU=ON
export CUDA_DIR="xxx"
``
其中CUDA_DIR为本地CUDA安装目录

#### 2.3 执行

```bash
python setup.py build
python setup.py bdist_wheel
```

生成`faceapi_gpu_python-1.0.1-py3-none-any.whl`

### 3、安装

```bash
pip install faceapi_python-1.0.1-py3-none-any.whl
```

### 4、使用

```python
from faceapi import FaceAPI
import cv2

# [0,1,15]表示人脸检测、关键点、人脸识别
api = FaceAPI("../model", [0, 1, 15])
img1 = cv2.imread("../images/2.jpg")
img2 = cv2.imread("../images/2.jpg")


def feature_extract(image):
    result = api.detect(image)
    box = result.data.pos
    points5 = api.mark5(image, box)
    feature = api.extract(image, points5)
    return feature


feature1 = feature_extract(img1)
feature2 = feature_extract(img2)
similar = api.calculate_similarity(feature1, feature2)
```