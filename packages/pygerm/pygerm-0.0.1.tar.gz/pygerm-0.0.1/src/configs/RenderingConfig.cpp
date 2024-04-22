//
// Created by Jeremy Liu on 4/13/24.
//

#include "RenderingConfig.hpp"

RenderingConfig::RenderingConfig() {}

RenderingConfig::RenderingConfig(int x_res, int y_res, SDL_Color bg_color) : x_resolution(x_res), y_resolution(y_res), clear_color(bg_color) {}

RenderingConfig::RenderingConfig(py::kwargs kwargs) {
    if (kwargs.contains("x_resolution")) {
        x_resolution = kwargs["x_resolution"].cast<int>();
    }

    if (kwargs.contains("y_resolution")) {
        y_resolution = kwargs["y_resolution"].cast<int>();
    }

    if (kwargs.contains("zoom_factor")) {
        zoom_factor = kwargs["zoom_factor"].cast<float>();
    }

    if (kwargs.contains("clear_color")) {
        auto bg_color = kwargs["clear_color"].cast<SDL_Color>();
        clear_color = bg_color;
    }

    if (kwargs.contains("r")) {
        clear_color.r = kwargs["r"].cast<uint8_t>();
    }
    if (kwargs.contains("g")) {
        clear_color.g = kwargs["g"].cast<uint8_t>();
    }
    if (kwargs.contains("b")) {
        clear_color.b = kwargs["b"].cast<uint8_t>();
    }

    std::unordered_set<std::string> valid_keys = {"x_resolution", "y_resolution", "clear_color", "r", "g", "b", "zoom_factor"};
    for (auto item : kwargs) {
        if (valid_keys.find(item.first.cast<std::string>()) == valid_keys.end()) {
            throw std::runtime_error("Invalid key: " + item.first.cast<std::string>());
        }
    }
}

RenderingConfig::RenderingConfig(std::string config_path) {
    if (!std::filesystem::exists(config_path)) {
        std::cout << "error: config file " << config_path << " does not exist";
        exit(0);
    }

    rapidjson::Document config_doc;
    EngineUtils::read_json_file(config_path, config_doc);

    x_resolution = config_doc.HasMember("x_resolution") ? config_doc["x_resolution"].GetInt() : 100;
    y_resolution = config_doc.HasMember("y_resolution") ? config_doc["y_resolution"].GetInt() : 100;

    zoom_factor = config_doc.HasMember("zoom_factor") ? config_doc["zoom_factor"].GetFloat() : 1.0f;

    uint8_t r = config_doc.HasMember("clear_color_r") ? config_doc["clear_color_r"].GetInt() : 0;
    uint8_t g = config_doc.HasMember("clear_color_g") ? config_doc["clear_color_g"].GetInt() : 0;
    uint8_t b = config_doc.HasMember("clear_color_b") ? config_doc["clear_color_b"].GetInt() : 0;

    clear_color = {r, g, b, 255};

    if (config_doc.HasMember("clear_color") || config_doc.HasMember("color")) {
        std::cout << "error: please specify clear_color_r, clear_color_g, and clear_color_b separately";
        exit(0);
    }
}

std::string RenderingConfig::to_string() {
    return "RenderingConfig(x_resolution=" + std::to_string(x_resolution) + ", y_resolution=" + std::to_string(y_resolution) + ", clear_color=Color(" + std::to_string(clear_color.r) + ", " + std::to_string(clear_color.g) + ", " + std::to_string(clear_color.b) + ", " + std::to_string(clear_color.a) + "))";
}
