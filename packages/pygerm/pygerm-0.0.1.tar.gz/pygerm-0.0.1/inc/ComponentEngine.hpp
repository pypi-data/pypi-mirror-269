//
//  ComponentEngine.hpp
//  game_engine
//
//  Created by Jeremy Liu on 2/28/24.
//

#ifndef ComponentEngine_hpp
#define ComponentEngine_hpp

#include <filesystem>
#include <memory>
#include <stdio.h>
#include <string>
#include <unordered_map>
#include <thread>

#include "lua/lua.hpp"
#include "LuaBridge/LuaBridge.h"
#include "box2d/box2d.h"
#include "box2d/b2_math.h"

#include "Input.hpp"
#include "GraphicsEngine.hpp"
#include "AudioEngine.hpp"
#include "Rigidbody.hpp"
#include "Raycast.hpp"
#include "EventBus.hpp"

class ComponentEngine {
private:
    
public:
    static void log_message(const std::string& s);
    static void log_error(const std::string& s);
    static void quit();
    static void sleep(int ms);
    static void open_url(const std::string &url);
    
    // lua plugin overhead
    static lua_State* lua_state;
    static void init_lua();
    static void establish_inheretance(luabridge::LuaRef &instance_table, const luabridge::LuaRef &parent_table);
    
    // general component assistance
    static std::shared_ptr<luabridge::LuaRef> get_component(std::string);
};

#endif /* ComponentEngine_hpp */
