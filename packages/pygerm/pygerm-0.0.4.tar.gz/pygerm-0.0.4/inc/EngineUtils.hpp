//
//  GameEngineUtils.hpp
//  game_engine
//
//  Created by Jeremy Liu on 1/30/24.
//

#ifndef GameEngineUtils_hpp
#define GameEngineUtils_hpp

#include <algorithm>
#include <stdio.h>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
#include <unordered_map>
#include <variant>

#include "rapidjson/document.h"
#include "rapidjson/filereadstream.h"
#include "SDL2/SDL.h"
#include "lua/lua.hpp"
#include "LuaBridge/LuaBridge.h"


class EngineUtils {
public:
    static void read_json_file(const std::string &path, rapidjson::Document &out_document);
    static std::string obtain_word_after_phrase(const std::string &input, const std::string &phrase);
    
    template <typename T>
    static void process_json_object(const rapidjson::Value &json, std::unordered_map<std::string, T> &store);

    static void print_lua_error(const std::string &actor_name, const luabridge::LuaException &e);
};

#endif /* GameEngineUtils_hpp */
