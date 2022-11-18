# **seetaFace6 python api(10分钟搞定商业级别人脸识别应用)**

## 1. 简介

项目基于`SeetaFace6` 封装的python接口,使用简便,性能与原始c++模块基本一致,
模块上`SeetaFace6` 相较于`SeetaFace2` 上训练样本更多，准确率更高，提供的功能和识别模型也更多
接口封装上，放弃了使用 `pybind11` 封装python 接口，接口函数完全纯 c 接口，使用 ctypes 调用，解除不同版本python使用上的限制
`10分钟搞定`是夸张说法，但本次项目基本涵盖了普通商用人脸识别所需的大部分功能，并且使用简单。

**支持 windows/linux/mac 下python3.6+版本**

## 2.下载模型（已下载则忽略）

点击链接[百度云](https://pan.baidu.com/s/1BT_PDOBZZfzCl1WNLv49Mw?pwd=8ecf)
下载，将下载的所有 *.csta 模型文件 放入 `FacePythonAPI/model` 目录下

## 3. 运行示例

### 3.1 运行依赖

当前需要机器同时支持以下几个指令集 AVX | SSE | FMA ，请先确认机器是否同时支持它们

示例依赖 `opencv` ,安装`opencv`(若已有cv2模块则忽略)

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python
# 部分机器存在问题，可能是图形截面导致的，可以安装headless类型opencv
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python-headless
``` 

### 3.2 演示demo

`linux`下则需要添加库路径
- 临时

```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${seetaFace6Python目录路径}/seetaface/lib/linux
``` 
- 永久
```shell script
sudo echo  ${编译目录}/lib/linux  > /etc/ld.so.conf.d/facepythonapi.conf
sudo ldconfig    
``` 

进入python目录，执行python main.py 即可开启服务


