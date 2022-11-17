import cv2
import base64
import numpy as np
from base.log import logger

fontFace = cv2.FONT_HERSHEY_COMPLEX_SMALL
fontScale = 0.6
thickness = 1


def image_to_base64(image_np):
    """
    将np图片(imread后的图片）转码为base64格式
    image_np: cv2图像，numpy.ndarray
    Returns: base64编码后数据
    """
    image = cv2.imencode('.jpg', image_np)[1]
    image_code = str(base64.b64encode(image))[2:-1]
    image_code = "image/jpeg;base64," + image_code
    return image_code


def base64_to_image(base64_code: str):
    """
    将base64编码解析成opencv可用图片
    base64_code: base64编码后数据
    Returns: cv2图像，numpy.ndarray
    """
    try:
        base64_list = base64_code.split(",")
        if len(base64_list) == 2:
            base64_code = base64_list[1]
        # base64解码
        img_data = base64.b64decode(base64_code)
        # 转换为np数组
        img_array = np.fromstring(img_data, np.uint8)
        # 转换成opencv可用格式
        img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
    except Exception as e:
        logger.error("base64图像解码异常，具体：" + str(e))
        return None
    return img


def draw_image(image: np.ndarray, text: str, face_position):
    ret_val, base_line = cv2.getTextSize(text, fontFace=fontFace, fontScale=fontScale,
                                         thickness=thickness)
    left, top = face_position[0], face_position[1]
    right, bottom = face_position[2], face_position[3]
    cv2.rectangle(image, (left, top), (right, bottom), color=(0, 255, 255), thickness=thickness, lineType=cv2.LINE_AA)
    cv2.rectangle(image, (left, top - ret_val[1] - base_line), (left + ret_val[0], top), thickness=-1,
                  color=(0, 255, 255))
    cv2.putText(image, text, (left, top - base_line), fontFace=fontFace, fontScale=fontScale,
                color=(255, 0, 255),
                thickness=1, lineType=cv2.LINE_AA)
    return image


if __name__ == '__main__':
    img = cv2.imread("asserts/1.jpg")
    ret = image_to_base64(img)
    print(ret)
