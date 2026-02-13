cmake_minimum_required(VERSION 3.20)
project(test_cpr)

set(CMAKE_CXX_STANDARD 17)

find_package(cpr CONFIG REQUIRED)

add_executable(test main.cpp)
target_link_libraries(test PRIVATE cpr::cpr)
