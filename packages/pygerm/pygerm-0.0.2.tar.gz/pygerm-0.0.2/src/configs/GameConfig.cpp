//
// Created by Jeremy Liu on 4/13/24.
//

#include "GameConfig.hpp"

GameConfig::GameConfig() : game_title(DEFAULT_GAME_TITLE) {}

GameConfig::GameConfig(py::kwargs kwargs) {
    if (kwargs.contains("game_title")) {
        game_title = kwargs["game_title"].cast<std::string>();
    }

    std::unordered_set<std::string> valid_keys = {"game_title"};
    for (auto item : kwargs) {
        if (valid_keys.find(item.first.cast<std::string>()) == valid_keys.end()) {
            throw std::runtime_error("Invalid key: " + item.first.cast<std::string>());
        }
    }
}

std::string GameConfig::to_string() {
    return "GameConfig(game_title=\"" + game_title + "\")";
}

GameConfig::GameConfig(std::string path) {
    if (!std::filesystem::exists(path)) {
        std::cout << "error: config file " << path << " does not exist";
        exit(0);
    }

    rapidjson::Document config_doc;
    EngineUtils::read_json_file(path, config_doc);

    game_title = config_doc.HasMember("game_title") ? config_doc["game_title"].GetString() : DEFAULT_GAME_TITLE;
}