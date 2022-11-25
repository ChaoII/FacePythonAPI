if (WIN32)
    add_custom_command(
            TARGET ${LIBRARY_NAME} POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy
            ${LIBRARY_OUTPUT_PATH}/Release/FaceAPI.dll ${LIBRARY_OUTPUT_PATH}/FaceAPI.dll)
    add_custom_command(
            TARGET ${LIBRARY_NAME} POST_BUILD COMMAND ${CMAKE_COMMAND} -E rm -rf
            ${LIBRARY_OUTPUT_PATH}/Release)
endif ()
add_custom_command(
        TARGET ${LIBRARY_NAME} POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CMAKE_BINARY_DIR}/lib/
        ${CMAKE_CURRENT_SOURCE_DIR}/serving/lib)
add_custom_command(
        TARGET ${LIBRARY_NAME} POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CMAKE_CURRENT_SOURCE_DIR}/model ${CMAKE_CURRENT_SOURCE_DIR}/serving/model)

if (BUILD_PYTHON)
    message(${LIBRARY_OUTPUT_PATH})
    file(GLOB DEP_LIBS ${LIBRARY_OUTPUT_PATH}/*.*)
    file(COPY ${DEP_LIBS} DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/python/faceapi/libs FOLLOW_SYMLINK_CHAIN)
endif ()