//
//  GraphicsEngine.hpp
//  game_engine
//
//  Created by Jeremy Liu on 2/9/24.
//

#ifndef GraphicsEngine_hpp
#define GraphicsEngine_hpp

#include <stdio.h>
#include <string>
#include <unordered_map>
#include <cmath>
#include <queue>

#include "glm/glm.hpp"
#include "rapidjson/document.h"
#include "SDL2_ttf/SDL_ttf.h"
#include <pybind11/pybind11.h>

#include "Helper.h"
#include "AudioHelper.h"
#include "Actor.hpp"
#include "EngineUtils.hpp"
#include "LuaComponent.hpp"
#include "GameConfig.hpp"
#include "RenderingConfig.hpp"

static const inline float SCENE_UNIT = 100.0;

struct TextRender {
    SDL_Texture *texture;
    glm::ivec2 position;

    TextRender(SDL_Texture *texture, const glm::vec2 &position) : texture(texture), position(position) {}
};

struct DrawUIRender {
    SDL_Texture *texture;
    glm::ivec2 position;
    std::optional<SDL_Color> color;
    int sort_order;

    DrawUIRender(SDL_Texture *texture, const glm::vec2 &position, int sort_order) : texture(texture), position(position), sort_order(sort_order) {}
    DrawUIRender(SDL_Texture *texture, const glm::vec2 &position, SDL_Color color, int sort_order) : texture(texture), position(position), color(color), sort_order(sort_order) {}

    bool operator<(const DrawUIRender &other) const {
        return sort_order < other.sort_order;
    }
};

struct DrawRender {
    SDL_Texture *texture;
    glm::vec2 position;
    int rotation = 0;
    glm::vec2 scale = {1, 1};
    glm::vec2 pivot = {0.5, 0.5};
    std::optional<SDL_Color> color;
    int sort_order = 0;

    DrawRender(SDL_Texture *texture, const glm::vec2 &position) : texture(texture), position(position) {}
    DrawRender(SDL_Texture *texture, const glm::vec2 &position, int rotation, const glm::vec2 &scale, const glm::vec2 &pivot, SDL_Color color, int sort_order) : texture(texture), position(position), rotation(rotation), scale(scale), pivot(pivot), color(color), sort_order(sort_order) {}

    bool operator<(const DrawRender &other) const {
        return sort_order < other.sort_order;
    }
};

struct DrawPixelRender {
    glm::vec2 position;
    SDL_Color color;

    DrawPixelRender(const glm::vec2 &position, const SDL_Color &color) : position(position), color(color) {}
};



class GraphicsEngine {
private:
    // sdl essentials
    static inline SDL_Window *window;
    static inline SDL_Renderer *renderer;

    // rendering information
    static inline GameConfig game_config;
    static inline RenderingConfig rendering_config;

    static inline glm::vec2 camera_position;

    // render requests
    static inline std::deque<TextRender> text_queue;
    static inline std::vector<DrawUIRender> draw_ui_queue;
    static inline std::vector<DrawRender> draw_queue;
    static inline std::deque<DrawPixelRender> pixel_queue;
    
    // caching
    static inline std::unordered_map<std::string, std::unordered_map<int, TTF_Font*>> font_store; // TODO maybe cache text textures?
    static inline std::unordered_map<std::string, SDL_Texture *> image_store;

public:
    
    static void init(const GameConfig &game_config, const RenderingConfig &rendering_config);
    
    // wrappers for rendering
    static void render_clear();
    static void render();
    static void render_present();

    // render api routes
    static void draw_text(const std::string &text, int x, int y, const std::string &font_path, int font_size, SDL_Color color);
    static void draw_ui(const std::string &img_name, float x, float y);
    static void draw_ui_ex(const std::string &img_name, float x, float y, SDL_Color color, float sort_order);
    static void draw(const std::string &img_name, float x, float y);
    static void draw_ex(const std::string &img_name, float x, float y, float rotation_degrees, float scale_x, float scale_y, float pivot_x, float pivot_y, SDL_Color color, float sort_order);
    static void draw_pixel(float x, float y, SDL_Color color);

    // camera api routes
    static void set_position(float x, float y);
    static float get_camera_pos_x();
    static float get_camera_pos_y();
    static void set_camera_zoom(float zoom);
    static float get_camera_zoom();

    // helpers
    SDL_Texture* get_image_texture(const std::string &texture_name);
};

#endif /* GraphicsEngine_hpp */
