//
//  Component.cpp
//  game_engine
//
//  Created by Jeremy Liu on 2/28/24.
//

#include "Component.hpp"

Component::Component() {
    enabled = true;
    num_runtime_components++;
}