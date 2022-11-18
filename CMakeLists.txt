cmake_minimum_required(VERSION 3.12)
project(FaceAPI)
set(LIBRARY_NAME FaceAPI)

option(USE_GPU "" OFF)

add_compile_options(-std=c++11 -fpic -O2)

find_package(OpenMP)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")

#添加头文件搜索路径
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
#添加动态库搜索文件
set(DEPEND_LIBS "")
set(INC_DIR ${CMAKE_CURRENT_SOURCE_DIR})


file(GLOB_RECURSE SRCS ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp)
add_library(${LIBRARY_NAME} SHARED ${SRCS})
# 设置文件输出目录
if (WIN32)
    add_definitions(-DFACE_LIB)
    set(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR}/lib/win)
elseif (APPLE)
    set(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR}/lib/mac)
elseif (UNIX)
    set(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR}/lib/linux)
else ()
    message(FATAL_ERROR "unsupported this system")
endif ()
# seetaface
include(${CMAKE_CURRENT_SOURCE_DIR}/cmake/seetaface.cmake)

include_directories(${INC_DIR})
if (APPLE)
    set_target_properties(${LIBRARY_NAME} PROPERTIES COMPILE_FLAGS "-fvisibility=hidden")
elseif (MSVC)
else ()
    set_target_properties(${LIBRARY_NAME} PROPERTIES COMPILE_FLAGS "-fvisibility=hidden")
    set_target_properties(${LIBRARY_NAME} PROPERTIES LINK_FLAGS "-Wl,--exclude-libs,ALL")
    set_target_properties(${LIBRARY_NAME} PROPERTIES LINK_FLAGS_RELEASE -s)
endif ()

target_link_libraries(${LIBRARY_NAME} ${DEPEND_LIBS})

if (WIN32)
    add_custom_command(
            TARGET ${LIBRARY_NAME} POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E mv
            ${LIBRARY_OUTPUT_PATH}/Release/FaceAPI.dll
            ${LIBRARY_OUTPUT_PATH}/FaceAPI.dll)
endif ()