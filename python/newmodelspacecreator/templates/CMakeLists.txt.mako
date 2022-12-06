# H2020 ESROCOS Project
# Company: GMV Aerospace & Defence S.A.U.
# Licence: GPLv2


cmake_minimum_required(VERSION 3.3)
# required version 3.3: provides "IN_LIST" operator in if()

project(${component_name} LANGUAGES C CXX)

include($ENV{ESROCOS_CMAKE})
esrocos_init()

# The project version number (for pkg-config)
set(VERSION_MAJOR   0   CACHE STRING "Project major version number.")
set(VERSION_MINOR   1   CACHE STRING "Project minor version number.")
set(VERSION_PATCH   0   CACHE STRING "Project patch version number.")
mark_as_advanced(VERSION_MAJOR VERSION_MINOR VERSION_PATCH)



#
# Required packages
#

# Code coverage (native only)
if(NOT CMAKE_CROSSCOMPILING)
    find_package(codecov REQUIRED)
    if (NOT ENABLE_COVERAGE)
        message(STATUS "Configure with -DENABLE_COVERAGE=On to collect coverage metrics")
    endif()
endif()

# Tests automation
include(CTest)

# POSIX threads (skip check if using RTEMS)
if(NOT CMAKE_CROSSCOMPILING)
    find_package(Threads REQUIRED)
endif()

add_subdirectory(model)

# Coverage for tests
if(NOT CMAKE_CROSSCOMPILING)
    coverage_evaluate()
endif()

