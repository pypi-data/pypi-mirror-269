
####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was CoverageControlConfig.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

set(PN CoverageControl)
set(${PN}_INCLUDE_DIR "${PACKAGE_PREFIX_DIR}/coverage_control/include")
set(${PN}_LIBRARY_DIR "${PACKAGE_PREFIX_DIR}/coverage_control/lib")
set(${PN}_LIBRARY "${${PN}_LIBRARY_DIR}/lib${PN}.so")
set(${PN}_DEFINITIONS USING_${PN})

if(NOT TARGET CoverageControl::${PN})
include("${CMAKE_CURRENT_LIST_DIR}/${PN}Targets.cmake")

find_package(OpenMP REQUIRED)
find_package(Eigen3 3.4 REQUIRED)

set(dependencies_list Eigen3::Eigen OpenMP::OpenMP_CXX)
target_link_libraries(CoverageControl::${PN} INTERFACE ${${PN}_LIBRARY} ${dependencies_list})

endif()
check_required_components(${PN})
