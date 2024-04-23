//
//  GameEngineUtils.cpp
//  game_engine
//
//  Created by Jeremy Liu on 1/30/24.
//

#include "EngineUtils.hpp"

void EngineUtils::read_json_file(const std::string &path, rapidjson::Document &out_document) {
    FILE* file_pointer = nullptr;
    
#ifdef _WIN32
    fopen_s(&file_pointer, path.c_str(), "rb");
#else
    file_pointer = fopen(path.c_str(), "rb");
#endif
    
    char buffer[65536];
    rapidjson::FileReadStream stream(file_pointer, buffer, sizeof(buffer));
    out_document.ParseStream(stream);
    std::fclose(file_pointer);

    if (out_document.HasParseError()) {
        // rapidjson::ParseErrorCode errorCode = out_document.GetParseError();
        std::cout << "error parsing json at [" << path << "]" << std::endl;
        exit(0);
    }
}

std::string EngineUtils::obtain_word_after_phrase(const std::string &input, const std::string &phrase) {
    // Find the position of the phrase in the string
    size_t pos = input.find(phrase);
    
    // If phrase is not found, return an empty string
    if (pos == std::string::npos) return "";
    
    // Find the starting position of the next word (skip spaces after the phrase)
    pos += phrase.length();
    while (pos < input.size() && std::isspace(input [pos])) {
        ++pos;
    }
    
    // If we're at the end of the string, return an empty string if (pos == input.size()) return "";
    if(pos == input.size()) return "";
    
    // Find the end position of the word (until a space or the end of the string)
    size_t endPos = pos;
    while (endPos < input.size() && !std::isspace(input[endPos])) {
        ++endPos;
    }
    // Extract and return the word
    return input.substr(pos, endPos - pos);
}

template <typename T>
void EngineUtils::process_json_object(const rapidjson::Value &json, std::unordered_map<std::string, T> &store) {
    for (auto iter = json.MemberBegin(); iter != json.MemberEnd(); ++iter) {
        std::string key = iter->name.GetString();
        if (iter->value.IsString()) {
            store[key] = iter->value.GetString();
        } else if (iter->value.IsInt()) {
            store[key] = iter->value.GetInt();
        } else if (iter->value.IsFloat()) {
            store[key] = iter->value.GetFloat();
        } else {
            std::cout << "UNKNOWN TYPE HANDLED YET" << std::endl;
            exit(0);
        }
    }
}

void EngineUtils::print_lua_error(const std::string &actor_name, const luabridge::LuaException &e) {
    std::string error_message = e.what();

    std::replace(error_message.begin(), error_message.end(), '\\', '/');
    std::cout << "\33[31m" << actor_name << " : " << error_message.substr(2) << "\33[0m" << std::endl;
}