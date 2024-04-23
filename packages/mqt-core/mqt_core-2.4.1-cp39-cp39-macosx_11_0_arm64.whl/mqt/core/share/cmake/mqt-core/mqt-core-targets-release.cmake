#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "MQT::Core" for configuration "Release"
set_property(TARGET MQT::Core APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(MQT::Core PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libmqt-core.a"
  )

list(APPEND _cmake_import_check_targets MQT::Core )
list(APPEND _cmake_import_check_files_for_MQT::Core "${_IMPORT_PREFIX}/lib/libmqt-core.a" )

# Import target "MQT::CoreDD" for configuration "Release"
set_property(TARGET MQT::CoreDD APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(MQT::CoreDD PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libmqt-core-dd.a"
  )

list(APPEND _cmake_import_check_targets MQT::CoreDD )
list(APPEND _cmake_import_check_files_for_MQT::CoreDD "${_IMPORT_PREFIX}/lib/libmqt-core-dd.a" )

# Import target "MQT::CoreZX" for configuration "Release"
set_property(TARGET MQT::CoreZX APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(MQT::CoreZX PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libmqt-core-zx.a"
  )

list(APPEND _cmake_import_check_targets MQT::CoreZX )
list(APPEND _cmake_import_check_files_for_MQT::CoreZX "${_IMPORT_PREFIX}/lib/libmqt-core-zx.a" )

# Import target "MQT::CoreECC" for configuration "Release"
set_property(TARGET MQT::CoreECC APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(MQT::CoreECC PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libmqt-core-ecc.a"
  )

list(APPEND _cmake_import_check_targets MQT::CoreECC )
list(APPEND _cmake_import_check_files_for_MQT::CoreECC "${_IMPORT_PREFIX}/lib/libmqt-core-ecc.a" )

# Import target "MQT::CorePython" for configuration "Release"
set_property(TARGET MQT::CorePython APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(MQT::CorePython PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libmqt-core-python.a"
  )

list(APPEND _cmake_import_check_targets MQT::CorePython )
list(APPEND _cmake_import_check_files_for_MQT::CorePython "${_IMPORT_PREFIX}/lib/libmqt-core-python.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
