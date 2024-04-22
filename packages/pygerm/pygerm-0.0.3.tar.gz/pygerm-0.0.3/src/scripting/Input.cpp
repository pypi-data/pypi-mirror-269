//
//  Input.cpp
//  game_engine
//
//  Created by Jeremy Liu on 2/17/24.
//

#include "Input.hpp"

#include <iostream>

SDL_Scancode Input::get_code(const std::string &key) {
    if (key.size() > 1) {
        if (key == "lshift") {
            return SDL_SCANCODE_LSHIFT;
        } else if (key == "rshift") {
            return SDL_SCANCODE_RSHIFT;
        } else if (key == "lctrl") {
            return SDL_SCANCODE_LCTRL;
        } else if (key == "rctrl") {
            return SDL_SCANCODE_RCTRL;
        } else if (key == "lalt") {
            return SDL_SCANCODE_LALT;
        } else if (key == "ralt") {
            return SDL_SCANCODE_RALT;
        } else if (key == "enter") {
            return SDL_SCANCODE_RETURN;
        }
    }
    return SDL_GetScancodeFromName(key.c_str());
}

void Input::init() {
    mouse_position = glm::vec2(0, 0);
    for (int code = SDL_SCANCODE_UNKNOWN; code < SDL_NUM_SCANCODES; ++code) {
        keyboard_states.at(code) = INPUT_STATE_UP;
    }
}

void Input::process_event(const SDL_Event &e) {
    // handle keyboard inputs
    if (e.type == SDL_KEYDOWN) {
        keyboard_states.at(e.key.keysym.scancode) = INPUT_STATE_JUST_BECAME_DOWN;
    } else if (e.type == SDL_KEYUP) {
        keyboard_states.at(e.key.keysym.scancode) = INPUT_STATE_JUST_BECAME_UP;
    }
    
    // handle mouse inputs
    else if (e.type == SDL_MOUSEMOTION) {
        mouse_position.x = static_cast<float>(e.motion.x);
        mouse_position.y = static_cast<float>(e.motion.y);
    } else if (e.type == SDL_MOUSEWHEEL) {
        mouse_scroll_delta = e.wheel.preciseY;
    } else if (e.type == SDL_MOUSEBUTTONDOWN) {
        mouse_states.at(e.button.button) = INPUT_STATE_JUST_BECAME_DOWN;
    } else if (e.type == SDL_MOUSEBUTTONUP) {
        mouse_states.at(e.button.button) = INPUT_STATE_JUST_BECAME_UP;
    }
}

void Input::late_update() {
    // change keyboard inputs
    for (int code = SDL_SCANCODE_UNKNOWN; code < SDL_NUM_SCANCODES; ++code) {
        if (keyboard_states[code] == INPUT_STATE_JUST_BECAME_DOWN) {
            keyboard_states[code] = INPUT_STATE_DOWN;
        } else if (keyboard_states[code] == INPUT_STATE_JUST_BECAME_UP) {
            keyboard_states[code] = INPUT_STATE_UP;
        }
    }
    
    // change mouse inputs
    for (int i = 0; i < 6; ++i) {
        if (mouse_states[i] == INPUT_STATE_JUST_BECAME_DOWN) {
            mouse_states[i] = INPUT_STATE_DOWN;
        } else if (mouse_states[i] == INPUT_STATE_JUST_BECAME_UP) {
            mouse_states[i] = INPUT_STATE_UP;
        }
    }

    mouse_scroll_delta = 0;
}

bool Input::get_key(const std::string &key) {
    SDL_Scancode code = get_code(key.c_str());
    return keyboard_states.at(code) == INPUT_STATE_DOWN || keyboard_states.at(code) == INPUT_STATE_JUST_BECAME_DOWN;
}

bool Input::get_key_up(const std::string &key) {
    SDL_Scancode code = get_code(key.c_str());
    return keyboard_states.at(code) == INPUT_STATE_JUST_BECAME_UP;
}

bool Input::get_key_down(const std::string &key) {
    SDL_Scancode code = get_code(key.c_str());
    return keyboard_states.at(code) == INPUT_STATE_JUST_BECAME_DOWN;
}

b2Vec2 Input::get_mouse_position() {
    return b2Vec2(mouse_position.x, mouse_position.y);
}

bool Input::get_mouse_button(int button_num) {
    return mouse_states.at(button_num) == INPUT_STATE_DOWN || mouse_states.at(button_num) == INPUT_STATE_JUST_BECAME_DOWN;
}

bool Input::get_mouse_button_down(int button_num) {
    return mouse_states.at(button_num) == INPUT_STATE_JUST_BECAME_DOWN;
}

bool Input::get_mouse_button_up(int button_num) {
    return mouse_states.at(button_num) == INPUT_STATE_JUST_BECAME_UP;
}

float Input::get_mouse_scroll_delta() {
    return mouse_scroll_delta;
}