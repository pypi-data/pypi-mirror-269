//
// Created by Jeremy Liu on 4/13/24.
//

#include <iostream>
#include <chrono>
#include <ctime>

#include <pybind11/pybind11.h>

#include "GameEngine.hpp"
#include "Application.hpp"

namespace py = pybind11;

PYBIND11_MODULE(pygerm, m) {
    m.doc() = "A component based, 2D python game engine!"; // optional module docstring

    // game engine class
    py::class_<GameEngine>(m, "Game")
            .def(py::init<>(), "Default Game Constructor")
            .def(py::init<GameConfig, RenderingConfig, Scene>(), "Game Constructor with Configs")
            .def(py::init<py::kwargs>(), "Game Constructor that takes game_config, rendering_config, and initial_scene kwargs")
            .def("run", &GameEngine::game_loop, "Begins your game. Does not return until the game exits")
            .def_readwrite("game_config", &GameEngine::game_config, "The game configuration")
            .def_readwrite("rendering_config", &GameEngine::rendering_config, "The rendering configuration")
            .def_readwrite("initial_scene", &GameEngine::scene, "Adds a scene to the game");

    // config classes
    py::class_<GameConfig>(m, "GameConfig")
            .def(py::init<>(), "Default GameConfig Constructor")
            .def(py::init<std::string>(), "GameConfig Constructor that takes in a json file path")
            .def(py::init<py::kwargs>(), "GameConfig Constructor that takes kwargs for game_title")
            .def("__str__", &GameConfig::to_string, "Returns a string representation of the GameConfig")
            .def_readwrite("game_title", &GameConfig::game_title, "The title of the game");

    py::class_<RenderingConfig>(m, "RenderingConfig")
            .def(py::init<>(), "Default RenderingConfig Constructor")
            .def(py::init<int, int, SDL_Color>(), "RenderingConfig Constructor that takes in x_resolution, y_resolution, and clear_color")
            .def(py::init<py::kwargs>(), "RenderingConfig Constructor that takes kwargs for x_resolution, y_resolution, and clear_color")
            .def(py::init<std::string>(), "RenderingConfig Constructor that takes in a json file path")
            .def("__str__", &RenderingConfig::to_string, "Returns a string representation of the RenderingConfig")
            .def_readwrite("x_resolution", &RenderingConfig::x_resolution, "The x resolution, or width, of the game window")
            .def_readwrite("y_resolution", &RenderingConfig::y_resolution, "The y resolution, or height, of the game window")
            .def_readwrite("color", &RenderingConfig::clear_color, "The color to clear the screen with at the beginning of every frame");

    py::class_<SDL_Color>(m, "Color")
            .def(py::init<>(), "Default Color Constructor")
            .def(py::init<uint8, uint8, uint8, uint8>(), py::arg("r") = 0, py::arg("g") = 0, py::arg("b") = 0, py::arg("a") = 255, "Color Constructor that takes in r, g, b, and a values")
            .def("__str__", [](const SDL_Color &c) {
                return "Color(" + std::to_string(c.r) + ", " + std::to_string(c.g) + ", " + std::to_string(c.b) + ", " + std::to_string(c.a) + ")";
            }, "Returns a string representation of the Color")
            .def_readwrite("r", &SDL_Color::r, "The red value of Color")
            .def_readwrite("g", &SDL_Color::g, "The green value of Color")
            .def_readwrite("b", &SDL_Color::b, "The blue value of Color")
            .def_readwrite("a", &SDL_Color::a, "The alpha value of Color");

    py::class_<Scene>(m, "Scene")
            .def(py::init<>(), "Default Scene Constructor")
            .def(py::init<std::string, py::list>(), "Scene Constructor that takes in a name and a list of actors")
            .def(py::init<py::kwargs>(), "Scene Constructor that takes kwargs for scene_name")
            .def("__str__", &Scene::to_string, "Returns a string representation of the Scene")
            .def_readwrite("scene_name", &Scene::name, "The name of the scene")
            .def_readwrite("actors", &Scene::scene_actors, "The actors in the scene")
            .def_static("getCurrent", &Scene::get_current_scene, "Returns the current scene")
            .def_static("load", &Scene::load, "Loads the scene with the given name")
            .def_static("persist", &Scene::dont_destroy_actor, "Marks an actor to persist across all scenes");

    py::class_<Actor>(m, "Actor")
            .def(py::init<>(), "Default Actor Constructor")
            .def(py::init<std::string, py::dict>(), "Actor Constructor that takes in a name and a list of components")
            .def(py::init<py::kwargs>(), "Actor Constructor that takes kwargs for actor_name and components")
            .def("getName", &Actor::get_name, "Returns the name of the actor")
            .def("getID", &Actor::get_id, "Returns the id of the actor")
            .def("getComponentByKey", &Actor::get_component_by_key, "Returns the component with the given key")
            .def("getComponent", &Actor::get_component, "Returns the component with the given type")
            .def("getComponents", &Actor::get_components, "Returns a tuple of components with the given type")
            .def("addComponent", &Actor::add_component, "Adds the given component to the actor")
            .def("removeComponent", &Actor::remove_component, "Removes the given component from the actor")
            .def_static("create", &Scene::add_actor, "Creates an actor with the given name and components")
            .def_static("destroy", &Scene::destroy_actor, "Destroys the actor with the given name")
            .def_static("find", &Scene::find_actor, "Returns the actor with the given name")
            .def_static("findAll", &Scene::find_all_actors, "Returns an array of actors with the given name")
            .def_readwrite("name", &Actor::name, "The name of the actor")
            .def_readwrite("components", &Actor::init_component_map, "The components of the actor will start with");

    py::class_<Component>(m, "Component")
            .def(py::init<>(), "Default Component Constructor")
            .def_readwrite("enabled", &Component::enabled, "Whether the component is enabled")
            .def_readwrite("key", &Component::key, "The key of the component")
            .def("onStart", &Component::onStart, "Called on the frame when the component is added to an actor")
            .def("onUpdate", &Component::onUpdate, "Called every frame the actor is valid")
            .def("onLateUpdate", &Component::onLateUpdate, "Called every frame after all onUpdate calls of all actors")
            .def("onDestroy", &Component::onDestroy, "Called on the frame when the component is removed from an actor")
            .def(py::pickle(
                    [](const Component &c) {
                        return py::make_tuple(c.enabled, c.key, c.actor);
                    },
                    [](py::tuple t) {
                        if (t.size() != 3) throw std::runtime_error("Invalid state!");
                        Component c;
                        c.enabled = t[0].cast<bool>();
                        c.key = t[1].cast<std::string>();
                        c.actor = t[2].cast<Actor*>();
                        return c;
                    }
            ));

    py::module application = m.def_submodule("Application", "The Application submodule of pygerm");
    application.def("quit", &Application::quit, "Quits the application")
            .def("sleep", &Application::sleep, "Sleeps the application for the given number of milliseconds")
            .def("getFrame", &Application::get_frame, "Returns the current frame of the game")
            .def("openUrl", &Application::open_url, "Opens the given url in the default browser");

    py::module input = m.def_submodule("Input", "The Input submodule of pygerm");
    input.def("getKey", &Input::get_key, "Returns true if the key is down")
            .def("getKeyDown", &Input::get_key_down, "Returns true if the key was just pressed")
            .def("getKeyUp", &Input::get_key_up, "Returns true if the key was just released")
            .def("getMousePosition", &Input::get_mouse_position, "Returns the current mouse position")
            .def("getMouseButton", &Input::get_mouse_button, "Returns true if the mouse button is down")
            .def("getMouseButtonDown", &Input::get_mouse_button_down, "Returns true if the mouse button was just pressed")
            .def("getMouseButtonUp", &Input::get_mouse_button_up, "Returns true if the mouse button was just released")
            .def("getMouseScrollDelta", &Input::get_mouse_scroll_delta, "Returns the mouse scroll delta");


    py::module text = m.def_submodule("Text", "The text submodule of pygerm");
    text.def("draw",&GraphicsEngine::draw_text, "Draws the given text at the given position with the given font, size, and color",
                py::arg("text"),
                py::arg("x")=0,
                py::arg("y")=0,
                py::arg("font_path"),
                py::arg("font_size")=24,
                py::arg("color")=SDL_Color{0, 0, 0, 255}
             );

    py::module audio = m.def_submodule("Audio", "The audio submodule of pygerm");
    audio.def("play", &AudioEngine::play, "Plays the sound at the given path",
                 py::arg("channel")=0,
                 py::arg("audio_path"),
                 py::arg("loops")=false)
            .def("stop", &AudioEngine::stop, "Stops the sound at the given channel",
                 py::arg("channel")=0)
            .def("setVolume", &AudioEngine::set_volume, "Sets the volume of the sound at the given channel",
                 py::arg("channel")=0,
                 py::arg("volume")=128);

    py::module image = m.def_submodule("Image", "The image submodule of pygerm");
    image.def("drawUI", &GraphicsEngine::draw_ui_ex, "Draws a UI element on the screen",
              py::arg("image_path"),
              py::arg("x")=0,
              py::arg("y")=0,
              py::arg("color")=SDL_Color{255, 255, 255, 255},
              py::arg("sort_order")=0)
          .def("draw", &GraphicsEngine::draw_ex, "Draws an image on the screen",
              py::arg("image_path"),
              py::arg("x")=0,
              py::arg("y")=0,
              py::arg("rotation")=0,
              py::arg("x_scale")=1.0,
              py::arg("y_scale")=1.1,
              py::arg("pivot_x")=0.5,
              py::arg("pivot_y")=0.5,
              py::arg("color")=SDL_Color{255, 255, 255, 255},
              py::arg("sort_order")=0)
            .def("drawPixel", &GraphicsEngine::draw_pixel, "Draws a pixel on the screen",
                 py::arg("x"),
                 py::arg("y"),
                 py::arg("color")=SDL_Color{255, 255, 255, 255});

    py::module camera = m.def_submodule("Camera", "The camera submodule of pygerm");
    camera.def("setPosition", &GraphicsEngine::set_position, "Sets the position of the camera",
               py::arg("x")=0.0,
               py::arg("y")=0.0)
            .def("getPositionX", &GraphicsEngine::get_camera_pos_x, "Returns the x position of the camera")
            .def("getPositionY", &GraphicsEngine::get_camera_pos_y, "Returns the y position of the camera")
            .def("setZoom", &GraphicsEngine::set_camera_zoom, "Sets the zoom of the camera",
                 py::arg("zoom")=1.0)
            .def("getZoom", &GraphicsEngine::get_camera_zoom, "Returns the zoom of the camera");
}
