# 人脸识别服务化部署

基于`ctypes python`接口的提供`fastapi`的服务化部署方式，支持接口限流，异步`orm`尽可能提高`QPS`的工作负载，此外集成`faiss`向量索引方式，理论上百万级别人脸库`1:N`搜索耗时为`ms`级别。
当然其ctypes 接口可以换成python pybind包直接安装，按照说明进行修改。

### 1、程序运行

#### 1.1 依赖安装

```bash
pip install -r requirements.txt
```

**注意：**

1. 需要确保目录下`lib`文件有对应平台的库，比如`mac`下`./lib/mac/*.dylib`
2. 确保`model`文件夹下有模型文件，比如：`./model/*.csta`
3. 如果没有除了可以手动添加外，也提供了自动化脚本方式 编译源码，编译方式见首页[源码编译](../README_CN.md)
4. 进入`cd FacePythonAPI/serving/script/`，执行`python copy_libs.py`,注意必须进入脚本目录，不然执行copy操作后，会显示路径错误

#### 1.2 https证书
如果需要开启`https`需要设置证书和秘钥，租用公有云服务器，会免费提供对应的证书秘钥。对于私有化部署也可以根据`OpenSSL`生成证书秘钥，但是浏览器会显示**不安全访问**  
`OpenSSL`生成秘钥方式：
1. 生成`rsa`私钥，`des3`算法，`2048`位强度，`ssl.key`是秘钥文件名。强烈建议密钥长度大于等于2048
```bash
openssl genrsa -des3 -out ssl.key 2048
```
2. 输入密码,这里会输入两次，填写一样即可，随意填写一个即可，下一步就会删除这个密码
3. 终端执行删除密码命令，这里目录和生成私钥的目录一致
```bash
openssl rsa -in ssl.key -out ssl.key
```
4. 生成`CSR`（证书签名请求），根据根据刚刚生成的key文件来生成证书请求文件，终端执行如下命令:
```bash
openssl req -new -key ssl.key -out ssl.csr
```
**说明**: 执行以上命令后，需要依次输入国家、地区、城市、组织、组织单位、`Common Name`、`Email`和密码。其中`Common Name`应该与域名保持一致。密码我们已经删掉了,直接回车即可  
**温馨提示**: `Common Name`就是证书对应的域名地址. 我们开发微信小程序时必须要让我们的外链的`https`的域名和证书统一才行
5. 生成自签名证书
根据以上2个文件生成crt证书文件，终端执行下面命令：
```bash
#3650是证书有效期(单位：天)。这个大家随意。最后使用到的文件是key和crt文件。
openssl x509 -req -days 3650 -in ssl.csr -signkey ssl.key -out ssl.crt
```
**注意**: 在使用自签名的证书时，浏览器会提示证书的颁发机构是未知的

在`uvicorn`中添加秘钥和证书参数即可开启`https`服务，注意开启需要修改config.yml文件中的秘钥和证书路径(绝对路径)，如果关闭直接置空即可

#### 1.3 运行

```bash
python run.py
```

#### 1.4 docker 运行方式
1. 已经制作好[docker镜像](https://pan.baidu.com/s/1RzWgLD1OpK7Tt86BgR81xg?pwd=rtrg)，可直接下载并解压
```bash
# 生成faceapi-v3.0.tar
unzip faceapi-v3.0.tar.zip
```
2. 导入镜像
```bash
docker import faceapi-v3.0.tar faceapi:v3.0
```
3. 运行镜像
```bash
docker run -itd --name faceapi --restart=always -v ${work_path}/serving:/opt/serving -w /opt/serving -p 9026:9026 faceapi:v3.0 python3 run.py
```
**注意**: 镜像指定了运行库路径加入了动态库查找路径，必须是`/opt/serving/lib` `-v`后挂载的路径需要是绝对路径

其中交互式文档请访问：

```bash
# 如果开启https请将http改为https
http://ip:port/docs
```

API文档请访问
```bash
# 如果开启https请将http改为https
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





