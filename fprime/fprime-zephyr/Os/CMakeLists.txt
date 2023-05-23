cmake_minimum_required(VERSION 3.13)
cmake_policy(SET CMP0079 NEW)

# message(FATAL_ERROR "Muhehehe")


if (${CMAKE_SYSTEM_NAME} STREQUAL "Zephyr")
    set(SOURCE_FILES
        # Common implementations
        "${FPRIME_FRAMEWORK_PATH}/Os/Pthreads/BufferQueueCommon.cpp"
        "${CMAKE_CURRENT_LIST_DIR}/BufferQueue.cpp"
        "${CMAKE_CURRENT_LIST_DIR}/Mutex.cpp"
        "${CMAKE_CURRENT_LIST_DIR}/Queue.cpp"
        "${CMAKE_CURRENT_LIST_DIR}/Task.cpp"
    )
    register_fprime_module(fprime-zephyr_Os)
endif()

####
# Dependency Melding:
#
# In short, this Os layer depends on the framework's Os layer and vise-versa. Effectively it is one
# library built in two halves, the framework base, and this add on. Here we make the link pointers
# depend on one another forming a (weak) circular dependency. This is allowed in CMake 3.13 and
# newer.
#
# Copied from: https://github.com/fprime-community/fprime-azure-threadx/blob/fprime-azure-threadx-cmjl-14-01-2022-v00/fprime-nucleo/NucleoOs/CMakeLists.txt
####
if (${CMAKE_SYSTEM_NAME} STREQUAL "Zephyr")
    add_dependencies(Os fprime-zephyr_Os)
    target_link_libraries(Os PRIVATE fprime-zephyr_Os)
    target_link_libraries(fprime-zephyr_Os PRIVATE Os)
endif()
