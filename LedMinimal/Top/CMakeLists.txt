####
# F prime CMakeLists.txt:
#
# SOURCE_FILES: combined list of source and autocoding files
# MOD_DEPS: (optional) module dependencies
####

set(SOURCE_FILES
  "${CMAKE_CURRENT_LIST_DIR}/instances.fpp"
  "${CMAKE_CURRENT_LIST_DIR}/LedMinimalPackets.xml"
  "${CMAKE_CURRENT_LIST_DIR}/topology.fpp"
  "${CMAKE_CURRENT_LIST_DIR}/LedMinimalTopology.cpp"
)
set(MOD_DEPS
  Fw/Logger
  Drv/ZephyrTime
)

register_fprime_module()
