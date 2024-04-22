//
//  EventBus.cpp
//  game_engine
//
//  Created by Jeremy Liu on 3/31/24.
//

#include "EventBus.hpp"

void EventBus::publish(const std::string &event_name, luabridge::LuaRef event_object) {
    for (auto &listener : event_map[event_name]) {
        listener.second(listener.first, event_object);
    }
}

void EventBus::subscribe(const std::string &event_name, luabridge::LuaRef component, luabridge::LuaRef callback) {
    subscribe_queue.push({event_name, component, callback});
}

void EventBus::unsubscribe(const std::string &event_name, luabridge::LuaRef component, luabridge::LuaRef function) {
    unsubscribe_queue.push({event_name, component, function});
}

void EventBus::process_subscriptions() {
    while (!subscribe_queue.empty()) {
        EventOwner event_owner = subscribe_queue.front();
        event_map[event_owner.event_name].push_back({event_owner.component, event_owner.callback});
        subscribe_queue.pop();
    }

    while (!unsubscribe_queue.empty()) {
        EventOwner event_owner = unsubscribe_queue.front();
        for (int i = 0; i < event_map[event_owner.event_name].size(); i++) {
            if (event_map[event_owner.event_name][i].first == event_owner.component && event_map[event_owner.event_name][i].second == event_owner.callback) {
                event_map[event_owner.event_name].erase(event_map[event_owner.event_name].begin() + i);
                break;
            }
        }
        unsubscribe_queue.pop();
    }
}