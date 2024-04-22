//
// Created by Jeremy Liu on 3/27/24.
//

#ifndef GAME_ENGINE_RIGIDBODY_HPP
#define GAME_ENGINE_RIGIDBODY_HPP

#include <string>

#include "box2d/box2d.h"
#include "box2d/b2_math.h"
#include "Scene.hpp"
#include "Actor.hpp"

class Actor;

inline const b2Vec2 EMPTY = {-999.0f, -999.0f};

class Rigidbody {
private:
    b2Body *body = nullptr;
public:
    // required properties for a component
    std::string type = "Rigidbody";
    std::string key = "???";
    Actor *actor = nullptr;
    bool enabled = true;

    // rigidbody properties
    float x = 0.0f;
    float y = 0.0f;
    std::string body_type = "dynamic";
    bool precise = true;
    float gravity_scale = 1.0f;
    float density = 1.0f;
    float angular_friction = 0.3f;
    float rotation = 0.0f;

    bool has_collider = true;
    std::string collider_type = "???";
    float width = 1.0f;
    float height = 1.0f;
    float radius = 0.5f;
    float friction = 0.3f;
    float bounciness = 0.3f;

    bool has_trigger = true;
    std::string trigger_type = "???";
    float trigger_width = 1.0f;
    float trigger_height = 1.0f;
    float trigger_radius = 0.5f;

    Rigidbody() = default;
    Rigidbody(luabridge::LuaRef &object);

    b2Vec2 get_position() const;
    float get_rotation() const;
    b2Vec2 get_velocity() const;
    float get_angular_velocity() const;
    float get_gravity_scale() const;
    b2Vec2 get_up_direction() const;
    b2Vec2 get_right_direction() const;

    void add_force(b2Vec2);
    void set_velocity(b2Vec2);
    void set_position(b2Vec2);
    void set_rotation(float);
    void set_angular_velocity(float);
    void set_gravity_scale(float);
    void set_up_direction(b2Vec2);
    void set_right_direction(b2Vec2);

    void OnStart();
    void OnDestroy();
};

class Collision {
public:
    Actor* other;
    b2Vec2 point;
    b2Vec2 relative_velocity;
    b2Vec2 normal;

    Collision();
    Collision(Actor* other, b2Vec2 point, b2Vec2 relative_velocity, b2Vec2 normal) : other(other), point(point), relative_velocity(relative_velocity), normal(normal) {}
};

class ContactListener : public b2ContactListener {
public:
    void BeginContact(b2Contact *contact) override;
    void EndContact(b2Contact *contact) override;
};


#endif //GAME_ENGINE_RIGIDBODY_HPP
