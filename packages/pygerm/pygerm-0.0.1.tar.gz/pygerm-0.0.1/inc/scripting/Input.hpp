//
//  Input.hpp
//  game_engine
//
//  Created by Jeremy Liu on 2/17/24.
//

#ifndef Input_hpp
#define Input_hpp

#include <array>
#include <stdio.h>

#include "glm/glm.hpp"
#include "SDL2/SDL.h"
#include "lua/lua.hpp"
#include "LuaBridge/LuaBridge.h"

#include "ComponentEngine.hpp"

enum INPUT_STATE { INPUT_STATE_UP, INPUT_STATE_JUST_BECAME_DOWN, INPUT_STATE_DOWN, INPUT_STATE_JUST_BECAME_UP };

class Input {
private:
    static inline float mouse_scroll_delta;
    static inline glm::vec2 mouse_position;
    static inline std::array<INPUT_STATE, 6> mouse_states;
    static inline std::array<INPUT_STATE, SDL_NUM_SCANCODES> keyboard_states;

    static SDL_Scancode get_code(const std::string &key);
public:
    static void init(); // Call before main loop begins.
    static void process_event(const SDL_Event & e); // Call every frame at start of event loop.
    static void late_update();

    static bool get_key(const std::string &key);
    static bool get_key_down(const std::string &key);
    static bool get_key_up(const std::string &key);
    static luabridge::LuaRef get_mouse_position();
    static bool get_mouse_button(int button_num);
    static bool get_mouse_button_down(int button_num);
    static bool get_mouse_button_up(int button_num);
    static float get_mouse_scroll_delta();
};

#endif /* Input_hpp */
