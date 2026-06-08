cmake_minimum_required(VERSION 3.10)
project(print)

set(PRINT_VERSION_MAJOR 0)
set(PRINT_VERSION_MINOR 1)
set(PRINT_VERSION_PATCH 0)
set(PRINT_VERSION_TWEAK 0)
set(PRINT_VERSION ${PRINT_VERSION_MAJOR}.${PRINT_VERSION_MINOR}.${PRINT_VERSION_PATCH}.${PRINT_VERSION_TWEAK})
set(PRINT_VERSION_STRING "v${PRINT_VERSION}")

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(print STATIC sources/print.cpp)
target_include_directories(print PUBLIC include)

option(BUILD_TESTS "Build tests" OFF)

if(BUILD_TESTS)
    enable_testing()
    find_package(GTest REQUIRED)
    
    file(GLOB TEST_SOURCES tests/*.cpp)
    add_executable(check ${TEST_SOURCES})
    target_link_libraries(check print GTest::gtest_main)
    target_include_directories(check PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
    add_test(NAME check COMMAND check)
endif()

add_executable(demo demo/main.cpp)
target_link_libraries(demo print)

install(TARGETS print DESTINATION lib)
install(DIRECTORY include/ DESTINATION include)
install(TARGETS demo RUNTIME DESTINATION bin)
