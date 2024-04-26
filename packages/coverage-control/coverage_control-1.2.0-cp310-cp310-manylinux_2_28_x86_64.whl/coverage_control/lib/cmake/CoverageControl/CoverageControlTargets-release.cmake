#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "CoverageControl::CoverageControl" for configuration "Release"
set_property(TARGET CoverageControl::CoverageControl APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(CoverageControl::CoverageControl PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/coverage_control/lib/libCoverageControl.so"
  IMPORTED_SONAME_RELEASE "libCoverageControl.so"
  )

list(APPEND _cmake_import_check_targets CoverageControl::CoverageControl )
list(APPEND _cmake_import_check_files_for_CoverageControl::CoverageControl "${_IMPORT_PREFIX}/coverage_control/lib/libCoverageControl.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
