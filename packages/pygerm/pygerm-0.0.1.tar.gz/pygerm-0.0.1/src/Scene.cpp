//
//  Scene.cpp
//  game_engine
//
//  Created by Jeremy Liu on 1/31/24.
//

#include "Scene.hpp"

Scene::Scene() {
    name = "Empty Scene";
    scene_actors = py::list();
}

Scene::Scene(const std::string &new_name, py::list new_actors) {
    name = new_name;
    scene_actors = new_actors;
}

Scene::Scene(py::kwargs kwargs) : Scene() {
    if (kwargs.contains("name")) {
        name = kwargs["name"].cast<std::string>();
    }

    if (kwargs.contains("actors")) {
        scene_actors = kwargs["actors"].cast<py::list>();
    }

    std::unordered_set<std::string> valid_args = {"name", "actors"};
    for (auto item : kwargs) {
        if (valid_args.find(item.first.cast<std::string>()) == valid_args.end()) {
            throw std::invalid_argument("Invalid argument: " + item.first.cast<std::string>());
        }
    }
}

std::string Scene::to_string() {
    std::stringstream ss;
    ss << "Scene: " << name << "\t";
    ss << "Actors: " << scene_actors.size() << "\n";
    ss << "TODO PRINT ACTUAL ACTORS" << std::endl;
    return ss.str();
}


//// is this even needed anymore?
//void Scene::load(const std::string &scene) {
//    scene_name = scene;
//    if (!std::filesystem::exists(std::string("./resources/scenes/") + scene_name + std::string(".scene"))) {
//        std::cout << "error: scene " << scene_name << " is missing";
//        exit(0);
//    }
//
//    rapidjson::Document actors_config_doc;
//    EngineUtils::read_json_file(std::string("./resources/scenes/") + scene_name + std::string(".scene"), actors_config_doc);
//
//    // if there are no actors, the scene is effectively empty
//    if (!(actors_config_doc.HasMember("actors") && actors_config_doc["actors"].IsArray())) {
//        return;
//    }
//
//    // create the initial actors in a scene
//    actor_cache.clear();
//    actors.clear();
//    actors.reserve(persistent_actors.size() + actors_config_doc["actors"].Size());
//    std::sort(persistent_actors.begin(), persistent_actors.end(), [](const std::shared_ptr<Actor> &a, const std::shared_ptr<Actor> &b) {
//        return a->actor_id < b->actor_id;
//    });
//
//    for (auto &actor : persistent_actors) {
//        actors.push_back(actor);
//        actor_cache[actor->get_name()].push_back(actor);
//    }
////    actors.insert(actors.end(), persistent_actors.begin(), persistent_actors.end());
//
//    for (rapidjson::SizeType i = 0; i < actors_config_doc["actors"].Size(); ++i) {
//        actors.emplace_back(std::make_shared<Actor>(actors_config_doc["actors"][i]));
//        actor_cache[actors.back()->get_name()].push_back(actors.back());
//    }
//}

void Scene::load(Scene scene) {
    next_scene = std::make_shared<Scene>(scene);
}

void Scene::start_next_scene() {
    if (next_scene == nullptr) {
        return;
    }

    // create the initial actors in a scene
    actor_cache.clear();
    actors.clear();
    actors.reserve(persistent_actors.size());
    std::sort(persistent_actors.begin(), persistent_actors.end(), [](const std::shared_ptr<Actor> &a, const std::shared_ptr<Actor> &b) {
        return a->actor_id < b->actor_id;
    });

    for (auto &actor : persistent_actors) {
        actors.push_back(actor);
        actor_cache[actor->get_name()].push_back(actor);
    }

    for (auto &actor : next_scene->scene_actors) {
        if (py::isinstance<Actor>(actor)) {
            auto scene_actor = actor.cast<Actor>();
            auto actor_ptr = std::make_shared<Actor>(std::move(scene_actor));
            actors.push_back(actor_ptr);
            actor_cache[actors.back()->get_name()].push_back(actors.back());
        } else {
            throw std::invalid_argument("Invalid type in actors array, requires Actor() type");
        }
    }
    next_scene = nullptr;
}

std::string Scene::get_current_scene() {
    return scene_name;
}

void Scene::dont_destroy_actor(Actor *actor_ptr) {
    for (auto &actor : actors) {
        if (actor.get() == actor_ptr) {
            persistent_actors.push_back(actor);
        }
    }
}

std::shared_ptr<Actor> Scene::find_actor(const std::string &name) {
    if (actor_cache.find(name) == actor_cache.end() || actor_cache[name].empty()) {
        return nullptr;
    }

    auto actor = actor_cache[name].front();
    if (actor.expired() || !actor.lock()->enabled) {
        actor_cache[name].pop_front();
        return find_actor(name);
    }

    return actor.lock();
}

py::list Scene::find_all_actors(const std::string &name) {
    if (actor_cache.find(name) == actor_cache.end() || actor_cache[name].empty()) {
        return py::list();
    }

    py::list found_actors = py::list();
    std::deque<std::weak_ptr<Actor>> all_actors = actor_cache[name];
    for (auto &actor : all_actors) {
        if (actor.expired() || !actor.lock()->enabled) {
            continue;
        }

        found_actors.append(actor.lock());
    }

    return found_actors;
}

std::shared_ptr<Actor> Scene::add_actor(py::object actor) {
    if (!py::isinstance<Actor>(actor)) {
        throw std::invalid_argument("Invalid type to call pygerm.createActor(), please ensure that you are using a valid pygerm.Actor() object");
    }

    auto scene_actor = actor.cast<Actor>();
    auto actor_ptr = std::make_shared<Actor>(std::move(scene_actor));
    actors.push_back(actor_ptr);
    actor_cache[actors.back()->get_name()].push_back(actors.back());
    return actor_ptr;
}

void Scene::destroy_actor(Actor *actor_ptr) {
     for (auto &actor : actors) {
         if (actor.get() == actor_ptr) {
             actor->disable_all_components();
             actors_to_remove.push_back(actor);
             return;
         }
     }

    for (auto &actor : actors_to_add) {
        if (actor.get() == actor_ptr) {
            actor->disable_all_components();
            actors_to_remove.push_back(actor);
            return;
        }
    }
}

void Scene::update_actors() {
    // actors to add
    for (auto &actor : actors_to_add) {
        actors.push_back(actor);
    }
    actors_to_add.clear();

    // process added components
    for (auto &actor : actors) {
        actor->process_on_start();
    }

    // OnUpdate
    for (auto &actor : actors) {
        actor->process_on_update();
    }

    // OnLateUpdate
    for (auto &actor : actors) {
        actor->process_on_late_update();
    }

    // process removed components
    for (auto &actor : actors) {
        actor->process_on_destroy();
    }

    // actors destroyed
    for (auto &actor : actors_to_remove) {
        actors.erase(std::remove(actors.begin(), actors.end(), actor), actors.end());
        actor.reset();
    }
}
