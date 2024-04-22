//
//  ComponentEngine.cpp
//  game_engine
//
//  Created by Jeremy Liu on 2/28/24.
//

#include "ComponentEngine.hpp"
#include "Actor.hpp"
#include "Scene.hpp"

lua_State* ComponentEngine::lua_state = nullptr;

void ComponentEngine::log_message(const std::string& s) { std::cout << s << std::endl; }
void ComponentEngine::log_error(const std::string &s) { std::cerr << s << std::endl; }
void ComponentEngine::quit() { exit(0); }
void ComponentEngine::sleep(int ms) { std::this_thread::sleep_for(std::chrono::milliseconds(ms)); }
void ComponentEngine::open_url(const std::string &url) {
    #ifdef _WIN32
    std::system(("start " + url).c_str());
    #elif __APPLE__
    std::system(("open " + url).c_str());
    #else
    std::system(("xdg-open " + url).c_str());
    #endif
}

void ComponentEngine::init_lua() {
    lua_state = luaL_newstate();
    luaL_openlibs(lua_state);
    
    // insert debug functionality
    luabridge::getGlobalNamespace(lua_state)
        .beginNamespace("Debug")
            .addFunction("Log", &log_message)
            .addFunction("LogError", &log_error)
        .endNamespace();
    
    // insert actor class functionality
//    luabridge::getGlobalNamespace(lua_state)
//        .beginClass<Actor>("Actor")
//            .addFunction("GetName", &Actor::get_name)
//            .addFunction("GetID", &Actor::get_id)
//            .addFunction("GetComponentByKey", &Actor::get_component_by_key)
//            .addFunction("GetComponent", &Actor::get_component)
//            .addFunction("GetComponents", &Actor::get_components)
//            .addFunction("AddComponent", &Actor::add_component)
//            .addFunction("RemoveComponent", &Actor::remove_component)
//        .endClass();

    // insert static actor functionality
    luabridge::getGlobalNamespace(lua_state)
        .beginNamespace("Actor")
            .addFunction("Find", &Scene::find_actor)
            .addFunction("FindAll", &Scene::find_all_actors)
            .addFunction("Instantiate", &Scene::add_actor)
            .addFunction("Destroy", &Scene::destroy_actor)
        .endNamespace();

    // insert application functionality
    luabridge::getGlobalNamespace(lua_state)
        .beginNamespace("Application")
            .addFunction("Quit", &quit)
            .addFunction("Sleep", &sleep)
            .addFunction("GetFrame", &Helper::GetFrameNumber)
            .addFunction("OpenURL", &open_url)
        .endNamespace();

    // tell lua to support vec2
    luabridge::getGlobalNamespace(lua_state)
        .beginClass<glm::vec2>("vec2")
            .addData("x", &glm::vec2::x)
            .addData("y", &glm::vec2::y)
        .endClass();

    // insert input functionality
    luabridge::getGlobalNamespace(lua_state)
        .beginNamespace("Input")
            .addFunction("GetKey", &Input::get_key)
            .addFunction("GetKeyDown", &Input::get_key_down)
            .addFunction("GetKeyUp", &Input::get_key_up)
            .addFunction("GetMousePosition", &Input::get_mouse_position)
            .addFunction("GetMouseButton", &Input::get_mouse_button)
            .addFunction("GetMouseButtonDown", &Input::get_mouse_button_down)
            .addFunction("GetMouseButtonUp", &Input::get_mouse_button_up)
            .addFunction("GetMouseScrollDelta", &Input::get_mouse_scroll_delta)
        .endNamespace();

    // insert text functionality
//    luabridge::getGlobalNamespace(lua_state)
//        .beginNamespace("Text")
//            .addFunction("Draw", &GraphicsEngine::draw_text)
//        .endNamespace();

    // insert audio functionality
    luabridge::getGlobalNamespace(lua_state)
        .beginNamespace("Audio")
            .addFunction("Play", &AudioEngine::play)
            .addFunction("Halt", &AudioEngine::stop)
            .addFunction("SetVolume", &AudioEngine::set_volume)
        .endNamespace();

    // insert Image functionality
    luabridge::getGlobalNamespace(lua_state)
        .beginNamespace("Image")
            .addFunction("Draw", &GraphicsEngine::draw)
            .addFunction("DrawEx", &GraphicsEngine::draw_ex)
            .addFunction("DrawUI", &GraphicsEngine::draw_ui)
            .addFunction("DrawUIEx", &GraphicsEngine::draw_ui_ex)
            .addFunction("DrawPixel", &GraphicsEngine::draw_pixel)
        .endNamespace();

    // insert camera functionality
    luabridge::getGlobalNamespace(lua_state)
        .beginNamespace("Camera")
            .addFunction("SetPosition", &GraphicsEngine::set_position)
            .addFunction("GetPositionX", &GraphicsEngine::get_camera_pos_x)
            .addFunction("GetPositionY", &GraphicsEngine::get_camera_pos_y)
            .addFunction("SetZoom", &GraphicsEngine::set_camera_zoom)
            .addFunction("GetZoom", &GraphicsEngine::get_camera_zoom)
        .endNamespace();

//    // insert Scene functionality
//    luabridge::getGlobalNamespace(lua_state)
//        .beginNamespace("Scene")
//            .addFunction("Load", &Scene::set_next_scene)
//            .addFunction("GetCurrent", &Scene::get_current_scene)
//            .addFunction("DontDestroy", &Scene::dont_destroy_actor)
//        .endNamespace();

    // insert Vector2
    luabridge::getGlobalNamespace(lua_state)
        .beginClass<b2Vec2>("Vector2")
            .addConstructor<void(*)(float, float)>()
            .addData("x", &b2Vec2::x)
            .addData("y", &b2Vec2::y)
            .addFunction("Normalize", &b2Vec2::Normalize)
            .addFunction("Length", &b2Vec2::Length)
            .addFunction("__add", &b2Vec2::operator_add)
            .addFunction("__sub", &b2Vec2::operator_sub)
            .addFunction("__mul", &b2Vec2::operator_mul)
            .addStaticFunction("Distance", &b2Distance)
            .addStaticFunction("Dot", static_cast<float(*)(const b2Vec2&, const b2Vec2&)>(b2Dot))
        .endClass();

    // insert rigidbody
    luabridge::getGlobalNamespace(lua_state)
        .beginClass<Rigidbody>("Rigidbody")
            .addData("type", &Rigidbody::type)
            .addData("actor", &Rigidbody::actor)
            .addData("key", &Rigidbody::key)
            .addData("enabled", &Rigidbody::enabled)
            .addData("x", &Rigidbody::x)
            .addData("y", &Rigidbody::y)
            .addData("body_type", &Rigidbody::body_type)
            .addData("precise", &Rigidbody::precise)
            .addData("gravity_scale", &Rigidbody::gravity_scale)
            .addData("density", &Rigidbody::density)
            .addData("angular_friction", &Rigidbody::angular_friction)
            .addData("rotation", &Rigidbody::rotation)
            .addData("has_collider", &Rigidbody::has_collider)
            .addData("collider_type", &Rigidbody::collider_type)
            .addData("width", &Rigidbody::width)
            .addData("height", &Rigidbody::height)
            .addData("radius", &Rigidbody::radius)
            .addData("friction", &Rigidbody::friction)
            .addData("bounciness", &Rigidbody::bounciness)
            .addData("has_trigger", &Rigidbody::has_trigger)
            .addData("trigger_type", &Rigidbody::trigger_type)
            .addData("trigger_width", &Rigidbody::trigger_width)
            .addData("trigger_height", &Rigidbody::trigger_height)
            .addData("trigger_radius", &Rigidbody::trigger_radius)
            .addFunction("GetPosition", &Rigidbody::get_position)
            .addFunction("GetRotation", &Rigidbody::get_rotation)
            .addFunction("GetVelocity", &Rigidbody::get_velocity)
            .addFunction("GetAngularVelocity", &Rigidbody::get_angular_velocity)
            .addFunction("GetGravityScale", &Rigidbody::get_gravity_scale)
            .addFunction("GetUpDirection", &Rigidbody::get_up_direction)
            .addFunction("GetRightDirection", &Rigidbody::get_right_direction)
            .addFunction("AddForce", &Rigidbody::add_force)
            .addFunction("SetVelocity", &Rigidbody::set_velocity)
            .addFunction("SetPosition", &Rigidbody::set_position)
            .addFunction("SetRotation", &Rigidbody::set_rotation)
            .addFunction("SetAngularVelocity", &Rigidbody::set_angular_velocity)
            .addFunction("SetGravityScale", &Rigidbody::set_gravity_scale)
            .addFunction("SetUpDirection", &Rigidbody::set_up_direction)
            .addFunction("SetRightDirection", &Rigidbody::set_right_direction)
            .addFunction("OnStart", &Rigidbody::OnStart)
        .endClass();

    // insert collision
    luabridge::getGlobalNamespace(lua_state)
        .beginClass<Collision>("Collision")
            .addData("other", &Collision::other)
            .addData("point", &Collision::point)
            .addData("relative_velocity", &Collision::relative_velocity)
            .addData("normal", &Collision::normal)
        .endClass();

    // insert raycast
    luabridge::getGlobalNamespace(lua_state)
        .beginClass<HitResult>("HitResult")
            .addData("actor", &HitResult::actor)
            .addData("point", &HitResult::point)
            .addData("normal", &HitResult::normal)
            .addData("is_trigger", &HitResult::is_trigger)
        .endClass();

    // insert physics namespace
    luabridge::getGlobalNamespace(lua_state)
        .beginNamespace("Physics")
            .addFunction("Raycast", &Raycast::raycast)
            .addFunction("RaycastAll", &Raycast::raycast_all)
        .endNamespace();

    // insert event bus
    luabridge::getGlobalNamespace(lua_state)
        .beginNamespace("Event")
            .addFunction("Publish", &EventBus::publish)
            .addFunction("Subscribe", &EventBus::subscribe)
            .addFunction("Unsubscribe", &EventBus::unsubscribe)
        .endNamespace();
}

void ComponentEngine::establish_inheretance(luabridge::LuaRef &instance_table, const luabridge::LuaRef &parent_table) {
    assert(lua_state != nullptr && "Remember to call init_lua()");
    
    luabridge::LuaRef new_metatable = luabridge::newTable(lua_state);
    new_metatable["__index"] = parent_table;

    instance_table.push(lua_state);
    new_metatable.push(lua_state);
    lua_setmetatable(lua_state, -2);
    lua_pop(lua_state, 1);
}

std::shared_ptr<luabridge::LuaRef> ComponentEngine::get_component(std::string component_name) {
    if (component_name == "") {
        return nullptr;
    }
    
    // lua support here
    assert(lua_state != nullptr && "Remember to call init_lua()");

    // return custom cpp components
    if (component_name == "Rigidbody") {
        // check to see if a box2d world has been made yet
        if (Scene::box2d_world == nullptr) {
            Scene::box2d_world = new b2World(b2Vec2(0.0f, 9.8f));
            Scene::box2d_world->SetContactListener(new ContactListener());
        }

        Rigidbody *rigidbody = new Rigidbody();
        luabridge::push(lua_state, rigidbody);
        return std::make_shared<luabridge::LuaRef>(luabridge::LuaRef::fromStack(lua_state, -1));
    }

    luabridge::LuaRef component_table_ref = luabridge::getGlobal(lua_state, component_name.c_str());
    if (component_table_ref == luabridge::Nil()) {
        std::string filename = "./resources/component_types/" + component_name + ".lua";
        if (!std::filesystem::exists(filename)) {
            std::cout << "error: failed to locate component " << component_name;
            exit(0);
        }
        
        if (luaL_dofile(lua_state, filename.c_str()) != LUA_OK) {
            std::cout << "problem with lua file " << component_name;
            exit(0);
        }
        
        component_table_ref = luabridge::getGlobal(lua_state, component_name.c_str());
        if (component_table_ref == luabridge::Nil()) {
            assert(false && "didn't find table name in luafile");
        }
    }

    auto copy = luabridge::newTable(lua_state);
    ComponentEngine::establish_inheretance(copy, component_table_ref);
    return std::make_shared<luabridge::LuaRef>(copy);
}
