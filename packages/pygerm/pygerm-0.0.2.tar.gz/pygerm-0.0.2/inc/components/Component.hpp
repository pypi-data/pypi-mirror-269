//
//  Component.hpp
//  game_engine
//
//  Created by Jeremy Liu on 2/28/24.
//

#ifndef Component_hpp
#define Component_hpp

#include <any>
#include <string>
#include <stdio.h>
#include <variant>
#include <iostream>

#include <pybind11/pybind11.h>

#include "Actor.hpp"

class Actor;

class Component {
private:
    
public:
    static inline int num_runtime_components = 0;

    bool enabled;
    std::string key;
    Actor* actor;

    Component();
    virtual void onStart() {};
    virtual void onUpdate() {};
    virtual void onLateUpdate() {};
    virtual void onDestroy() {};
};

#endif /* Component_hpp */
