//
//  Actor.hpp
//  game_engine
//
//  Created by Jeremy Liu on 1/31/24.
//

#ifndef Actor_hpp
#define Actor_hpp

#include <iostream>
#include <stdio.h>
#include <string>
#include <optional>
#include <unordered_set>
#include <map>
#include <memory>
#include <queue>
#include <vector>
#include <filesystem>
#include <unordered_map>

#include "glm/glm.hpp"
#include "rapidjson/document.h"
#include "SDL2/SDL.h"
#include <pybind11/pybind11.h>

#include "EngineUtils.hpp"
#include "ComponentEngine.hpp"
#include "Component.hpp"
#include "LuaComponent.hpp"

namespace py = pybind11;
const inline std::string DEFAULT_ACTOR_NAME = "New Actor";

class Collision;

class Actor {
private:
    inline static int global_id_counter = 0;
    static inline std::unordered_map<std::string, std::shared_ptr<Actor>> template_store;

    std::map<std::string, std::shared_ptr<py::object>> components_to_add;
    std::map<std::string, std::shared_ptr<py::object>> components;
    std::map<std::string, std::shared_ptr<py::object>> components_to_remove;

    void process_actor_init();

    // caching data structures (could try to reduce in the future?)
    void process_event(const std::string &event_name, std::map<std::string, std::weak_ptr<py::object>> &components_with_event);
    void process_event_with_args(const std::string &event_name, std::map<std::string, std::weak_ptr<py::object>> &components_with_event, const Collision &collision) {};
    std::map<std::string, std::weak_ptr<py::object>> components_with_on_update;
    std::map<std::string, std::weak_ptr<py::object>> components_with_on_late_update;
    std::map<std::string, std::weak_ptr<py::object>> components_with_on_collision_enter;
    std::map<std::string, std::weak_ptr<py::object>> components_with_on_collision_exit;
    std::map<std::string, std::weak_ptr<py::object>> components_with_on_trigger_enter;
    std::map<std::string, std::weak_ptr<py::object>> components_with_on_trigger_exit;

    std::unordered_map<std::string, std::weak_ptr<py::object>> component_key_cache;
    std::unordered_map<std::string, std::deque<std::weak_ptr<py::object>>> component_type_cache;

public:
    bool enabled = true;
    int actor_id;
    std::string name;
    py::dict init_component_map;
    
    Actor();
    Actor(const std::string &actor_name, py::dict components);
    Actor(py::kwargs kwargs);

    Actor(const Actor &actor);
    Actor(const Actor &&other) noexcept;
    void operator=(const Actor &actor);


    // LEGACY CODE
    Actor(const std::string &actor_name) {};
    Actor(const rapidjson::Value &actor_json) {};
    ~Actor() {};

    std::string get_name();
    int get_id();
    py::object get_component_by_key(const std::string &key_name);
    py::object get_component(py::object);
    py::list get_components(py::object);

    py::object add_component(py::object);
    void remove_component(py::object);
    void disable_all_components() {};

    // template management
    static std::shared_ptr<Actor> get_template_actor(const std::string &) {};

    // component and lifetime management
    void process_on_start();
    void process_on_update();
    void process_on_late_update();
    void process_on_destroy();

    // component trigger and collision management
    void process_on_collision_enter(const Collision &collision) {};
    void process_on_collision_exit(const Collision &collision) {};
    void process_on_trigger_enter(const Collision &collision) {};
    void process_on_trigger_exit(const Collision &collision) {};
};

#endif /* Actor_hpp */
