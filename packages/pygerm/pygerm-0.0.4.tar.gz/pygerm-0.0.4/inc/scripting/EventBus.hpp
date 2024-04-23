//
//  EventBus.hpp
//  game_engine
//
//  Created by Jeremy Liu on 3/31/24.
//

#ifndef EventBus_hpp
#define EventBus_hpp

#include <string>
#include <stdio.h>
#include <unordered_map>
#include <vector>
#include <queue>

#include "lua/lua.hpp"
#include "LuaBridge/LuaBridge.h"

struct EventOwner {
    std::string event_name;
    luabridge::LuaRef component;
    luabridge::LuaRef callback;
};

class EventBus {
private:
    // pair <component, callback>
    static inline std::unordered_map<std::string, std::vector<std::pair<luabridge::LuaRef, luabridge::LuaRef>>> event_map;

    static inline std::queue<EventOwner> subscribe_queue;
    static inline std::queue<EventOwner> unsubscribe_queue;
public:
    static void publish (const std::string &event_name, luabridge::LuaRef event_object);
    static void subscribe (const std::string &event_name, luabridge::LuaRef component, luabridge::LuaRef callback);
    static void unsubscribe (const std::string &event_name, luabridge::LuaRef component, luabridge::LuaRef function);

    static void process_subscriptions();
};

#endif /* EventBus_hpp */
