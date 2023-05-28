cmake_minimum_required(VERSION 3.25)
project(Mariyka)

find_package(PkgConfig)
pkg_check_modules(GTKMM gtkmm-4.0)
add_subdirectory(src)
