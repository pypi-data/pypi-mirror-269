//
// Created by Jeremy Liu on 3/30/24.
//

#ifndef GAME_ENGINE_RAYCAST_HPP
#define GAME_ENGINE_RAYCAST_HPP

#include <vector>

#include <box2d/box2d.h>

#include "Actor.hpp"

class Actor;

class HitResult {
public:
    Actor *actor;
    b2Vec2 point;
    b2Vec2 normal;
    bool is_trigger;

    HitResult() : actor(nullptr), point(b2Vec2_zero), normal(b2Vec2_zero), is_trigger(false) {}
    HitResult(Actor *actor, b2Vec2 point, b2Vec2 normal, bool is_trigger) : actor(actor), point(point), normal(normal), is_trigger(is_trigger) {}
};

class Raycast : public b2RayCastCallback {
private:
    b2Vec2 start_point = b2Vec2_zero;
public:
    std::vector<HitResult> hits;

    Raycast(b2Vec2 start_point) : start_point(start_point) {}

    float ReportFixture(b2Fixture* fixture, const b2Vec2& point, const b2Vec2& normal, float fraction) override;
    static luabridge::LuaRef raycast(const b2Vec2 &pos, const b2Vec2 &dir, float dist);
    static luabridge::LuaRef raycast_all(const b2Vec2 &pos, const b2Vec2 &dir, float dist);
};


#endif //GAME_ENGINE_RAYCAST_HPP
