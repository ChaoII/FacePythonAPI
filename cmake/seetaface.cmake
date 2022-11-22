if (WIN32)
    set(DEP_LIBS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/third/seeta/lib/win")
    file(GLOB SEETAFACE_LIBS ${DEP_LIBS_DIR}/*.lib)
    set(PLATFORM_DIR win)
elseif (APPLE)
    set(DEP_LIBS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/third/seeta/lib/mac")
    file(GLOB SEETAFACE_LIBS ${DEP_LIBS_DIR}/*.dylib)
    set(PLATFORM_DIR mac)
elseif (UNIX)
    set(DEP_LIBS_DIR "${CMAKE_CURRENT_SOURCE_DIR}/third/seeta/lib/linux")
    file(GLOB SEETAFACE_LIBS ${DEP_LIBS_DIR}/*.so)
    set(PLATFORM_DIR linux)
else ()
    message(FATAL_ERROR "unsupported this system")
endif ()
# 设置包含目录
set(SEETAFACE_INC_DIR ${CMAKE_CURRENT_SOURCE_DIR}/third/seeta/include)
include_directories(${SEETAFACE_INC_DIR})
# 添加外部库
list(APPEND DEPEND_LIBS ${SEETAFACE_LIBS})
# 拷贝文件
if (WIN32)
    file(GLOB SEETAFACE_LIBS ${DEP_LIBS_DIR}/*.dll)
endif ()
file(COPY ${SEETAFACE_LIBS} DESTINATION ${LIBRARY_OUTPUT_PATH} FOLLOW_SYMLINK_CHAIN)

if (USE_GPU)
    if (WIN32)
        add_custom_command(
                TARGET ${PROJECT_NAME} POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy
                ${LIBRARY_OUTPUT_PATH}/tennis_gpu.dll ${LIBRARY_OUTPUT_PATH}/tennis.dll)
        add_custom_command(
                TARGET ${PROJECT_NAME} POST_BUILD COMMAND ${CMAKE_COMMAND} -E rm -rf
                ${LIBRARY_OUTPUT_PATH}/tennis_gpu.dll)
    elseif (UNIX AND NOT APPLE)
        add_custom_command(
                TARGET ${PROJECT_NAME} POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy
                ${LIBRARY_OUTPUT_PATH}/libtennis_gpu.so ${LIBRARY_OUTPUT_PATH}/libtennis.so)
        add_custom_command(
                TARGET ${PROJECT_NAME} POST_BUILD COMMAND ${CMAKE_COMMAND} -E rm -rf
                ${LIBRARY_OUTPUT_PATH}/libtennis_gpu.so)
    else ()
        message(WARNING "GPU is supported only by windows and linux , USE_GPU will be turn off")
        set(USE_GPU OFF)
    endif ()
endif ()
