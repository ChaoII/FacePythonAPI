cmake_minimum_required(VERSION 3.12)
project(SeetaFaceAPI)

add_compile_options(-std=c++11 -fpic -O2)
find_package(OpenMP)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")

#添加头文件搜索路径
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
#添加动态库搜索文件
set(SeetaLibs "")
if (WIN32)
    set(SeetaLibs "${CMAKE_CURRENT_SOURCE_DIR}/lib/windows")
    add_definitions(-DFACE_LIB)
elseif (APPLE)
    set(SeetaLibs "${CMAKE_CURRENT_SOURCE_DIR}/lib/mac")
elseif (UNIX)
    set(SeetaLibs "${CMAKE_CURRENT_SOURCE_DIR}/lib/linux")
else ()
    message(FATAL_ERROR "unsupported this system")
endif ()
if (APPLE)
    set_target_properties(${LIBRARY_NAME} PROPERTIES COMPILE_FLAGS "-fvisibility=hidden")
elseif (MSVC)
else ()
    set_target_properties(${LIBRARY_NAME} PROPERTIES COMPILE_FLAGS "-fvisibility=hidden")
    set_target_properties(${LIBRARY_NAME} PROPERTIES LINK_FLAGS "-Wl,--exclude-libs,ALL")
    set_target_properties(${LIBRARY_NAME} PROPERTIES LINK_FLAGS_RELEASE -s)
endif ()


link_directories(${SeetaLibs})
set(LIBRARY_OUTPUT_PATH ${SeetaLibs})           #设置库文件的输出目录

add_library(SeetaFaceAPI SHARED faceapi.cpp utils.cpp)
target_link_libraries(SeetaFaceAPI
        SeetaAuthorize tennis
        SeetaQualityAssessor300
        SeetaFaceDetector600
        SeetaAgePredictor600
        SeetaEyeStateDetector200
        SeetaFaceAntiSpoofingX600
        SeetaFaceLandmarker600
        SeetaGenderPredictor600
        SeetaMaskDetector200
        SeetaFaceRecognizer610
        SeetaFaceTracking600)
