#cmake_minimum_required(VERSION 3.5)

#project(CmakeObjDesc VERSION 0.1 LANGUAGES CXX)

#set(CMAKE_INCLUDE_CURRENT_DIR ON)

#set(CMAKE_AUTOUIC ON)
#set(CMAKE_AUTOMOC ON)
#set(CMAKE_AUTORCC ON)

#set(CMAKE_CXX_STANDARD 17)
#set(CMAKE_CXX_STANDARD_REQUIRED ON)

#find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Widgets)
#find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Widgets)

#find_package(CGAL COMPONENTS Qt5 Core)

#include(${CGAL_USE_FILE})

#set(PROJECT_SOURCES
#        main.cpp
#        mainwindow.cpp
#        mainwindow.h
#        mainwindow.ui
#)

#if(${QT_VERSION_MAJOR} GREATER_EQUAL 6)
#    qt_add_executable(CmakeObjDesc
#        MANUAL_FINALIZATION
#        ${PROJECT_SOURCES}
#    )
## Define target properties for Android with Qt 6 as:
##    set_property(TARGET CmakeObjDesc APPEND PROPERTY QT_ANDROID_PACKAGE_SOURCE_DIR
##                 ${CMAKE_CURRENT_SOURCE_DIR}/android)
## For more information, see https://doc.qt.io/qt-6/qt-add-executable.html#target-creation
#else()
#    if(ANDROID)
#        add_library(CmakeObjDesc SHARED
#            ${PROJECT_SOURCES}
#        )
## Define properties for Android with Qt 5 after find_package() calls as:
##    set(ANDROID_PACKAGE_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/android")
#    else()
#        add_executable(CmakeObjDesc
#            ${PROJECT_SOURCES}
#        )
#    endif()
#endif()

#target_link_libraries(CmakeObjDesc PUBLIC CGAL::CGAL_Basic_viewer PRIVATE Qt${QT_VERSION_MAJOR}::Widgets)

#set_target_properties(CmakeObjDesc PROPERTIES
#    MACOSX_BUNDLE_GUI_IDENTIFIER my.example.com
#    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
#    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
#    MACOSX_BUNDLE TRUE
#    WIN32_EXECUTABLE TRUE
#)

#if(QT_VERSION_MAJOR EQUAL 6)
#    qt_finalize_executable(CmakeObjDesc)
#endif()


cmake_minimum_required(VERSION 3.5)

project(CmakeObjDesc LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

set(CMAKE_AUTOUIC OFF)
set(CMAKE_AUTOMOC OFF)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(QT NAMES Qt5 COMPONENTS Widgets REQUIRED)
find_package(Qt${QT_VERSION_MAJOR} COMPONENTS Widgets REQUIRED)
find_package(CGAL REQUIRED COMPONENTS Qt5 REQUIRED)


set(SOURCES mainwindow.cpp main.cpp)

QT5_WRAP_CPP(MOC_files mainwindow.h)

QT5_WRAP_UI(UI_files mainwindow.ui)

add_definitions(-DCGAL_USE_BASIC_VIEWER)


add_executable(CmakeObjDesc
  ${SOURCES}
  ${MOC_files}
  ${UI_files}

  ${CGAL_Qt5_RESOURCE_FILES} ${CGAL_Qt5_MOC_FILES}
  )

target_link_libraries(CmakeObjDesc PRIVATE Qt${QT_VERSION_MAJOR}::Widgets PUBLIC CGAL::CGAL_Qt5 CGAL::CGAL)

