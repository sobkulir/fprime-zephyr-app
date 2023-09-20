####
# F prime CMakeLists.txt:
#
# SOURCE_FILES: combined list of source and autocoding files
# MOD_DEPS: (optional) module dependencies
# UT_SOURCE_FILES: list of source files for unit tests
#
####
set(SOURCE_FILES
  "${CMAKE_CURRENT_LIST_DIR}/ZephyrTimeImpl.cpp"
)

# Uncomment and add any modules that this component depends on, else
# they might not be available when cmake tries to build this component.

set(MOD_DEPS
  Svc/Time
)

register_fprime_module()

# Because the component depends on compile-time generated zephyr header:
# `syscall_list.h`, solution taken from here: https://github.com/zephyrproject-rtos/zephyr/issues/32537#issuecomment-784042873
# target_link_libraries(Components_ZephyrTime PUBLIC zephyr_interface)
