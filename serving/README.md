# 人脸识别服务化部署

基于`ctypes python`接口的提供`fastapi`的服务化部署方式，支持接口限流，异步`orm`尽可能提高`QPS`的工作负载，此外集成`faiss`向量索引方式，理论上百万级别人脸库`1:N`搜索耗时为`ms`级别。
当然其ctypes 接口可以换成python pybind包直接安装，按照说明进行修改。

### 1、程序运行

#### 1.1 依赖安装

```bash
pip install -r requirements.txt
```

**注意：**

1. 需要确保目录下lib文件有对应平台的库，比如mac下./lib/mac/*.dylib
2. 确保model文件夹下有模型文件，比如：./model/*.csta
3. 如果没有除了可以手动添加外，也提供了自动化脚本方式 编译源码，编译方式见首页[源码编译](../README.md)
4. 进入`cd FacePythonAPI/serving/script/`，执行`python copy_libs.py`,注意必须进入脚本目录，不然执行copy操作后，会显示路径错误

#### 1.2 运行

```bash
python run.py
bash
```

其中交互式文档请访问：

```bash
http://ip:port/docs
```

API文档请访问

```bash
http://ip:port/redoc
```

### 3.调用示例

```python
import cv2
import requests


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
    url = "http://127.0.0.1:9026/delete_face"
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
    url = "http://127.0.0.1:9026/get_face_library"
    data = {'uid': id_}
    if id_ is None:
        data = {}
    print(data)
    ret = requests.post(url=url, json=data)
    print(ret.json())
```





