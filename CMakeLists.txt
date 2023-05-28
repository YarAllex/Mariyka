cmake_minimum_required(VERSION 3.25)
project(Mariyka)

find_package(PkgConfig)

pkg_check_modules(GTKMM gtkmm-4.0)

link_directories(
        ${GTKMM_LIBRARY_DIRS}
)

include_directories(
        ${GTKMM_INCLUDE_DIRS}
)

set(CMAKE_CXX_STANDARD 17)

add_executable(Mariyka main.cpp MainWindow.cpp MainWindow.h)

target_link_libraries(Mariyka
        ${GTKMM_LIBRARIES}  )
