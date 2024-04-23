//
//  Actor.cpp
//  game_engine
//
//  Created by Jeremy Liu on 1/31/24.
//

#include "Actor.hpp"

void Actor::process_actor_init() {
    // validate init_component_map and move to components_to_add
    for (auto &[key, value] : init_component_map) {
        std::string component_key = key.cast<std::string>();

        if (!py::isinstance<Component>(value)) {
            throw std::invalid_argument("error: component: " + component_key + " must be inheriting from the Component() class");
        }

        auto component_ptr = std::make_shared<py::object>(value.cast<py::object>());
        component_ptr->attr("actor") = this;
        component_ptr->attr("key") = component_key;

        components_to_add[component_key] = component_ptr;

        // cache overhead
        component_key_cache[component_key] = components_to_add[component_key];
        component_type_cache[component_ptr->attr("__class__").attr("__name__").cast<std::string>()].push_back(components_to_add[component_key]);
    }

    init_component_map.clear();
}

Actor::Actor() {
    actor_id = global_id_counter++;
    name = DEFAULT_ACTOR_NAME;
}

Actor::Actor(const std::string &actor_name, py::dict components) : Actor() {
    name = actor_name;
    init_component_map = components;

    process_actor_init();
}

Actor::Actor(py::kwargs kwargs) : Actor() {
    if (kwargs.contains("name")) {
        if (py::isinstance<py::str>(kwargs["name"])) {
            name = kwargs["name"].cast<std::string>();
        } else {
            throw std::invalid_argument("error: name must be a string");
        }
    }

    if (kwargs.contains("components")) {
        if (py::isinstance<py::dict>(kwargs["components"])) {
            init_component_map = kwargs["components"].cast<py::dict>();
        } else {
            throw std::invalid_argument("error: components must be a dictionary");
        }
    }

    std::unordered_set<std::string> valid_kwargs = {"name", "components"};
    for (auto &item : kwargs) {
        if (valid_kwargs.find(item.first.cast<std::string>()) == valid_kwargs.end()) {
            throw std::invalid_argument("error: invalid keyword argument " + item.first.cast<std::string>());
        }
    }

    process_actor_init();
}

Actor::Actor(const Actor &actor) : Actor() {
    enabled = actor.enabled;
    name = actor.name;

    py::module copy = py::module::import("copy");
    for (auto &[key, component] : actor.components_to_add) {
        auto component_ptr = std::make_shared<py::object>(copy.attr("deepcopy")(*component));
        components_to_add[key] = component_ptr;
        components_to_add[key]->attr("actor") = this;

        // cache overhead
        component_key_cache[key] = components_to_add[key];
        component_type_cache[component_ptr->attr("__class__").attr("__name__").cast<std::string>()].push_back(components_to_add[key]);
    }
}

Actor::Actor(const Actor&& other) noexcept {
    enabled = other.enabled;
    name = other.name;
    actor_id = other.actor_id;

    components_to_add = other.components_to_add;
    for (auto &[key, component] : components_to_add) {
        components_to_add[key]->attr("actor") = this;
    }

    for (auto &[key, component] : components) {
        components[key]->attr("actor") = this;
    }

    for (auto &[key, component] : components_to_remove) {
        components_to_remove[key]->attr("actor") = this;
    }

    // move caches
    component_key_cache = other.component_key_cache;
    component_type_cache = other.component_type_cache;
}

void Actor::operator=(const Actor &actor) {
    throw std::runtime_error("error: Actor assignment operator is not implemented yet");
}

//Actor::Actor(const std::string &actor_name) : Actor() {
//    auto templated_actor = get_template_actor(actor_name);
//
//    name = templated_actor->name;
//    for (auto &[key, component] : templated_actor->components_to_add) {
//        if ((*component)["type"].cast<std::string>() == "Rigidbody") {
//            if (Scene::box2d_world == nullptr) {
//                Scene::box2d_world = new b2World(b2Vec2(0.0f, 9.8f));
//                Scene::box2d_world->SetContactListener(new ContactListener());
//            }
//
//            Rigidbody *rigidbody = new Rigidbody(*component);
//            luabridge::push(ComponentEngine::lua_state, rigidbody);
//            auto component_ref = std::make_shared<luabridge::LuaRef>(luabridge::LuaRef::fromStack(ComponentEngine::lua_state, -1));
//            (*component_ref)["actor"] = this;
//
//            components_to_add[key] = component_ref;
//
//            // CACHING
//            component_key_cache[key] = components_to_add[key];
//            component_type_cache[(*components_to_add[key])["type"].cast<std::string>()].push_back(components_to_add[key]);
//            continue;
//        }
//
//        auto component_ref = std::make_shared<luabridge::LuaRef>(luabridge::newTable(ComponentEngine::lua_state));
//        ComponentEngine::establish_inheretance(*component_ref, *component);
//        (*component_ref)["actor"] = this;
//
//        components_to_add[key] = component_ref;
//
//        // CACHING
//        component_key_cache[key] = components_to_add[key];
//        component_type_cache[(*components_to_add[key])["type"].cast<std::string>()].push_back(components_to_add[key]);
//    }
//}
//
//Actor::Actor(const rapidjson::Value &actor_json) : Actor() {
//    if (actor_json.HasMember("template")) {
//        auto templated_actor = get_template_actor(actor_json["template"].GetString());
//
//        // deep copy the fields needed to the current actor from the templated actor
//        name = templated_actor->name;
//        for (auto &[key, component] : templated_actor->components_to_add) {
//            if ((*component)["type"].cast<std::string>() == "Rigidbody") {
//                if (Scene::box2d_world == nullptr) {
//                    Scene::box2d_world = new b2World(b2Vec2(0.0f, 9.8f));
//                    Scene::box2d_world->SetContactListener(new ContactListener());
//                }
//
//                Rigidbody *rigidbody = new Rigidbody(*component);
//                luabridge::push(ComponentEngine::lua_state, rigidbody);
//                auto component_ref = std::make_shared<luabridge::LuaRef>(luabridge::LuaRef::fromStack(ComponentEngine::lua_state, -1));
//                (*component_ref)["actor"] = this;
//
//                components_to_add[key] = component_ref;
//                continue;
//            }
//
//            auto component_ref = std::make_shared<luabridge::LuaRef>(luabridge::newTable(ComponentEngine::lua_state));
//            ComponentEngine::establish_inheretance(*component_ref, *component);
//            (*component_ref)["actor"] = this;
//
//            components_to_add[key] = component_ref;
//        }
//    }
//
//    name = actor_json.HasMember("name") ? actor_json["name"].GetString() : name;
//
//    // init or update components for actor
//    if (actor_json.HasMember("components") && actor_json["components"].IsObject()) {
//        for (auto &component : actor_json["components"].GetObject()) {
//            std::string component_name = component.name.GetString();
//
//            // get the component ref if its from a template or create a new component
//            std::shared_ptr<luabridge::LuaRef> component_ptr;
//            if (components_to_add.find(component_name) != components_to_add.end()) {
//                component_ptr = components_to_add[component_name];
//            } else if (component.value.HasMember("type")) {
//                component_ptr = ComponentEngine::get_component(component.value["type"].GetString());
//            } else {
//                continue;
//            }
//
//            // inject member values
//            for (auto &property : component.value.GetObject()) {
//                std::string property_name = property.name.GetString();
//                if (property.value.IsBool()) {
//                    (*component_ptr)[property_name] = property.value.GetBool();
//                } else if (property.value.IsInt()) {
//                    (*component_ptr)[property_name] = property.value.GetInt();
//                } else if (property.value.IsFloat()) {
//                    (*component_ptr)[property_name] = property.value.GetFloat();
//                } else if (property.value.IsString()) {
//                    (*component_ptr)[property_name] = std::string(property.value.GetString());
//                } else {
//                    std::cout << "error: unsupported type in actor ctor type: " << property.value.GetType() << std::endl;
//                }
//            }
//
//            // inject engine identifier
//            (*component_ptr)["actor"] = this;
//            (*component_ptr)["enabled"] = true;
//            (*component_ptr)["key"] = component_name;
//            components_to_add[component_name] = component_ptr;
//        }
//
//        // TODO optimization: can filter out which ones have OnStart, OnUpdate, OnLateUpdate and store into their own maps
//        for (auto &[key, component] : components_to_add) {
//            component_key_cache[key] = components_to_add[key];
//            component_type_cache[(*components_to_add[key])["type"].cast<std::string>()].push_back(components_to_add[key]);
//        }
//    }
//}

//Actor::~Actor() {
//    components.insert(components_to_add.begin(), components_to_add.end());
//    components.insert(components_to_remove.begin(), components_to_remove.end());
//    for (auto &[key, component] : components) {
//        component->onDestroy();
////        if (!(*component)["OnDestroy"].isNil()) {
////            (*component)["OnDestroy"]((*component));
////        }
//    }
//}

std::string Actor::get_name() {
    return name;
}

int Actor::get_id() {
    return actor_id;
}

py::object Actor::get_component_by_key(const std::string &key_name) {
    if (component_key_cache.find(key_name) == component_key_cache.end() || component_key_cache[key_name].expired()) {
        if (component_key_cache[key_name].expired()) {
            component_key_cache.erase(key_name);
        }

        return py::none();
    }

    auto ref = component_key_cache[key_name].lock();
    auto actor = ref->attr("actor").cast<Actor>();
    if (!actor.enabled || !ref->attr("enabled").cast<bool>()) {
        return py::none();
    }

    return *ref;
}

py::object Actor::get_component(py::object component_type) {
    auto bases = component_type.attr("__bases__");
    py::module cpp_module = py::module::import("pygerm");
    py::object component_class = cpp_module.attr("Component");

    bool found = false;
    for (auto b : bases) {
        if (b.is(component_class)) {
            found = true;
            break;
        }
    }

    if (!found) {
        throw std::invalid_argument("error: getComponent() must be called by an object type that inherits from pygerm.Component()");
    }

    auto type_name = component_type.attr("__name__").cast<std::string>();
    if (component_type_cache.find(type_name) == component_type_cache.end() || component_type_cache[type_name].empty()) {
        return py::none();
    }

    if (component_type_cache[type_name].front().expired()) {
        component_type_cache[type_name].pop_front();
        get_component(component_type);
    }

    auto ref = component_type_cache[type_name].front().lock();
    auto actor = ref->attr("actor").cast<Actor>();
    if (!actor.enabled || !ref->attr("enabled").cast<bool>()) {
        return py::none();
    }

    return *ref;
}

py::list Actor::get_components(py::object component_type) {
    auto bases = component_type.attr("__bases__");
    py::module cpp_module = py::module::import("pygerm");
    py::object component_class = cpp_module.attr("Component");

    bool found = false;
    for (auto b : bases) {
        if (b.is(component_class)) {
            found = true;
            break;
        }
    }

    if (!found) {
        throw std::invalid_argument("error: getComponent() must be called by an object type that inherits from pygerm.Component()");
    }

    auto type_name = component_type.attr("__name__").cast<std::string>();

    py::list found_components;
    auto all_components = component_type_cache[type_name];
    for (int i = 0; i < all_components.size(); i++) {
        if (all_components[i].expired()) {
            continue;
        }

        auto ref = all_components[i].lock();
        auto actor = ref->attr("actor").cast<Actor>();
        auto component = ref->cast<Component>();
        if (!actor.enabled || !ref->attr("enabled").cast<bool>()){
            continue;
        }

        found_components.append(*ref);
    }

    return found_components;
}

py::object Actor::add_component(py::object new_component) {
    if (!py::isinstance<Component>(new_component)) {
        throw std::invalid_argument("error: addComponent() must called with a pygerm.Component() object");
    }

    std::string component_key = "r" + std::to_string(Component::num_runtime_components++);
    init_component_map[py::str(component_key)] = new_component;
    process_actor_init();

    return get_component_by_key(component_key);
}

void Actor::remove_component(py::object component_to_remove) {
    if (!py::isinstance<Component>(component_to_remove)) {
        throw std::invalid_argument("error: removeComponent() must called with a pygerm.Component() object");
    }

    std::string key = component_to_remove.attr("key").cast<std::string>();
    if (components.find(key) != components.end()) {
        components_to_remove[key] = components[key];
        components_to_remove[key]->attr("enabled") = false;
    }
}

//void Actor::disable_all_components() {
//    enabled = false;
//
//    for (auto &[key, component] : components) {
//        component->enabled = false;
//    }
//
//    for (auto &[key, component] : components_to_add) {
//        component->enabled = false;
//    }
//}
//
//std::shared_ptr<Actor> Actor::get_template_actor(const std::string& actor_name) {
//    if(template_store.find(actor_name) != template_store.end()) {
//        return template_store[actor_name];
//    }
//
//    if(!std::filesystem::exists(std::string("./resources/actor_templates/") + actor_name + std::string(".template"))) {
//        std::cout << "error: template " << actor_name << " is missing";
//        exit(0);
//    }
//
//    rapidjson::Document actor_config_doc;
//    EngineUtils::read_json_file(std::string("./resources/actor_templates/") + actor_name + std::string(".template"), actor_config_doc);
//    template_store[actor_name] = std::make_shared<Actor>(actor_config_doc.GetObject());
//
//    return template_store[actor_name];
//}
//
void Actor::process_event(const std::string &event_name, std::map<std::string, std::weak_ptr<py::object>> &components_with_event) {
    std::queue <std::string> keys_to_remove;
    for (auto &[key, component] : components_with_event) {
        try {
            if (component.expired()) {
                keys_to_remove.push(key);
                continue;
            }

            std::shared_ptr<py::object> component_ptr = component.lock();
            if (!component_ptr->attr("enabled").cast<bool>()) {
                continue;
            }
            component_ptr->attr(event_name.c_str())();

//            if (!(*component_ptr)[event_name].isNil() && (*component_ptr)["enabled"].cast<bool>()) {
//                (*component_ptr)[event_name]((*component_ptr));
//            }
        } catch (const py::error_already_set &e) {
            throw std::runtime_error("error: " + name + " failed to process event " + event_name + " with error: " + e.what());
        }
    }

    while (!keys_to_remove.empty()) {
        components_with_event.erase(keys_to_remove.front());
        keys_to_remove.pop();
    }
}

//void Actor::process_event_with_args(const std::string &event_name, std::map<std::string, std::weak_ptr<Component>> &components_with_event, const Collision &collision) {
//    std::queue <std::string> keys_to_remove;
//    for (auto &[key, component] : components_with_event) {
//        try {
//            if (component.expired()) {
//                keys_to_remove.push(key);
//                continue;
//            }
//            auto component_ptr = component.lock();
//            if (!(*component_ptr)[event_name].isNil() && (*component_ptr)["enabled"].cast<bool>()) {
//                (*component_ptr)[event_name]((*component_ptr), collision);
//            }
//        } catch (const luabridge::LuaException &e) {
//            EngineUtils::print_lua_error(name, e);
//        }
//    }
//
//    while (!keys_to_remove.empty()) {
//        components_with_event.erase(keys_to_remove.front());
//        keys_to_remove.pop();
//    }
//}

void Actor::process_on_start() {
    for (auto &[key, component] : components_to_add) {
        try {
            component->attr("onStart")();
        } catch (const py::error_already_set &e) {
            throw std::runtime_error("error: " + name + " failed to start component " + key + " with error: " + e.what());
        }

        components_with_on_update[key] = component;
        components_with_on_late_update[key] = component;

//        if ((*component)["OnUpdate"].isFunction()) {
//            components_with_on_update[key] = component;
//        }
//
//        if ((*component)["OnLateUpdate"].isFunction()) {
//            components_with_on_late_update[key] = component;
//        }
//
//        if ((*component)["OnCollisionEnter"].isFunction()) {
//            components_with_on_collision_enter[key] = component;
//        }
//
//        if ((*component)["OnCollisionExit"].isFunction()) {
//            components_with_on_collision_exit[key] = component;
//        }
//
//        if ((*component)["OnTriggerEnter"].isFunction()) {
//            components_with_on_trigger_enter[key] = component;
//        }
//
//        if ((*component)["OnTriggerExit"].isFunction()) {
//            components_with_on_trigger_exit[key] = component;
//        }

        components[key] = component;
    }
    components_to_add.clear();
}

void Actor::process_on_update() {
    process_event("onUpdate", components_with_on_update);
}

void Actor::process_on_late_update() {
    process_event("onLateUpdate", components_with_on_late_update);
}

void Actor::process_on_destroy() {
    for (auto &[key, component] : components_to_remove) {
//        if (!(*component)["OnDestroy"].isNil()) {
//            (*component)["OnDestroy"]((*component));
//        }

        component->attr("onDestroy")();
        components.erase(key);
    }

    components_to_remove.clear();
}

//void Actor::process_on_collision_enter(const Collision &collision) {
//    process_event_with_args("OnCollisionEnter", components_with_on_collision_enter, collision);
//}
//
//void Actor::process_on_collision_exit(const Collision &collision) {
//    process_event_with_args("OnCollisionExit", components_with_on_collision_exit, collision);
//}
//
//void Actor::process_on_trigger_enter(const Collision &collision) {
//    process_event_with_args("OnTriggerEnter", components_with_on_trigger_enter, collision);
//}
//
//void Actor::process_on_trigger_exit(const Collision &collision) {
//    process_event_with_args("OnTriggerExit", components_with_on_trigger_exit, collision);
//}
