import os
import numpy as np

from face import FaceAPI
import faiss

import pickle
import cv2

face_api = FaceAPI()
faiss.omp_set_num_threads(4)
seetaFace = face_api.get_seetaface()

index = faiss.read_index("facelib/index/vector.index")
img = cv2.imread("../images/123.jpg")
det_result = face_api.seetaFace.Detect(img)

face = det_result.data[0].pos
points = seetaFace.mark5(img, face)
feature = seetaFace.Extract(img, points)
# seetaFace.unload_engine()
f = seetaFace.get_feature_numpy(feature).reshape((1, -1))
# print(face_api.face_recognize_sub(img))

d, i = index.search(f, 4)
print(d, i)
