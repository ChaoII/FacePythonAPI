//
// Created by aichao on 2022/11/23.
//

#pragma once

#include "src/utils/utils.h"
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <seeta/CStruct.h>
#include <seeta/FaceTracker.h>
#include <seeta/FaceDetector.h>
#include <seeta/FaceLandmarker.h>
#include <vector>

namespace py = pybind11;

FACEAPI void BindFaceAPI(py::module &);

FACEAPI void PyArrayToSeetaImageData(py::array_t<unsigned char> pyarray, SeetaImageData *data);

FACEAPI py::array_t<unsigned char> SeetaImageDataToPyArray(const SeetaImageData &data);

FACEAPI std::vector<int> SeetaPoint2vector(const SeetaPoint &point);

FACEAPI std::vector<float> SeetaPointF2vector(const SeetaPointF &point);

FACEAPI std::vector<int> SeetaRect2vector(const SeetaRect &rect);

FACEAPI std::vector<float>
SeetaFaceInfo2vector(const SeetaFaceInfo &face_info);

FACEAPI std::vector<std::vector<float>>
SeetaFaceInfoArray2vector(const SeetaFaceInfoArray &face_infos);

FACEAPI std::vector<float>
SeetaTrackingFaceInfo2vector(const SeetaTrackingFaceInfo &track_info);

FACEAPI std::vector<std::vector<float>>
SeetaTrackingFaceInfoArray2vector(const SeetaTrackingFaceInfoArray &track_infos);
