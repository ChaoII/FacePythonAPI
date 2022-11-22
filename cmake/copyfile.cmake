if (WIN32)
    add_custom_command(
            TARGET ${LIBRARY_NAME} POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy
            ${LIBRARY_OUTPUT_PATH}/Release/FaceAPI.dll ${LIBRARY_OUTPUT_PATH}/FaceAPI.dll)
    add_custom_command(
            TARGET ${LIBRARY_NAME} POST_BUILD COMMAND ${CMAKE_COMMAND} -E rm -rf
            ${LIBRARY_OUTPUT_PATH}/Release)
endif ()
message(${LIBRARY_OUTPUT_PATH})
add_custom_command(
        TARGET ${LIBRARY_NAME} POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CMAKE_BINARY_DIR}/lib/
        ${CMAKE_CURRENT_SOURCE_DIR}/python/lib)
add_custom_command(
        TARGET ${LIBRARY_NAME} POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CMAKE_CURRENT_SOURCE_DIR}/model ${CMAKE_CURRENT_SOURCE_DIR}/python/model)