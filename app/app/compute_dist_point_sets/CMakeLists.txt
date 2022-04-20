### CMakeLists.txt ---
##

project(compute_dist_point_sets)

## #############################################################################
## Sources
## #############################################################################

set(${PROJECT_NAME}_SOURCES
  main.cpp)

## #################################################################
## Dependencies - external
## #################################################################

# Qt5 is needed for CGAL Basic viewer
find_package(CGAL REQUIRED OPTIONAL_COMPONENTS Qt5)

## #############################################################################
##
## #############################################################################

add_executable(${PROJECT_NAME}
  ${${PROJECT_NAME}_SOURCES})

target_link_libraries(${PROJECT_NAME} PUBLIC CGAL::CGAL_Basic_viewer)

######################################################################
### CMakeLists.txt ends here
