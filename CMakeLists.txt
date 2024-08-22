cmake_minimum_required(VERSION 3.28)

include(.stcproj/project_init.cmake)

project(cmsis C ASM)

get_filename_component(ROOT ${CMAKE_CURRENT_LIST_DIR}/cmsis ABSOLUTE)
#set(CMSIS_DIR ROOT CACHE STRING "cmsis_5 root directory")

message(STATUS "CMSIS ROOT IS: " ${ROOT})
set(CMSIS_5_INCLUDE_DIRS
        "${ROOT}/CMSIS/Core/Include"
        "${ROOT}/CMSIS/DSP/Include"
        "${ROOT}/CMSIS/NN/Include"
        "${ROOT}/CMSIS/RTOS2/Include")

add_subdirectory(${ROOT}/CMSIS/DSP/Source DSP_bin)
target_include_directories(CMSISDSP INTERFACE ${CMSIS_5_INCLUDE_DIRS})
target_include_directories(CMSISDSPBasicMath PRIVATE ${CMSIS_5_INCLUDE_DIRS})
target_include_directories(CMSISDSPBayes PRIVATE ${CMSIS_5_INCLUDE_DIRS})
target_include_directories(CMSISDSPCommon PRIVATE ${CMSIS_5_INCLUDE_DIRS})
target_include_directories(CMSISDSPComplexMath PRIVATE ${CMSIS_5_INCLUDE_DIRS})
target_include_directories(CMSISDSPController PRIVATE ${CMSIS_5_INCLUDE_DIRS})
target_include_directories(CMSISDSPDistance PRIVATE ${CMSIS_5_INCLUDE_DIRS})
target_include_directories(CMSISDSPFastMath PRIVATE ${CMSIS_5_INCLUDE_DIRS})
target_include_directories(CMSISDSPFiltering PRIVATE ${CMSIS_5_INCLUDE_DIRS})
target_include_directories(CMSISDSPInterpolation PRIVATE ${CMSIS_5_INCLUDE_DIRS})
target_include_directories(CMSISDSPMatrix PRIVATE ${CMSIS_5_INCLUDE_DIRS})
target_include_directories(CMSISDSPTransform PRIVATE ${CMSIS_5_INCLUDE_DIRS})
target_include_directories(CMSISDSPSVM PRIVATE ${CMSIS_5_INCLUDE_DIRS})
target_include_directories(CMSISDSPSupport PRIVATE ${CMSIS_5_INCLUDE_DIRS})
target_include_directories(CMSISDSPStatistics PRIVATE ${CMSIS_5_INCLUDE_DIRS})
target_include_directories(CMSISDSPQuaternionMath PRIVATE ${CMSIS_5_INCLUDE_DIRS})

add_subdirectory(${ROOT}/CMSIS/NN NN_bin)

#add_library(CMSIS INTERFACE)
#target_include_directories(CMSIS INTERFACE $<INSTALL_INTERFACE:${CMSIS_5_INCLUDE_DIRS}>  )
#target_link_libraries(CMSIS INTERFACE cmsis-nn ) #CMSISDSP

ADD_GLOB_COMPILE_OPTIONS(cortex-m4)
message("cmsis include is:" ${CMSIS_5_INCLUDE_DIRS})


install(DIRECTORY ${ROOT}/CMSIS/Core/Include
        DESTINATION include/cmsis/Core
        FILES_MATCHING PATTERN "*.h"
)
install(DIRECTORY ${ROOT}/CMSIS/DSP/Include
        DESTINATION include/cmsis/DSP
        FILES_MATCHING PATTERN "*.h"
)
install(DIRECTORY ${ROOT}/CMSIS/NN/Include
        DESTINATION include/cmsis/NN
        FILES_MATCHING PATTERN "*.h"
)
install(DIRECTORY ${ROOT}/CMSIS/RTOS2/Include
        DESTINATION include/cmsis/RTOS2
        FILES_MATCHING PATTERN "*.h"
)

include_directories(
        "${CMAKE_INSTALL_PREFIX}/include/cmsis/Core"
        "${CMAKE_INSTALL_PREFIX}/include/cmsis/DSP"
        "${CMAKE_INSTALL_PREFIX}/include/cmsis/NN"
        "${CMAKE_INSTALL_PREFIX}/include/cmsis/RTOS2"
)
install(TARGETS cmsis-nn
        CMSISDSPBasicMath
        CMSISDSPBayes
        CMSISDSPCommon
        CMSISDSPComplexMath
        CMSISDSPController
        CMSISDSPDistance
        CMSISDSPFastMath
        CMSISDSPFiltering
        CMSISDSPInterpolation
        CMSISDSPMatrix
        CMSISDSPTransform
        CMSISDSPSVM
        CMSISDSPSupport
        CMSISDSPStatistics
        CMSISDSPQuaternionMath
        CMSISDSP
        EXPORT MyLibTargets
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib
        RUNTIME DESTINATION bin
        INCLUDES DESTINATION include
)

include(CMakePackageConfigHelpers)
write_basic_package_version_file(
        MyLibConfigVersion.cmake
        VERSION 5.9.1
        COMPATIBILITY AnyNewerVersion
)

install(EXPORT MyLibTargets
        FILE MyLibConfig.cmake
        NAMESPACE MyLib::
        DESTINATION lib/cmake/MyLib
)

install(FILES
        "${CMAKE_CURRENT_BINARY_DIR}/MyLibConfigVersion.cmake"
        DESTINATION lib/cmake/MyLib
)
