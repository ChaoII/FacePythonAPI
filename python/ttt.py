from faceapi import FaceAPI
import cv2

face_api = FaceAPI("../model", [0, 1, 15])

img = cv2.imread("../images/2.jpg")

r = face_api.detect(img)

print(r)
