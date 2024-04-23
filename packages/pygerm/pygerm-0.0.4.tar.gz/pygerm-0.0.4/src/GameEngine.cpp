//
//  TextAdventure.cpp
//  game_engine
//
//  Created by Jeremy Liu on 1/24/24.
//

#include "GameEngine.hpp"

GameEngine::GameEngine() : game_config(), rendering_config() {}

GameEngine::GameEngine(GameConfig game_config, RenderingConfig rendering_config, Scene scene) : game_config(game_config), rendering_config(rendering_config) {}

GameEngine::GameEngine(py::kwargs kwargs) {
    if (kwargs.contains("game_config")) {
        if (py::isinstance<py::str>(kwargs["game_config"])) {
            game_config = GameConfig(kwargs["game_config"].cast<std::string>());
        } else if (py::isinstance<GameConfig>(kwargs["game_config"])) {
            game_config = kwargs["game_config"].cast<GameConfig>();
        } else {
            throw std::invalid_argument("game_config must be a file path string or a GameConfig object");
        }
    }

    if (kwargs.contains("rendering_config")) {
        if (py::isinstance<py::str>(kwargs["rendering_config"])) {
            rendering_config = RenderingConfig(kwargs["rendering_config"].cast<std::string>());
        } else if (py::isinstance<RenderingConfig>(kwargs["rendering_config"])) {
            rendering_config = kwargs["rendering_config"].cast<RenderingConfig>();
        } else {
            throw std::invalid_argument("rendering_config must be a file path string or a RenderingConfig object");
        }
    }

    if (kwargs.contains("scene")) {
        if (py::isinstance<py::str>(kwargs["scene"])) {
            // init scene information to begin game
//    if (config.find("initial_scene") == config.end()) {
//        std::cout << "error: initial_scene unspecified";
//        exit(0);
//    }

//            Scene::set_next_scene(kwargs["initial_scene"].cast<std::string>());
            throw std::runtime_error("Pathing to scene is currently not supported");
        } else if (py::isinstance<Scene>(kwargs["scene"])) {
            scene = kwargs["scene"].cast<Scene>();
        } else {
            throw std::invalid_argument("scene must be a file path string or a Scene object");

        }
    }

    std::unordered_set<std::string> valid_keys = {"game_config", "rendering_config", "scene"};
    for (auto item : kwargs) {
        if (valid_keys.find(item.first.cast<std::string>()) == valid_keys.end()) {
            throw std::runtime_error("Invalid key: " + item.first.cast<std::string>());
        }
    }
}

void GameEngine::init_game() {
    is_running = true;

    ComponentEngine::init_lua();
    GraphicsEngine::init(game_config, rendering_config);
    AudioEngine::init();
    Input::init();

    Scene::load(scene);
    Scene::start_next_scene();
}

void GameEngine::game_loop() {
    init_game();

    SDL_Event e;
    while (is_running) {
        // handle SDL events and update key states
        while (Helper::SDL_PollEvent498(&e)) {
            if (e.type == SDL_QUIT) {
                is_running = false;
            }

            Input::process_event(e);
        }

        GraphicsEngine::render_clear();

        // update actors, process events, and render physics
        Scene::update_actors();
        EventBus::process_subscriptions();
        if (Scene::box2d_world != nullptr) {
            Scene::box2d_world->Step(1.0f / 60.0f, 8, 3);
        }

        GraphicsEngine::render();
        GraphicsEngine::render_present();

        // update input states
        Input::late_update();

        if (Scene::next_scene) {
            Scene::start_next_scene();
        }
    }

    // shotty fix against Fatal Python error: PyThreadState_Get: the function must be called with the GIL held, but the GIL is released (the current Python thread state is NULL)
    exit(0);
}