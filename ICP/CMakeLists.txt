cmake_minimum_required(VERSION 3.13)
project(SfMToolkitICP)


set(CMAKE_CXX_STANDARD 14)

find_package(libpointmatcher REQUIRED)

include_directories(${CMAKE_CURRENT_BINARY_DIR} ${libpointmatcher_INCLUDE_DIRS})

add_executable(${PROJECT_NAME} SfMToolkitICP.cpp)
message(STATUS "Using libpointmatcher version ${libpointmatcher_VERSION}")

target_link_libraries(${PROJECT_NAME} ${libpointmatcher_LIBRARIES})

install(TARGETS ${PROJECT_NAME} RUNTIME DESTINATION bin )