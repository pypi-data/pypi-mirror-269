//
// Created by Jeremy Liu on 3/30/24.
//

#include "Raycast.hpp"

/// return -1: ignore this fixture and continue
/// return 0: terminate the ray cast
/// return fraction: clip the ray to this point
/// return 1: don't clip the ray and continue
float Raycast::ReportFixture(b2Fixture *fixture, const b2Vec2 &point, const b2Vec2 &normal, float fraction) {
    // if its a phantom fixture, ignore it
    if (reinterpret_cast<Actor *>(fixture->GetUserData().pointer) == nullptr) {
        return -1;
    }

    // if the raycast starts inside the fixture, ignore it
    if (fixture->TestPoint(start_point)) {
        return -1;
    }

    // if object does not have any colliders, ignore it
    if (fixture->GetFilterData().categoryBits == 0) {
        return -1;
    }

    HitResult hit(reinterpret_cast<Actor *>(fixture->GetUserData().pointer), point, normal, fixture->IsSensor());
    hits.emplace_back(hit);

    return 1;
}

luabridge::LuaRef Raycast::raycast(const b2Vec2 &pos, const b2Vec2 &dir, float dist) {
    Raycast raycast(pos);
    b2Vec2 dir_normalized = dir;
    dir_normalized.Normalize();
    Scene::box2d_world->RayCast(&raycast, pos, (dist * dir_normalized) + pos);

    if (raycast.hits.empty()) {
        return luabridge::LuaRef(ComponentEngine::lua_state);
    }

    std::sort(raycast.hits.begin(), raycast.hits.end(), [&pos](const HitResult &a, const HitResult &b) {
        return (a.point - pos).LengthSquared() < (b.point - pos).LengthSquared();
    });
    return luabridge::LuaRef(ComponentEngine::lua_state, raycast.hits[0]);
}

luabridge::LuaRef Raycast::raycast_all(const b2Vec2 &pos, const b2Vec2 &dir, float dist) {
    Raycast raycast(pos);
    b2Vec2 dir_normalized = dir;
    dir_normalized.Normalize();
    Scene::box2d_world->RayCast(&raycast, pos, (dist * dir_normalized) + pos);

    luabridge::LuaRef hits_table = luabridge::newTable(ComponentEngine::lua_state);
    std::sort(raycast.hits.begin(), raycast.hits.end(), [&pos](const HitResult &a, const HitResult &b) {
        return (a.point - pos).LengthSquared() < (b.point - pos).LengthSquared();
    });
    for (int i = 0; i < raycast.hits.size(); i++) {
        hits_table[i + 1] = luabridge::LuaRef(ComponentEngine::lua_state, raycast.hits[i]);
    }

    return hits_table;
}