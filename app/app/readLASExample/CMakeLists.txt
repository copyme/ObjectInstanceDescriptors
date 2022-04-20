### CMakeLists.txt ---
##
##

project(readLASExample)

## #############################################################################
## Dependencies
## #############################################################################

find_package(LASlib REQUIRED)

## #############################################################################
## Sources
## #############################################################################

set(${PROJECT_NAME}_SOURCES
  main.cpp)


## #############################################################################
##
## #############################################################################

add_executable(${PROJECT_NAME}
  ${${PROJECT_NAME}_SOURCES})

target_link_libraries(${PROJECT_NAME} CGAL)
#target_link_libraries(${PROJECT_NAME} CGAL::LasLIB_support)
target_link_libraries(${PROJECT_NAME} LASlib)

######################################################################
### CMakeLists.txt ends here
