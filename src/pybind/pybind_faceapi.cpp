//
// Created by aichao on 2022/11/24.
//
#include "src/pybind/main.h"
#include "src/pybind/FaceAPI.h"

void BindFaceAPI(py::module &m) {

    py::class_<FaceAPI>(m, "FaceAPI")
            .def(py::init<const std::string &, const std::vector<int> &, int, int>(),
                 py::arg("model_dir"),
                 py::arg("functions"),
                 py::arg("device"),
                 py::arg("id"))
            .def("detect", [](FaceAPI &self, const py::array_t<unsigned char> &img) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.Detect(s_img);
            })
            .def("set_property", &FaceAPI::SetProperty)
            .def("mark5", [](FaceAPI &self, const py::array_t<unsigned char> &img, const std::vector<float> &box) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.mark5(s_img, box);
            })
            .def("mark68", [](FaceAPI &self, const py::array_t<unsigned char> &img, const std::vector<float> &box) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.mark68(s_img, box);
            })
            .def("set_live_threshold", &FaceAPI::SetLiveThreshold)
            .def("alive_detect", [](FaceAPI &self, const py::array_t<unsigned char> &img,
                                    const std::vector<float> &box,
                                    const std::vector<std::vector<float>> &points5) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.AliveDetect(s_img, box, points5);
            })
            .def("get_alive_score", [](FaceAPI &self) {

                float clarity;
                float reality;
                self.GetAliveScore(&clarity, &reality);
                std::vector<float> live_status({clarity, reality});
                return live_status;
            })
            .def("video_alive_detect", [](FaceAPI &self,
                                          const py::array_t<unsigned char> &img,
                                          const std::vector<float> &box,
                                          const std::vector<std::vector<float>> &points5) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.VideoAliveDetect(s_img, box, points5);
            })
            .def("reset_video_alive", &FaceAPI::ResetVideoAlive)
            .def("mark_mask", [](FaceAPI &self,
                                 const py::array_t<unsigned char> &img,
                                 const std::vector<float> &box) {

                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.DetectMask(s_img, box);
            })
            .def("predict_age_crop", [](FaceAPI &self,
                                        const py::array_t<unsigned char> &img,
                                        const std::vector<std::vector<float>> &points5) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.PredictAgeWithCrop(s_img, points5);
            })
            .def("predict_age", [](FaceAPI &self,
                                   const py::array_t<unsigned char> &img) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.PredictAge(s_img);
            })
            .def("predict_gender_crop", [](FaceAPI &self,
                                           const py::array_t<unsigned char> &img,
                                           const std::vector<std::vector<float>> &points5) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.PredictGenderWithCrop(s_img, points5);
            })
            .def("predict_gender", [](FaceAPI &self,
                                      const py::array_t<unsigned char> &img) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.PredictGender(s_img);
            })
            .def("detect_mask", [](FaceAPI &self,
                                   const py::array_t<unsigned char> &img,
                                   const std::vector<float> &box) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.DetectMask(s_img, box);
            })
            .def("get_eyes_status", [](FaceAPI &self,
                                       const py::array_t<unsigned char> &img,
                                       const std::vector<std::vector<float>> &points5) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.DectectEye(s_img, points5);
            })
            .def("clarity_evaluate", [](FaceAPI &self,
                                        const py::array_t<unsigned char> &img,
                                        const std::vector<float> &box,
                                        const std::vector<std::vector<float>> &points5) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.ClarityEvaluate(s_img, box, points5);
            })
            .def("bright_evaluate", [](FaceAPI &self,
                                       const py::array_t<unsigned char> &img,
                                       const std::vector<float> &box,
                                       const std::vector<std::vector<float>> &points5) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.BrightEvaluate(s_img, box, points5);
            })
            .def("resolution_evaluate", [](FaceAPI &self,
                                           const py::array_t<unsigned char> &img,
                                           const std::vector<float> &box,
                                           const std::vector<std::vector<float>> &points5) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.ResolutionEvaluate(s_img, box, points5);
            })
            .def("pose_evaluate", [](FaceAPI &self,
                                     const py::array_t<unsigned char> &img,
                                     const std::vector<float> &box,
                                     const std::vector<std::vector<float>> &points5) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.PoseEvaluate(s_img, box, points5);
            })
            .def("integrity_evaluate", [](FaceAPI &self,
                                          const py::array_t<unsigned char> &img,
                                          const std::vector<float> &box,
                                          const std::vector<std::vector<float>> &points5) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.IntegrityEvaluate(s_img, box, points5);
            })
            .def("track", [](FaceAPI &self,
                             const py::array_t<unsigned char> &img) {

                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.Track(s_img);
            })
            .def("reset_track", &FaceAPI::ResetTrack)
            .def("set_track_min_face_size", &FaceAPI::SetTrackMinFaceSize)
            .def("set_track_resolution", &FaceAPI::SetTrackResolution)
            .def("set_track_threshold", &FaceAPI::SetTrackThreshold)
            .def("set_track_interval", &FaceAPI::SetTrackInterval)
            .def("set_track_threads", &FaceAPI::SetTrackThreads)
            .def("crop_face", [](FaceAPI &self,
                                 const py::array_t<unsigned char> &img,
                                 const std::vector<std::vector<float>> &points5) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                auto data = self.CropFace(s_img, points5);
                return SeetaImageDataToPyArray(data);
            })
            .def("extract_cropped_face", [](FaceAPI &self,
                                            const py::array_t<unsigned char> &img) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.ExtractCroppedFace(s_img);
            })
            .def("extract", [](FaceAPI &self,
                               const py::array_t<unsigned char> &img,
                               const std::vector<std::vector<float>> &points5) {
                SeetaImageData s_img{};
                PyArrayToSeetaImageData(img, &s_img);
                return self.Extract(s_img, points5);
            })
            .def("calculate_similarity", &FaceAPI::CalculateSimilarity);

}