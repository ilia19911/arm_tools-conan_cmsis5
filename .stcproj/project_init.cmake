execute_process(
        COMMAND conan install ${CMAKE_CURRENT_LIST_DIR} -pr:h=${CMAKE_CURRENT_LIST_DIR}/conan_profile --output-folder=${CMAKE_BINARY_DIR}  #-r=BREO    --build missing
        RESULT_VARIABLE CONAN_INSTALL_RESULT
        OUTPUT_VARIABLE CONAN_INSTALL_OUTPUT
)
if(CONAN_INSTALL_RESULT)
    message(FATAL_ERROR "Conan install failed: ${CONAN_INSTALL_RESULT}")
endif()

#option(GCC_VERBOSE "Enable verbose GCC output" ON)
include(${CMAKE_BINARY_DIR}/conan_toolchain.cmake)
#string(TOLOWER ${SERIES} series)
#add_compile_definitions(HSE_VALUE=${HSE_VALUE} ${FVP_PLATFORM} ${DEVICE} SERIES=${series})