#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "pybind11_numpy_example::pybind11_numpy_example" for configuration "Release"
set_property(TARGET pybind11_numpy_example::pybind11_numpy_example APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(pybind11_numpy_example::pybind11_numpy_example PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/pybind11_numpy_example.lib"
  )

list(APPEND _cmake_import_check_targets pybind11_numpy_example::pybind11_numpy_example )
list(APPEND _cmake_import_check_files_for_pybind11_numpy_example::pybind11_numpy_example "${_IMPORT_PREFIX}/lib/pybind11_numpy_example.lib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
