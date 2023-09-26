# Module subdirectories

# Ports
add_fprime_subdirectory("${CMAKE_CURRENT_LIST_DIR}/ZephyrGpioDriverPorts/")

# Components
add_fprime_subdirectory("${CMAKE_CURRENT_LIST_DIR}/ZephyrUartDriver")
add_fprime_subdirectory("${CMAKE_CURRENT_LIST_DIR}/ZephyrRateDriver")
add_fprime_subdirectory("${CMAKE_CURRENT_LIST_DIR}/ZephyrGpioDriver")
add_fprime_subdirectory("${CMAKE_CURRENT_LIST_DIR}/ZephyrTime")
