//
// Created by aichao on 2022/11/23.
//

#include "src/pybind/main.h"






void BindStruct(py::module &m) {
    py::class_<SeetaPoint>(m, "SeetaPoint")
            .def_readwrite("x", &SeetaPoint::x)
            .def_readwrite("y", &SeetaPoint::y)
            .def("__repr__", [](SeetaPoint &self) {
                return "[x: " + std::to_string(self.x) + ", y: " + std::to_string(self.y) + "]";
            });
    py::class_<SeetaPointF>(m, "SeetaPointF")
            .def_readwrite("x", &SeetaPointF::x)
            .def_readwrite("y", &SeetaPointF::y)
            .def("__repr__", [](SeetaPointF &self) {
                return "[x: " + std::to_string(self.x) + ", y: " + std::to_string(self.y) + "]";
            });
    py::class_<SeetaRect>(m, "SeetaRect")
            .def_readwrite("x", &SeetaRect::x)
            .def_readwrite("y", &SeetaRect::y)
            .def_readwrite("width", &SeetaRect::width)
            .def_readwrite("height", &SeetaRect::height)
            .def("__repr__", [](SeetaRect &self) {
                return "[x:" + std::to_string(self.x) + ", y:" + std::to_string(self.y) +
                       ", width:" + std::to_string(self.width) + ", height:" +
                       std::to_string(self.height) + "]";
            });
    py::enum_<SeetaDevice>(m, "SeetaDevice")
            .value("SEETA_DEVICE_AUTO", SeetaDevice::SEETA_DEVICE_AUTO)
            .value("SEETA_DEVICE_CPU", SeetaDevice::SEETA_DEVICE_CPU)
            .value("SEETA_DEVICE_GPU", SeetaDevice::SEETA_DEVICE_GPU)
            .export_values();
    py::class_<SeetaTrackingFaceInfo>(m, "SeetaTrackingFaceInfo")
            .def_readwrite("pos", &SeetaTrackingFaceInfo::pos)
            .def_readwrite("score", &SeetaTrackingFaceInfo::score)
            .def_readwrite("frame_no", &SeetaTrackingFaceInfo::frame_no)
            .def_readwrite("pid", &SeetaTrackingFaceInfo::PID)
            .def_readwrite("step", &SeetaTrackingFaceInfo::step);
    py::class_<SeetaTrackingFaceInfoArray>(m, "SeetaTrackingFaceInfoArray")
            .def_readwrite("data", &SeetaTrackingFaceInfoArray::data)
            .def_readwrite("size", &SeetaTrackingFaceInfoArray::size);
    py::class_<SeetaFaceInfo>(m, "SeetaFaceInfo")
            .def_readwrite("pos", &SeetaFaceInfo::pos)
            .def_readwrite("score", &SeetaFaceInfo::score);
    py::class_<SeetaFaceInfoArray>(m, "SeetaFaceInfoArray")
            .def_readwrite("data", &SeetaFaceInfoArray::data)
            .def_readwrite("size", &SeetaFaceInfoArray::size);
    py::class_<seeta::FaceLandmarker::PointWithMask>(m, "PointWithMask")
            .def_readwrite("point", &seeta::FaceLandmarker::PointWithMask::point)
            .def_readwrite("mask", &seeta::FaceLandmarker::PointWithMask::mask);
}