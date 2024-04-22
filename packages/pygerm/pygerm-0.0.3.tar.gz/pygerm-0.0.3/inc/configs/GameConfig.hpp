//
// Created by Jeremy Liu on 4/13/24.
//

#ifndef PYGERM_GAMECONFIG_HPP
#define PYGERM_GAMECONFIG_HPP

#include <string>
#include <filesystem>
#include <iostream>
#include <unordered_set>

#include <pybind11/pybind11.h>
#include "rapidjson/document.h"

#include "EngineUtils.hpp"

namespace py = pybind11;

const std::string DEFAULT_GAME_TITLE = "PyGerm Game";

class GameConfig {
public:
    std::string game_title;

    GameConfig();
    GameConfig(py::kwargs kwargs);
    GameConfig(std::string config_path);

    std::string to_string();
};


#endif //PYGERM_GAMECONFIG_HPP
