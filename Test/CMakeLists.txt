cmake_minimum_required(VERSION 3.28)

project(CMSIS_TEST C CXX ASM)

set(CMAKE_PREFIX_PATH ${CMAKE_CURRENT_SOURCE_DIR}/../install/lib/cmake ${CMAKE_PREFIX_PATH})
find_package(CMSIS_M7 REQUIRED)
add_executable(test ./main.cpp)
target_link_libraries(test PUBLIC CMSIS::CMSIS_M7 CMSIS::CMSISDSPCommon CMSIS::CMSISDSPTransform)