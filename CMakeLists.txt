cmake_minimum_required(VERSION 3.12)
project(FaceAPI)
set(CMAKE_CXX_STANDARD 11)
set(LIBRARY_NAME FaceAPI)
set(PY_LIBRARY_NAME PYFaceAPI)
option(BUILD_PYTHON "" ON)
option(USE_GPU "" OFF)
set(CUDA_DIR "" CACHE PATH "If build tensorrt backend, need to define path of cuda library.")
message(STATUS "USE GPU: ${USE_GPU}")
add_compile_options(-fpic -O2)

find_package(OpenMP)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")

#添加头文件搜索路径
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
#添加动态库搜索文件
set(DEPEND_LIBS "")
set(INC_DIR ${CMAKE_CURRENT_SOURCE_DIR})


file(GLOB_RECURSE UTILS_SRC ${CMAKE_CURRENT_SOURCE_DIR}/src/utils/*.cpp)
list(APPEND CSRCS ${UTILS_SRC})
file(GLOB_RECURSE CAPI_SRC ${CMAKE_CURRENT_SOURCE_DIR}/src/capi/*.cpp)
list(APPEND CSRCS ${CAPI_SRC})

add_library(${LIBRARY_NAME} SHARED ${CSRCS})
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
if (USE_GPU)
    set(USE_GPU true)
    if (NOT CUDA_DIR)
        message(FATAL "while USE GPU must define CUDA_DIR")
    endif ()
    message(STATUS "CUDA_DIR: ${CUDA_DIR}")
else ()
    set(USE_GPU false)
endif ()
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/serving/config.yml.in ${CMAKE_CURRENT_SOURCE_DIR}/serving/config.yml @ONLY)
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
include(cmake/copyfile.cmake)

if (BUILD_PYTHON)
    add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/third/pybind11)
    if (pybind11_FOUND)
        message(PYBIND11 FOUNDED)
        message(STATUS " Found pybind11 v${pybind11_VERSION}: ${pybind11_INCLUDE_DIRS}")
        message(STATUS " pybind11_INCLUDE_DIRS = ${pybind11_INCLUDE_DIRS}")
        include_directories(${pybind11_INCLUDE_DIRS})
    endif ()
    file(GLOB_RECURSE PYBIND_SRC ${PROJECT_SOURCE_DIR}/src/pybind/*.cpp)
    list(APPEND PYBIND_SRCS ${PYBIND_SRC})
    list(APPEND PYBIND_SRCS ${UTILS_SRC})
    if (MSVC)
        set(PY_EXT_SUFFIX ".pyd")
    elseif (APPLE)
        set(PY_EXT_SUFFIX ".dylib")
    else ()
        set(PY_EXT_SUFFIX ".so")
    endif ()

    # find_package Python has replaced PythonInterp and PythonLibs since cmake 3.12
    # Use the following command in the future; now this is only compatible with the latest pybind11
    # find_package(Python ${PY_VERSION} COMPONENTS Interpreter Development REQUIRED)
    find_package(PythonInterp ${PY_VERSION} REQUIRED)
    find_package(PythonLibs ${PY_VERSION})
    pybind11_add_module(${PY_LIBRARY_NAME} MODULE ${PYBIND_SRCS})

    set_target_properties(${PY_LIBRARY_NAME} PROPERTIES PREFIX "")
    set_target_properties(${PY_LIBRARY_NAME}
            PROPERTIES COMPILE_FLAGS "-fvisibility=hidden")
    #    set_target_properties(${PY_LIBRARY_NAME} PROPERTIES SUFFIX ${PY_EXT_SUFFIX})
    #    set_target_properties(${PY_LIBRARY_NAME}
    #            PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
    target_include_directories(${PY_LIBRARY_NAME} PRIVATE ${PYTHON_INCLUDE_DIR})

    target_include_directories(${PY_LIBRARY_NAME} PUBLIC ${PROJECT_SOURCE_DIR}/third/pybind11/include)

    if (APPLE)
        set_target_properties(${PY_LIBRARY_NAME} PROPERTIES LINK_FLAGS "-undefined dynamic_lookup")
    endif ()

    target_link_libraries(${PY_LIBRARY_NAME} PUBLIC ${SEETAFACE_LIBS})

    if (MSVC)
        target_link_libraries(${PY_LIBRARY_NAME} PRIVATE ${PYTHON_LIBRARIES})
        target_compile_options(${PY_LIBRARY_NAME}
                PRIVATE /MP
                /wd4244 # 'argument': conversion from 'google::
                # protobuf::uint64' to 'int', possible
                # loss of data
                /wd4267 # Conversion from 'size_t' to 'int',
                # possible loss of data
                /wd4996 # The second parameter is ignored.
                ${EXTRA_FLAGS})
        target_compile_options(${PY_LIBRARY_NAME} PRIVATE $<$<NOT:$<CONFIG:Debug>>:/MT> $<$<CONFIG:Debug>:/MTd>)
    endif ()
endif (BUILD_PYTHON)