set(ROOT ${CMAKE_CURRENT_LIST_DIR}/../cmsis)
set(CMSIS_DIR ROOT CACHE STRING "cmsis_5 root directory")

add_subdirectory(${ROOT}/CMSIS/DSP/Source DSP_bin)
add_subdirectory(${ROOT}/CMSIS/NN NN_bin)
message(STATUS "CMSIS ROOT IS: " ${ROOT})
set(CMSIS_5_INCLUDE_DIRS
        ${ROOT}/CMSIS/Core/Include
        ${ROOT}/CMSIS/DSP/Include
        ${ROOT}/CMSIS/NN/Include
        ${ROOT}/CMSIS/RTOS2/Include)

include_directories(${CMSIS_5_INCLUDE_DIRS})