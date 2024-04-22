//
// Created by Jeremy Liu on 3/27/24.
//

#include "Rigidbody.hpp"

Rigidbody::Rigidbody(luabridge::LuaRef &object) {
    type = object["type"].cast<std::string>();
    key = object["key"].cast<std::string>();
    actor = object["actor"].cast<Actor *>();
    enabled = object["enabled"].cast<bool>();
    x = object["x"].cast<float>();
    y = object["y"].cast<float>();
    body_type = object["body_type"].cast<std::string>();
    precise = object["precise"].cast<bool>();
    gravity_scale = object["gravity_scale"].cast<float>();
    density = object["density"].cast<float>();
    angular_friction = object["angular_friction"].cast<float>();
    rotation = object["rotation"].cast<float>();
    has_collider = object["has_collider"].cast<bool>();
    collider_type = object["collider_type"].cast<std::string>();
    width = object["width"].cast<float>();
    height = object["height"].cast<float>();
    radius = object["radius"].cast<float>();
    friction = object["friction"].cast<float>();
    bounciness = object["bounciness"].cast<float>();
    has_trigger = object["has_trigger"].cast<bool>();
    trigger_type = object["trigger_type"].cast<std::string>();
    trigger_width = object["trigger_width"].cast<float>();
    trigger_height = object["trigger_height"].cast<float>();
    trigger_radius = object["trigger_radius"].cast<float>();
}

b2Vec2 Rigidbody::get_position() const {
    if (body == nullptr) {
        return b2Vec2(x, y);
    }
    return {body->GetPosition().x, body->GetPosition().y};
}

float Rigidbody::get_rotation() const {
    return body->GetAngle() * (180.0f / b2_pi);
}

b2Vec2 Rigidbody::get_velocity() const {
    return {body->GetLinearVelocity().x, body->GetLinearVelocity().y};
}

float Rigidbody::get_angular_velocity() const {
    return body->GetAngularVelocity() * (180.0f / b2_pi);
}

float Rigidbody::get_gravity_scale() const {
    return gravity_scale;
}

b2Vec2 Rigidbody::get_up_direction() const {
    float angle = body->GetAngle();
    b2Vec2 result = b2Vec2(glm::sin(angle), -glm::cos(angle));
    result.Normalize();
    return result;
}

b2Vec2 Rigidbody::get_right_direction() const {
    float angle = body->GetAngle();
    b2Vec2 result = b2Vec2(glm::cos(angle), glm::sin(angle));
    result.Normalize();
    return result;
}

void Rigidbody::add_force(b2Vec2 force) {
    body->ApplyForceToCenter(force, true);
}

void Rigidbody::set_velocity(b2Vec2 velocity) {
    body->SetLinearVelocity(velocity);
}

void Rigidbody::set_position(b2Vec2 position) {
    if (body == nullptr) {
        x = position.x;
        y = position.y;
        return;
    }

    body->SetTransform({position.x, position.y}, body->GetAngle());
}

void Rigidbody::set_rotation(float degrees_clockwise) {
    body->SetTransform(body->GetPosition(), degrees_clockwise * (b2_pi / 180.0f));
}

void Rigidbody::set_angular_velocity(float velocity) {
    body->SetAngularVelocity(velocity * (b2_pi / 180.0f));
}

void Rigidbody::set_gravity_scale(float scale) {
    gravity_scale = scale;
    body->SetGravityScale(scale);
}

void Rigidbody::set_up_direction(b2Vec2 direction) {
    direction.Normalize();
    body->SetTransform(body->GetPosition(), glm::atan(direction.x, -direction.y));
}

void Rigidbody::set_right_direction(b2Vec2 direction) {
    direction.Normalize();
    body->SetTransform(body->GetPosition(), glm::atan(direction.x, -direction.y) - (b2_pi / 2.0f));
}

void Rigidbody::OnStart() {
    // define and create body
    b2BodyDef *body_def = new b2BodyDef();
    if (body_type == "dynamic") {
        body_def->type = b2_dynamicBody;
    } else if (body_type == "kinematic") {
        body_def->type = b2_kinematicBody;
    } else {
        body_def->type = b2_staticBody;
    }

    body_def->position = b2Vec2(x, y);
    body_def->gravityScale = gravity_scale;
    body_def->bullet = precise;
    body_def->angle = rotation * (b2_pi / 180.0f);
    body_def->angularDamping = angular_friction;

    body = Scene::box2d_world->CreateBody(body_def);

    if (!has_collider && !has_trigger) {
        b2FixtureDef *fixture = new b2FixtureDef();
        fixture->density = density;
        fixture->friction = friction;
        fixture->restitution = bounciness;
        fixture->userData.pointer = reinterpret_cast<uintptr_t>(actor);
        if (collider_type == "circle") {
            fixture->shape = new b2CircleShape();
            ((b2CircleShape *)fixture->shape)->m_radius = radius;
        } else {
            fixture->shape = new b2PolygonShape();
            ((b2PolygonShape *) fixture->shape)->SetAsBox(width / 2, height / 2);
        }

        fixture->filter.categoryBits = 0x0000;
        fixture->filter.maskBits = 0x0000;

        body->CreateFixture(fixture);
    } else if (has_trigger && !has_collider) {
        b2FixtureDef *trigger = new b2FixtureDef();
        trigger->friction = friction;
        trigger->restitution = bounciness;
        trigger->density = density;
        trigger->isSensor = true;
        trigger->userData.pointer = reinterpret_cast<uintptr_t>(actor);
        if (trigger_type == "circle") {
            trigger->shape = new b2CircleShape();
            ((b2CircleShape *)trigger->shape)->m_radius = trigger_radius;
        } else {
            trigger->shape = new b2PolygonShape();
            ((b2PolygonShape *) trigger->shape)->SetAsBox(trigger_width / 2, trigger_height / 2);
        }

        trigger->filter.categoryBits = 0x0002;
        trigger->filter.maskBits = 0x0002;

        body->CreateFixture(trigger);
    } else if (has_collider && !has_trigger) {
        b2FixtureDef *collider = new b2FixtureDef();
        collider->friction = friction;
        collider->restitution = bounciness;
        collider->density = density;
        collider->userData.pointer = reinterpret_cast<uintptr_t>(actor);
        if (collider_type == "circle") {
            collider->shape = new b2CircleShape();
            ((b2CircleShape *)collider->shape)->m_radius = radius;
        } else {
            collider->shape = new b2PolygonShape();
            ((b2PolygonShape *) collider->shape)->SetAsBox(width / 2, height / 2);
        }

        collider->filter.categoryBits = 0x0001;
        collider->filter.maskBits = 0x0001;

        body->CreateFixture(collider);
    } else {
        b2FixtureDef *collider = new b2FixtureDef();
        collider->friction = friction;
        collider->restitution = bounciness;
        collider->density = density;
        collider->userData.pointer = reinterpret_cast<uintptr_t>(actor);
        if (collider_type == "circle") {
            collider->shape = new b2CircleShape();
            ((b2CircleShape *)collider->shape)->m_radius = radius;
        } else {
            collider->shape = new b2PolygonShape();
            ((b2PolygonShape *) collider->shape)->SetAsBox(width / 2, height / 2);
        }

        collider->filter.categoryBits = 0x0001;
        collider->filter.maskBits = 0x0001;

        body->CreateFixture(collider);

        b2FixtureDef *trigger = new b2FixtureDef();
        trigger->friction = friction;
        trigger->restitution = bounciness;
        trigger->density = density;
        trigger->isSensor = true;
        trigger->userData.pointer = reinterpret_cast<uintptr_t>(actor);
        if (trigger_type == "circle") {
            trigger->shape = new b2CircleShape();
            ((b2CircleShape *)trigger->shape)->m_radius = trigger_radius;
        } else {
            trigger->shape = new b2PolygonShape();
            ((b2PolygonShape *) trigger->shape)->SetAsBox(trigger_width / 2, trigger_height / 2);
        }

        trigger->filter.categoryBits = 0x0002;
        trigger->filter.maskBits = 0x0002;

        body->CreateFixture(trigger);
    }
}

void Rigidbody::OnDestroy() {
    Scene::box2d_world->DestroyBody(body);
}

void ContactListener::BeginContact(b2Contact *contact) {
    b2Fixture *fixture_a = contact->GetFixtureA();
    Actor *actor_a = reinterpret_cast<Actor *>(fixture_a->GetUserData().pointer);
    b2Vec2 velocity_a = fixture_a->GetBody()->GetLinearVelocity();

    b2Fixture *fixture_b = contact->GetFixtureB();
    Actor *actor_b = reinterpret_cast<Actor *>(fixture_b->GetUserData().pointer);
    b2Vec2 velocity_b = fixture_b->GetBody()->GetLinearVelocity();

    // if it is a collision between two actors
    if (fixture_a->GetFilterData().categoryBits == 0x0001) {
        b2WorldManifold worldManifold;
        contact->GetWorldManifold(&worldManifold);
        actor_a->process_on_collision_enter(Collision(actor_b, worldManifold.points[0], velocity_a - velocity_b, worldManifold.normal));
        actor_b->process_on_collision_enter(Collision(actor_a, worldManifold.points[0], velocity_a - velocity_b, worldManifold.normal));
    } else if (fixture_a->GetFilterData().categoryBits == 0x0002) { // trigger
        actor_a->process_on_trigger_enter(Collision(actor_b, EMPTY, velocity_a - velocity_b, EMPTY));
        actor_b->process_on_trigger_enter(Collision(actor_a, EMPTY, velocity_a - velocity_b, EMPTY));
    }

}

void ContactListener::EndContact(b2Contact *contact) {
    b2Fixture *fixture_a = contact->GetFixtureA();
    Actor *actor_a = reinterpret_cast<Actor *>(fixture_a->GetUserData().pointer);
    b2Vec2 velocity_a = fixture_a->GetBody()->GetLinearVelocity();

    b2Fixture *fixture_b = contact->GetFixtureB();
    Actor *actor_b = reinterpret_cast<Actor *>(fixture_b->GetUserData().pointer);
    b2Vec2 velocity_b = fixture_b->GetBody()->GetLinearVelocity();

    if (fixture_a->GetFilterData().categoryBits == 0x0001) {
        actor_a->process_on_collision_exit(Collision(actor_b, EMPTY, velocity_a - velocity_b, EMPTY));
        actor_b->process_on_collision_exit(Collision(actor_a, EMPTY, velocity_a - velocity_b, EMPTY));
    } else if (fixture_a->GetFilterData().categoryBits == 0x0002) {
        actor_a->process_on_trigger_exit(Collision(actor_b, EMPTY, velocity_a - velocity_b, EMPTY));
        actor_b->process_on_trigger_exit(Collision(actor_a, EMPTY, velocity_a - velocity_b, EMPTY));
    }
}
