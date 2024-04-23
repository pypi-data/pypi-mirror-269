//
//  TextAdventure.hpp
//  game_engine
//
//  Created by Jeremy Liu on 1/24/24.
//

#ifndef GameEngine_hpp
#define GameEngine_hpp

#include <stdio.h>
#include <iostream>
#include <sstream>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <optional>
#include <tuple>
#include <variant>

#include "glm/glm.hpp"
#include <pybind11/pybind11.h>

#include "Helper.h"
#include "AudioHelper.h"
#include "GraphicsEngine.hpp"
#include "AudioEngine.hpp"
#include "EngineUtils.hpp"
#include "Scene.hpp"
#include "Input.hpp"
#include "ComponentEngine.hpp"
#include "EventBus.hpp"
#include "GameConfig.hpp"
#include "RenderingConfig.hpp"

namespace py = pybind11;

class GameEngine {
private:
    bool is_running;
public:
    GameConfig game_config;
    RenderingConfig rendering_config;
    Scene scene;

    GameEngine();
    GameEngine(GameConfig game_config, RenderingConfig rendering_config, Scene scene);
    GameEngine(py::kwargs kwargs);

    void init_game();
    void game_loop();
};

#endif /* TextAdventure_hpp */
