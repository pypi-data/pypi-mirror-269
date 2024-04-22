//
//  Scene.hpp
//  game_engine
//
//  Created by Jeremy Liu on 1/31/24.
//

#ifndef Scene_hpp
#define Scene_hpp

#include <memory>
#include <iostream>
#include <string>
#include <sstream>
#include <stdio.h>
#include <unordered_set>
#include <unordered_map>
#include <vector>
#include <map>
#include <algorithm>

#include "glm/glm.hpp"
#include "rapidjson/document.h"
#include "lua/lua.hpp"
#include "LuaBridge/LuaBridge.h"
#include "box2d/b2_world.h"
#include <pybind11/pybind11.h>

#include "Actor.hpp"
#include "GraphicsEngine.hpp"

namespace py = pybind11;

class Actor;

class Scene {
private:
    static inline std::string scene_name;
    static inline std::vector<std::shared_ptr<Actor>> persistent_actors;

    static inline std::vector<std::shared_ptr<Actor>> actors_to_add;
    static inline std::vector<std::shared_ptr<Actor>> actors;
    static inline std::vector<std::shared_ptr<Actor>> actors_to_remove;

    // caching and optimization for finding actors
    static inline std::unordered_map<std::string, std::deque<std::weak_ptr<Actor>>> actor_cache;

public:
    // physics in scene
    static inline b2World* box2d_world;

    // scene management
    static inline std::shared_ptr<Scene> next_scene = nullptr;

    static std::string get_current_scene();
    static void load(Scene scene);
    static void start_next_scene();
    static void dont_destroy_actor(Actor *actor_ptr);

    static std::shared_ptr<Actor> find_actor(const std::string &name);
    static py::list find_all_actors(const std::string &name);
    static std::shared_ptr<Actor> add_actor(py::object actor);
    static void destroy_actor(Actor * actor_ptr);
    
    static void update_actors();

    // class member items
    std::string name;
    py::list scene_actors;

    Scene();
    Scene(const std::string &new_name, py::list new_actors);
    Scene(py::kwargs kwargs);
    std::string to_string();
};

#endif /* Scene_hpp */
