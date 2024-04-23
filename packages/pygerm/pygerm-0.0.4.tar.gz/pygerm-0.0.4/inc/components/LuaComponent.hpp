////
////  LuaComponent.hpp
////  game_engine
////
////  Created by Jeremy Liu on 2/28/24.
////
//
//#ifndef LuaComponent_hpp
//#define LuaComponent_hpp
//
//#include <any>
//#include <memory>
//#include <string>
//#include <cstdio>
//
//#include "lua/lua.hpp"
//#include "LuaBridge/LuaBridge.h"
//
//#include "Component.hpp"
//#include "ComponentEngine.hpp"
//
//class Component;
//
//class LuaComponent : public Component {
//private:
//    luabridge::LuaRef state;
//public:
//    LuaComponent(luabridge::LuaRef);
//    LuaComponent(const LuaComponent &);
//
//    std::shared_ptr<LuaComponent> copy();
//    luabridge::LuaRef get_ref();
//
//    void onStart() override;
//    void onUpdate() override;
//    void onLateUpdate() override;
//    void onDestroy() override;
//};
//
//#endif /* LuaComponent_hpp */
