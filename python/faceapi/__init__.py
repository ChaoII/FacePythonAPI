from . import c_lib_wrap as C
import numpy as np


class FaceAPI:
    def __init__(self, model_dir: str, functions: list, device: int = 0, device_id: int = 0):
        self.face_api = C.FaceAPI(model_dir, functions, device, device_id)

    def detect(self, img):
        return self.face_api.detect(img)

    def set_property(self, attribute, value):
        self.face_api.set_property(attribute, value)

    def mark5(self, img: np.ndarray, box):
        return self.face_api.mark5(img, box)

    def mark68(self, img: np.ndarray, box):
        return self.face_api.mark68(img, box)

    def set_live_threshold(self, clarity: float, reality: float):
        self.face_api.set_live_threshold(clarity, reality)

    def alive_detect(self, img, box, points5):
        return self.face_api.alive_detect(img, box, points5)

    def get_alive_score(self):
        return self.face_api.get_alive_score()

    def video_alive_detect(self, img, box, points5):
        return self.face_api.video_alive_detect(img, box, points5)

    def reset_video_alive(self):
        return self.face_api.reset_video_alive()

    def mark_mask(self, img, box):
        return self.face_api.mark_mask(img, box)

    def predict_age_crop(self, img, points5):
        return self.face_api.predict_age_crop(img, points5)

    def predict_age(self, img):
        return self.face_api.predict_age(img)

    def predict_gender_crop(self, img, points5):
        return self.face_api.predict_gender_crop(img, points5)

    def predict_gender(self, img):
        return self.face_api.predict_gender(img)

    def detect_mask(self, img, box):
        return self.face_api.detect_mask(img, box)

    def get_eyes_status(self, img, points5):
        return self.face_api.get_eyes_status(img, points5)

    def clarity_evaluate(self, img, box, points5):
        return self.face_api.clarity_evaluate(img, box.points5)

    def bright_evaluate(self, img, box, points5):
        return self.face_api.bright_evaluate(img, box, points5)

    def resolution_evaluate(self, img, box, points5):
        return self.face_api.resolution_evaluate(img, box.points5)

    def pose_evaluate(self, img, box, points5):
        return self.face_api.pose_evaluate(img, box, points5)

    def integrity_evaluate(self, img, box, points5):
        return self.face_api.integrity_evaluate(img, box, points5)

    def track(self, img):
        return self.face_api.track(img)

    def reset_track(self):
        self.face_api.reset_track()

    def set_track_min_face_size(self, face_size: int):
        self.face_api.set_track_min_face_size(face_size)

    def set_track_resolution(self, width: int, height: int):
        self.face_api.set_track_resolution(width, height)

    def set_track_threshold(self, threshold: int):
        self.face_api.set_track_threshold(threshold)

    def set_track_interval(self, interval: int):
        self.face_api.set_track_interval(interval)

    def set_track_threads(self, threads: int):
        self.face_api.set_track_threads(threads)

    def crop_face(self, img, points5):
        return self.face_api.crop_face(img, points5)

    def extract_cropped_face(self, img):
        return self.face_api.extract_cropped_face(img)

    def extract(self, img, points5):
        return self.face_api.extract(img, points5)

    def calculate_similarity(self, feature1, feature2):
        return self.calculate_similarity(feature1, feature2)
