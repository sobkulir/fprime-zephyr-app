
set(SOURCE_FILES "${CMAKE_CURRENT_LIST_DIR}/ZephyrMallocAllocator.cpp")

register_fprime_module()

target_link_libraries(Fw_ZephyrMallocAllocator PUBLIC zephyr_interface)