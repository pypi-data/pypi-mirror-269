//
// Created by Jeremy Liu on 4/13/24.
//

#ifndef PYGERM_RENDERINGCONFIG_HPP
#define PYGERM_RENDERINGCONFIG_HPP

#include <string>
#include <iostream>
#include <filesystem>

#include "SDL2/SDL.h"
#include "rapidjson/document.h"
#include <pybind11/pybind11.h>

#include "EngineUtils.hpp"

namespace py = pybind11;

class RenderingConfig {
public:
    int x_resolution = 640;
    int y_resolution = 360;
    float zoom_factor = 1.0;
    SDL_Color clear_color = {255, 255, 255, 255};

    RenderingConfig();
    RenderingConfig(int x_res, int y_res, SDL_Color bg_color);
    RenderingConfig(py::kwargs kwargs);
    RenderingConfig(std::string config_path);

    std::string to_string();
};


#endif //PYGERM_RENDERINGCONFIG_HPP
