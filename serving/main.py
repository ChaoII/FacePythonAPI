from face import FaceAPI
from typing import Optional
from models.models import FaceInfo
from base.config import settings
from base.utils import base64_to_image
from fastapi import FastAPI, Body, applications
from base.db import do_stuff, init
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from models.pydantic_models import FaceInfoIn
from base.middleware import (register_offline_docs,
                             register_middleware,
                             register_orm,
                             register_exception,
                             register_limit,
                             register_cors)

face_api = FaceAPI()
# 必须在app实例化之前进行注册
register_offline_docs(applications)
# 实例化app
app = FastAPI(**settings.FastAPI_SETTINGS)
app.mount(path="/facelib", app=StaticFiles(directory="./facelib"), name="facelib")
app.mount("/static", StaticFiles(directory="static"), name="static")

register_orm(app)
register_cors(app)
register_exception(app)
limiter = register_limit(app)
register_middleware(app)


@app.on_event("startup")
async def initial_db():
    # 初始化数据库连接
    await init()


@app.on_event("shutdown")
async def shutdown_event():
    """添加在应用程序关闭时关闭所有数据库链接"""
    await do_stuff()
    # 卸载engine
    face_api.unload_engine()


@app.post("/register_face")
@limiter.limit("5/second")
async def register_face(request: Request, face_info: FaceInfoIn):
    uid = face_info.uid
    name = face_info.name
    # 注册人脸时，先删除已存在的人脸
    await face_api.delete_face_sub(uid)
    error_index = []
    for index, img_str in enumerate(face_info.images):
        if not isinstance(img_str, str):
            return {"code": -1, "data": {"uid": uid, "name": name}, "msg": "人脸数据必须是base64字符串"}
        img = base64_to_image(img_str)
        ret = await face_api.register_face_sub(img, uid, name)
        if ret == -1:
            error_index.append(index)
    if len(error_index) == 0:
        return {"code": 0, "data": {"uid": uid, "name": name}, "msg": "注册人脸成功!"}
    else:
        return {"code": -1, "data": {"uid": uid, "name": name}, "msg": f"图像{error_index}注册失败,请确认是正确的base64字符串"}


@app.delete("/delete_face")
@limiter.limit("5/second")
async def delete_face(request: Request, uid: str = Body(..., embed=True)):
    ret = await face_api.delete_face_sub(uid)
    if ret == -1:
        return {"code": -1, "data": {"uid": uid}, "msg": "删除人脸失败！"}
    else:
        return {"code": 0, "data": {"uid": uid}, "msg": "删除人脸成功！"}


@app.post("/face_recognize")
@limiter.limit("5/second")
async def face_recognize(request: Request, image: str = Body(..., embed=True, alias="imageBase64")):
    image = base64_to_image(image)
    if image is None:
        return {"code": -1, "data": {}, "msg": "未知异常! 请确认人脸完全在人脸遮罩内"}
    ret = face_api.face_recognize_sub(image)

    if ret is None:
        return {"code": -1, "data": {}, "msg": "未知异常! 请确认人脸完全在人脸遮罩内"}
    if ret == -1:
        return {"code": -1, "data": {},
                "msg": "人脸识别失败，请准确将人脸置于指定区域，或人脸不在人脸库中"}
    elif ret == -2:
        return {"code": -2, "data": {}, "msg": "非活体人脸！"}
    else:
        return {"code": 0, "data": {"uid": ret[0], "name": ret[1]}, "msg": "人脸识别成功!"}


@app.post("/get_face_library")
@limiter.limit("5/second")
async def get_face_library(request: Request, uid: Optional[str] = Body(None, embed=True)):
    if uid is None:
        data = await FaceInfo.all()
    else:
        data = await FaceInfo.filter(uid=uid).all()
    return {"code": 0, "data": {"result": data}, "msg": "人脸信息查询成功!"}
