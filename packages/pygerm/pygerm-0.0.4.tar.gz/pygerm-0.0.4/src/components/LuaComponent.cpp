////
////  LuaComponent.cpp
////  game_engine
////
////  Created by Jeremy Liu on 2/28/24.
////
////
//
//#include "Actor.hpp"
//#include "LuaComponent.hpp"
//
//LuaComponent::LuaComponent(luabridge::LuaRef parent_table) : state(luabridge::newTable(ComponentEngine::lua_state)) {
//    ComponentEngine::establish_inheretance(state, parent_table);
//};
//
//LuaComponent::LuaComponent(const LuaComponent &other) : state(luabridge::newTable(ComponentEngine::lua_state)) {
//    ComponentEngine::establish_inheretance(state, other.state);
//}
//
//std::shared_ptr<LuaComponent> LuaComponent::copy() {
//    return std::make_shared<LuaComponent>(*this);
//}
//
//luabridge::LuaRef LuaComponent::get_ref() {
//    return state;
//}
//
////void LuaComponent::set(std::string key, std::any value) {
////    if (value.type() == typeid(bool)) {
////        state[key] = std::any_cast<bool>(value);
////    } else if (value.type() == typeid(int)) {
////        state[key] = std::any_cast<int>(value);
////    } else if (value.type() == typeid(float)) {
////        state[key] = std::any_cast<float>(value);
////    } else if (value.type() == typeid(std::string)) {
////        state[key] = std::any_cast<std::string>(value);
////    } else if (value.type() == typeid(Actor *)) {
////        state[key] = std::any_cast<Actor *>(value);
////    } else {
////        std::cout << "unspported type in LuaComponent::set at the current moment " << value.type().name() << std::endl;
////        exit(1);
////    }
////}
////
////void LuaComponent::set_key(std::string key_name) {
////    Component::set_key(key_name);
////    set("key", key_name);
////}
//
//void LuaComponent::onStart() {
//    if (!state["OnStart"].isNil() && state["enabled"].cast<bool>()) {
//        state["OnStart"](state);
//    }
//}
//
//void LuaComponent::onUpdate() {
//    if (!state["OnUpdate"].isNil() && state["enabled"].cast<bool>()) {
//        state["OnUpdate"](state);
//    }
//}
//
//void LuaComponent::onLateUpdate() {
//    if (!state["OnLateUpdate"].isNil() && state["enabled"].cast<bool>()) {
//        state["OnLateUpdate"](state);
//    }
//}
