cmake_minimum_required(VERSION 3.16)
project(pygerm)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O3 -fPIC")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -fPIC")

include_directories(inc inc/components inc/configs inc/scripting src src/components src/configs src/scripting extern)

# add pybind
#find_package(Python COMPONENTS Interpreter Development REQUIRED)
add_subdirectory(extern/pybind11)
include_directories(extern/pybind11/include)
include_directories(${PYTHON_INCLUDE_DIRS})

# add lua dependencies
file(GLOB LUA_SOURCE_FILES
    "extern/lua/*.c"
    "extern/lua/*.h"
)

add_library(lua STATIC ${LUA_SOURCE_FILES})

# add box2d dependencies
file(GLOB BOX2D_SOURCE_FILES
    "extern/box2d/include/box2d/*.h"
    "extern/box2d/src/collision/*.cpp"
    "extern/box2d/src/common/*.cpp"
    "extern/box2d/src/dynamics/*.h"
    "extern/box2d/src/dynamics/*.cpp"
    "extern/box2d/src/rope/*.cpp"
)
add_library(box2d STATIC ${BOX2D_SOURCE_FILES})
include_directories(extern/box2d/include extern/box2d/src)

find_package(SDL2 REQUIRED COMPONENTS SDL2)
find_package(SDL2_image REQUIRED)
find_package(SDL2_mixer REQUIRED)
find_package(SDL2_ttf REQUIRED)
include_directories(${SDL2_INCLUDE_DIRS} ${SDL2_IMAGE_INCLUDE_DIRS} ${SDL2_MIXER_INCLUDE_DIRS} ${SDL2_TTF_INCLUDE_DIRS})
link_libraries(${SDL2_LIBRARIES} ${SDL2_IMAGE_LIBRARIES} ${SDL2_MIXER_LIBRARIES} ${SDL2_TTF_LIBRARIES} lua box2d)

# link all files
file(GLOB SOURCES "src/*.cpp" "src/components/*.cpp" "src/configs/*.cpp" "src/scripting/*.cpp")
list(REMOVE_ITEM SOURCES "src/pygerm.cpp")
add_library(game_engine STATIC ${SOURCES})

pybind11_add_module(pygerm src/pygerm.cpp)
target_link_libraries(pygerm PRIVATE game_engine)























#file(GLOB SOURCES "src/*.cpp" "src/components/*.cpp")
#add_executable(game_engine_linux main.cpp ${SOURCES})

#IF (APPLE)
#    find_package(SDL2 REQUIRED COMPONENTS SDL2)
#    find_package(SDL2_image REQUIRED)
#    find_package(SDL2_mixer REQUIRED)
#    find_package(SDL2_ttf REQUIRED)
#    target_link_libraries(game_engine_linux SDL2::SDL2 SDL2_image::SDL2_image SDL2_ttf::SDL2_ttf SDL2_mixer::SDL2_mixer)
#ELSE ()
#    link_directories(${CMAKE_SOURCE_DIR}/bin/SDL2/extern/x64 ${CMAKE_SOURCE_DIR}/bin/SDL2_image/extern/x64 ${CMAKE_SOURCE_DIR}/bin/SDL2_mixer/extern/x64 ${CMAKE_SOURCE_DIR}/bin/SDL2_ttf/extern/x64)
#    include_directories(${CMAKE_SOURCE_DIR}/bin/SDL2/include ${CMAKE_SOURCE_DIR}/bin/SDL2_image/include ${CMAKE_SOURCE_DIR}/bin/SDL2_mixer/include ${CMAKE_SOURCE_DIR}/bin/SDL2_ttf/include)
#
#    target_link_libraries(game_engine_linux stdc++fs)
#    target_link_libraries(game_engine_linux SDL2 SDL2_image SDL2_mixer SDL2_ttf)
#ENDIF ()

#target_link_libraries(game_engine_linux lua box2d)
#
#set_target_properties(game_engine_linux PROPERTIES
#        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}
#)


# attempt at portable cmake file
#cmake_minimum_required(VERSION 3.16)
#project(GAME_ENGINE)
#set(CMAKE_CXX_STANDARD 17)
#set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O3")
#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")
#
#include(FetchContent)
#
#include_directories(inc)
#include_directories(src)
#
## fetch external dependencies
#function(fetch_dependency DEPENDENCY_NAME DEPENDENCY_URL)
#    FetchContent_Declare(
#            ${DEPENDENCY_NAME}
#            URL ${DEPENDENCY_URL}
#    )
#endfunction()
#
#set(SDL2IMAGE_INSTALL OFF)
#set(SDL2MIXER_INSTALL OFF)
#set(SDL2TTF_INSTALL OFF)
#
## get head only libraries
#fetch_dependency(GLM https://github.com/g-truc/glm/archive/refs/tags/0.9.9.8.tar.gz)
#fetch_dependency(RAPIDJSON https://github.com/Tencent/rapidjson/archive/refs/tags/v1.1.0.tar.gz)
#
## get SDL dependencies
#fetch_dependency(SDL2 https://github.com/libsdl-org/SDL/releases/download/release-2.28.5/SDL2-2.28.5.tar.gz)
#fetch_dependency(SDL_IMAGE https://github.com/libsdl-org/SDL_image/releases/download/release-2.6.3/SDL2_image-2.6.3.tar.gz)
#fetch_dependency(SDL_TTF https://github.com/libsdl-org/SDL_ttf/releases/download/release-2.20.2/SDL2_ttf-2.20.2.tar.gz)
#fetch_dependency(SDL_MIXER https://github.com/libsdl-org/SDL_mixer/releases/download/release-2.6.3/SDL2_mixer-2.6.3.tar.gz)
#
## get all fetch content
#FetchContent_MakeAvailable(GLM RAPIDJSON SDL2 SDL_IMAGE SDL_TTF SDL_MIXER)
#
## copy headers to correct location
#file(MAKE_DIRECTORY ${SDL2_image_SOURCE_DIR}/SDL2_image)
#file(COPY ${SDL2_image_SOURCE_DIR}/SDL_image.h DESTINATION ${SDL2_image_SOURCE_DIR}/SDL2_image)
#
#file(MAKE_DIRECTORY ${SDL2_ttf_SOURCE_DIR}/SDL2_ttf)
#file(COPY ${SDL2_ttf_SOURCE_DIR}/SDL_ttf.h DESTINATION ${SDL2_ttf_SOURCE_DIR}/SDL2_ttf)
#
#file(MAKE_DIRECTORY ${SDL2_mixer_SOURCE_DIR}/SDL2_mixer)
#file(COPY ${SDL2_mixer_SOURCE_DIR}/include/SDL_mixer.h DESTINATION ${SDL2_mixer_SOURCE_DIR}/SDL2_mixer)
#
## get lua and luabridge
#fetch_dependency(lua https://github.com/marovira/lua/archive/refs/tags/5.4.4.tar.gz)
#fetch_dependency(luabridge https://github.com/vinniefalco/LuaBridge/archive/refs/tags/2.8.tar.gz)
#FetchContent_MakeAvailable(lua luabridge)
#
## copy lua headers to correct location, build lua, and update luabridge source code to support more parameters
#file(REMOVE ${lua_SOURCE_DIR}/src/lua.c)
#file(REMOVE ${lua_SOURCE_DIR}/src/luac.c)
#file(MAKE_DIRECTORY ${lua_SOURCE_DIR}/lua)
#file(GLOB LUA_HEADERS ${lua_SOURCE_DIR}/src/*.h ${lua_SOURCE_DIR}/src/*.hpp)
#foreach(header ${LUA_HEADERS})
#    file(COPY ${header} DESTINATION ${lua_SOURCE_DIR}/lua)
#endforeach()
#
#file(REMOVE ${luabridge_SOURCE_DIR}/Source/LuaBridge/detail/FuncTraits.h)
#file(COPY lib/FuncTraits.h DESTINATION ${luabridge_SOURCE_DIR}/Source/LuaBridge/detail)
#
#file(GLOB LUA_SOURCE_FILES
#    "lib/lua/*.c"
#    "lib/lua/*.h"
#)
#add_library(lua STATIC ${LUA_SOURCE_FILES})
#
#
## build and link everything
#file(GLOB SOURCES "src/*.cpp")
#add_executable(game_engine_linux main.cpp ${SOURCES})
#set_target_properties(game_engine_linux PROPERTIES
#        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}
#)
#
#target_include_directories(game_engine_linux PRIVATE
#        ${glm_SOURCE_DIR}
#        ${rapidjson_SOURCE_DIR}/include
#        ${SDL2_SOURCE_DIR}/include
#        ${SDL2_image_SOURCE_DIR}
#        ${SDL2_ttf_SOURCE_DIR}
#        ${SDL2_mixer_SOURCE_DIR}
#        ${SDL2_mixer_SOURCE_DIR}/include
#        ${lua_SOURCE_DIR}
#        ${luabridge_SOURCE_DIR}/Source
#        ${luabridge_SOURCE_DIR}/Source/LuaBridge
#)
#
#target_link_libraries(game_engine_linux PRIVATE
#        SDL2
#        SDL2_image
#        SDL2_ttf
#        SDL2_mixer
#        lua
#)
