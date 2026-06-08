cmake_minimum_required(VERSION 3.10)
project(lab05)
set(PRINT_VERSION_MAJOR 0)
set(PRINT_VERSION_MINOR 1)
set(PRINT_VERSION_PATCH 0)
set(PRINT_VERSION_TWEAK 0)
set(PRINT_VERSION ${PRINT_VERSION_MAJOR}.${PRINT_VERSION_MINOR}.${PRINT_VERSION_PATCH}.${PRINT_VERSION_TWEAK})
set(PRINT_VERSION_STRING "v${PRINT_VERSION}")

hunter_add_package(GTest)
find_package(GTest CONFIG REQUIRED)


set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

option(BUILD_TESTS "Build tests" OFF)

add_subdirectory(banking)

if(BUILD_TESTS)
    enable_testing()
    find_package(GTest REQUIRED)
    
    add_executable(check 
        tests/test_account.cpp
        tests/test_transaction.cpp
    )
    target_link_libraries(check banking GTest::GTest::main)
    target_include_directories(check PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
    add_test(NAME check COMMAND check)
endif()

add_executable(demo ${CMAKE_CURRENT_SOURCE_DIR}/demo/main.cpp)
target_link_libraries(demo print)
install(TARGETS demo RUNTIME DESTINATION bin)

include(CPackConfig.cmake)
