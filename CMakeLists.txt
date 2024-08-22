cmake_minimum_required(VERSION 3.28)

include(.stcproj/project_init.cmake)

project(cmsis C ASM)



set(ROOT ${CMAKE_CURRENT_LIST_DIR}/cmsis)
set(CMSIS_DIR ROOT CACHE STRING "cmsis_5 root directory")


message(STATUS "CMSIS ROOT IS: " ${ROOT})
set(CMSIS_5_INCLUDE_DIRS
        "${ROOT}/CMSIS/Core/Include"
        "${ROOT}/CMSIS/DSP/Include"
        "${ROOT}/CMSIS/NN/Include"
        "${ROOT}/CMSIS/RTOS2/Include")
include_directories(${CMSIS_5_INCLUDE_DIRS})
add_subdirectory(${ROOT}/CMSIS/DSP/Source)

add_subdirectory(${ROOT}/CMSIS/NN NN_bin)

add_library(CMSIS INTERFACE)

target_link_libraries(CMSIS INTERFACE CMSISDSP cmsis-nn)

ADD_GLOB_COMPILE_OPTIONS(cortex-m4)
message("cmsis include is:" ${CMSIS_5_INCLUDE_DIRS})


# Определяем цель установки
install(TARGETS CMSIS
        EXPORT CMSIS
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        RUNTIME DESTINATION bin
)