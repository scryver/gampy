cmake_minimum_required(VERSION 2.6)
project(game_core)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

# include(FindPkgConfig)

# find_package(OpenGL REQUIRED)

add_library(${PROJECT_NAME} SHARED
    src/wrapper.cpp
    src/math/matrix4.cpp
)

# pkg_search_module(SDL2 REQUIRED sdl2)
# pkg_search_module(GLEW REQUIRED glew)

include_directories(
    include
    include/math
    # ${SDL2_INCLUDE_DIRS}
    # ${GLEW_INCLUDE_DIRS}
)

# set(ALL_LIBS
#     ${OPENGL_LIBRARY}
#     ${SDL2_LIBRARIES}
#     ${GLEW_LIBRARIES}
# )

target_link_libraries(${PROJECT_NAME})

# add_executable(${PROJECT_NAME}
#     src/main.cpp
# )

# target_link_libraries(${PROJECT_NAME}
#     ${LIB_NAME}
# )
