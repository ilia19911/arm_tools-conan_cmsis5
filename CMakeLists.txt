cmake_minimum_required(VERSION 3.28)

project(cmsis C  ASM)

if(CMAKE_CROSSCOMPILING)

    option(HARDFP OFF)
    ADD_GLOB_COMPILE_OPTIONS(${ARM_CPU})
else ()
    message("BUILDING FOR ITSELF")
    option(HOST "Build for host" ON)
    set(ARM_CPU cortex-m7)
    set(VERSION "1.0.0-PC")
endif ()

#option(CONFIGTABLE          "Configuration of table allowed"    ON)
##     When CONFIGTABLE is ON, select if all interpolation tables must be included
#option(ALLFAST              "All interpolation tables included" ON)
##     When CONFIGTABLE is ON, select if all FFT tables must be included
#option(ALLFFT               "All fft tables included"           ON)

message("ARM_CPU=" ${ARM_CPU})
message("VERSION=" ${VERSION})


set(ROOT ${CMAKE_CURRENT_LIST_DIR}/cmsis )

file(READ ${ROOT}/CMSIS/DSP/Source/CMakeLists.txt file_content)

string(REPLACE "target_include_directories"  "#target_include_directories" file_content "${file_content}")

file(WRITE ${ROOT}/CMSIS/DSP/Source/CMakeLists.txt  "${file_content}")

set(MY_LIST "CMSISDSPBasicMath;CMSISDSPBayes;CMSISDSPCommon;CMSISDSPComplexMath;CMSISDSPController;CMSISDSPDistance;CMSISDSPFastMath;CMSISDSPFiltering;CMSISDSPInterpolation;CMSISDSPMatrix;CMSISDSPTransform;CMSISDSPSVM;CMSISDSPSupport;CMSISDSPStatistics;CMSISDSPQuaternionMath;cmsis-nn")
#set(MCU_LIST "cortex-m0; cortex-m1; cortex-m3; cortex-m4; cortex-m7")
if(${ARM_CPU} STREQUAL cortex-m0 )
    set(SUFFIX "_M0")
elseif (${ARM_CPU} STREQUAL cortex-m1)
    set(SUFFIX "_M1")
elseif (${ARM_CPU} STREQUAL cortex-m3)
    set(SUFFIX "_M3")
elseif (${ARM_CPU} STREQUAL cortex-m4)
    set(SUFFIX "_M4")
elseif (${ARM_CPU} STREQUAL cortex-m7)
    set(SUFFIX "_M7")
endif ()
set(LIB_NAME CMSIS${SUFFIX})
set(CMSIS_5_INCLUDE_DIRS
        "${ROOT}/CMSIS/Core/Include"
        "${ROOT}/CMSIS/DSP/Include"
        "${ROOT}/CMSIS/NN/Include"
        "${ROOT}/CMSIS/RTOS2/Include"
)

function(CHANGE_INCLUDE_TO_PRIVATE TARGET NEW_STATUS)
    # Изменяем свойство INTERFACE_INCLUDE_DIRECTORIES на новое значение
    get_target_property(existing_includes ${TARGET} INTERFACE_INCLUDE_DIRECTORIES)
    set_target_properties(${TARGET} PROPERTIES INTERFACE_INCLUDE_DIRECTORIES "")
    target_include_directories(${TARGET} ${NEW_STATUS} ${existing_includes})
endfunction()

function(copy_target_properties source_target dest_target)
    # Копируем исходные файлы
    get_target_property(sources ${source_target} SOURCES)
    add_library(${dest_target} STATIC ${sources})

    # Копируем include-директории
    get_target_property(include_dirs ${source_target} INCLUDE_DIRECTORIES)
    target_include_directories(${dest_target} PRIVATE ${include_dirs})

    # Копируем compile options
    get_target_property(compile_options ${source_target} COMPILE_OPTIONS)
    target_compile_options(${dest_target} PRIVATE ${compile_options})

    # Копируем compile definitions
    get_target_property(compile_definitions ${source_target} COMPILE_DEFINITIONS)
    target_compile_definitions(${dest_target} PRIVATE ${compile_definitions})

    # Копируем линковочные библиотеки
    get_target_property(link_libraries ${source_target} LINK_LIBRARIES)
    target_link_libraries(${dest_target} PRIVATE ${link_libraries})

    # Копируем compile features (если есть)
    get_target_property(compile_features ${source_target} COMPILE_FEATURES)
    if(compile_features)
        target_compile_features(${dest_target} PRIVATE ${compile_features})
    endif()

    # Копируем другие нужные свойства аналогичным образом...
endfunction()

add_subdirectory(${ROOT}/CMSIS/DSP/Source DSP_bin)
add_subdirectory(${ROOT}/CMSIS/NN NN_bin)



install(DIRECTORY ${ROOT}/CMSIS/Core/Include/
        DESTINATION ${CMAKE_INSTALL_PREFIX}/Include/Core
        FILES_MATCHING PATTERN "*.h"
)
install(DIRECTORY ${ROOT}/CMSIS/DSP/Include/
        DESTINATION ${CMAKE_INSTALL_PREFIX}/Include/DSP
        FILES_MATCHING PATTERN "*.h"
)
install(DIRECTORY ${ROOT}/CMSIS/NN/Include/
        DESTINATION ${CMAKE_INSTALL_PREFIX}/Include/NN
        FILES_MATCHING PATTERN "*.h"
)
install(DIRECTORY ${ROOT}/CMSIS/RTOS2/Include/
        DESTINATION ${CMAKE_INSTALL_PREFIX}/Include/RTOS2
        FILES_MATCHING PATTERN "*.h"
)


add_library(${LIB_NAME} INTERFACE)
target_include_directories(${LIB_NAME} INTERFACE
        "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/CMSIS/Core/Include>"
        "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/CMSIS/DSP/Include>"
        "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/CMSIS/NN/Include>"
        "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/CMSIS/RTOS2/Include>"
        "$<INSTALL_INTERFACE:${CMAKE_INSTALL_PREFIX}/Include/Core>"
        "$<INSTALL_INTERFACE:${CMAKE_INSTALL_PREFIX}/Include/DSP>"
        "$<INSTALL_INTERFACE:${CMAKE_INSTALL_PREFIX}/Include/NN>"
        "$<INSTALL_INTERFACE:${CMAKE_INSTALL_PREFIX}/Include/RTOS2>"
)

foreach(item IN LISTS MY_LIST)
    target_include_directories(${item} PRIVATE ${CMSIS_5_INCLUDE_DIRS})
    CHANGE_INCLUDE_TO_PRIVATE(${item} PRIVATE)

#    foreach(mcu IN LISTS MCU_LIST)
#        add_library(${mcu}${item} STATIC)
#        copy_target_properties(${item} ${mcu}${item})
#    endforeach ()

endforeach ()
#CHANGE_INCLUDE_TO_PRIVATE(CMSISDSP INTERFACE)
target_link_libraries(${LIB_NAME} INTERFACE CMSISDSP)

install(TARGETS ${LIB_NAME}
        ${MY_LIST}
        CMSISDSP
        EXPORT ${LIB_NAME}Targets
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib
        RUNTIME DESTINATION bin
        INCLUDES DESTINATION ""
)

include(CMakePackageConfigHelpers)
write_basic_package_version_file(
        ${LIB_NAME}ConfigVersion.cmake
        VERSION ${VERSION}
        COMPATIBILITY AnyNewerVersion
)

install(EXPORT ${LIB_NAME}Targets
        FILE ${LIB_NAME}Config.cmake
        NAMESPACE BREO::
        DESTINATION lib/cmake/
)

install(FILES
        "${CMAKE_CURRENT_BINARY_DIR}/${LIB_NAME}ConfigVersion.cmake"
        DESTINATION lib/cmake/
)




message("CMAKE_STATIC_LINKER_FLAGS: " ${CMAKE_STATIC_LINKER_FLAGS})
message("HARDFP is:" ${HARDFP})

#add_subdirectory(Test)