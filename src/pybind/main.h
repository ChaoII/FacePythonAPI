//
// Created by aichao on 2022/11/23.
//

#pragma once

#include "src/utils/utils.h"
#include "src/pybind/FaceAPI.h"
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <seeta/CStruct.h>
#include <seeta/FaceTracker.h>
#include <seeta/FaceDetector.h>
#include <vector>

namespace py = pybind11;

FACEAPI void BindStruct(py::module &);

FACEAPI void BindFaceAPI(py::module &);

FACEAPI void PyArrayToSeetaImageData(py::array_t<unsigned char> pyarray, SeetaImageData *data);

FACEAPI py::array_t<unsigned char> SeetaImageDataToPyArray(const SeetaImageData &data);

