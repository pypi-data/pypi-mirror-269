//
//  GraphicsEngine.cpp
//  game_engine
//
//  Created by Jeremy Liu on 2/9/24.
//

#include "GraphicsEngine.hpp"

void GraphicsEngine::init(const GameConfig &init_game_config, const RenderingConfig &init_rendering_config) {
    game_config = init_game_config;
    rendering_config = init_rendering_config;

    SDL_Init(SDL_INIT_VIDEO);
    TTF_Init();
    window = Helper::SDL_CreateWindow498(game_config.game_title.c_str(),
                                         SDL_WINDOWPOS_UNDEFINED,
                                         SDL_WINDOWPOS_UNDEFINED,
                                         rendering_config.x_resolution,
                                         rendering_config.y_resolution,
                                         SDL_WINDOW_SHOWN
                                         );
    renderer = Helper::SDL_CreateRenderer498(window, -1, SDL_RENDERER_PRESENTVSYNC | SDL_RENDERER_ACCELERATED);

    // TODO possibly preload images?
}

void GraphicsEngine::render_clear() {
    SDL_SetRenderDrawColor(renderer, rendering_config.clear_color.r, rendering_config.clear_color.g, rendering_config.clear_color.b, rendering_config.clear_color.a);
    SDL_RenderClear(renderer);
}

void GraphicsEngine::render() {
    // handle draw requests
    SDL_RenderSetScale(renderer, rendering_config.zoom_factor, rendering_config.zoom_factor);
    std::stable_sort(draw_queue.begin(), draw_queue.end());
    for (auto &draw_request : draw_queue) {
        int flip = 0;
        if (draw_request.scale.x < 0) { flip |= SDL_FLIP_HORIZONTAL; }
        if (draw_request.scale.y < 0) { flip |= SDL_FLIP_VERTICAL; }

        if (draw_request.color.has_value()) {
            SDL_SetTextureColorMod(draw_request.texture, draw_request.color.value().r, draw_request.color.value().g, draw_request.color.value().b);
            SDL_SetTextureAlphaMod(draw_request.texture, draw_request.color.value().a);
        }

        int w, h;
        SDL_QueryTexture(draw_request.texture, nullptr, nullptr, &w, &h);

        SDL_Point center;
        center.x = static_cast<int>(draw_request.pivot.x * w * std::abs(draw_request.scale.x));
        center.y = static_cast<int>(draw_request.pivot.y * h * std::abs(draw_request.scale.y));

        SDL_Rect destRect {static_cast<int>(draw_request.position.x), static_cast<int>(draw_request.position.y), 0, 0};
        destRect.x = static_cast<int>((draw_request.position.x - camera_position.x) * SCENE_UNIT + rendering_config.x_resolution * 0.5f / rendering_config.zoom_factor - center.x);
        destRect.y = static_cast<int>((draw_request.position.y - camera_position.y) * SCENE_UNIT + rendering_config.y_resolution * 0.5f / rendering_config.zoom_factor - center.y);
        destRect.w = w * std::abs(draw_request.scale.x);
        destRect.h = h * std::abs(draw_request.scale.y);

        Helper::SDL_RenderCopyEx498(renderer, draw_request.texture, nullptr, &destRect, static_cast<int>(draw_request.rotation), &center, static_cast<SDL_RendererFlip>(flip));
    }
    draw_queue.clear();
    SDL_RenderSetScale(renderer, 1, 1);

    // render draw UI
    std::stable_sort(draw_ui_queue.begin(), draw_ui_queue.end());
    for (auto &draw_ui_request : draw_ui_queue) {
        SDL_Rect destRect {draw_ui_request.position.x, draw_ui_request.position.y, 0, 0};
        SDL_QueryTexture(draw_ui_request.texture, nullptr, nullptr, &destRect.w, &destRect.h);
        if (draw_ui_request.color.has_value()) {
            SDL_SetTextureColorMod(draw_ui_request.texture, draw_ui_request.color.value().r, draw_ui_request.color.value().g, draw_ui_request.color.value().b);
            SDL_SetTextureAlphaMod(draw_ui_request.texture, draw_ui_request.color.value().a);
        }
        SDL_RenderCopy(renderer, draw_ui_request.texture, nullptr, &destRect);
    }
    draw_ui_queue.clear();

    // render text
    while (!text_queue.empty()) {
        TextRender text_render = text_queue.front();
        SDL_RenderSetScale(renderer, 1.0, 1.0);

        SDL_Rect destRect{text_render.position.x, text_render.position.y, 0, 0};
        SDL_QueryTexture(text_render.texture, nullptr, nullptr, &destRect.w, &destRect.h);
        SDL_RenderCopy(renderer, text_render.texture, nullptr, &destRect);
        text_queue.pop_front();
    }

    SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND);
    while (!pixel_queue.empty()) {
        DrawPixelRender pixel_render = pixel_queue.front();
        SDL_SetRenderDrawColor(renderer, pixel_render.color.r, pixel_render.color.g, pixel_render.color.b, pixel_render.color.a);
        SDL_RenderDrawPoint(renderer, pixel_render.position.x, pixel_render.position.y);
        pixel_queue.pop_front();
    }
    SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_NONE);
}

void GraphicsEngine::render_present() {
    Helper::SDL_RenderPresent498(renderer);
}

void GraphicsEngine::draw_text(const std::string &text, int x, int y, const std::string &font_path, int font_size, SDL_Color color) {
    if (font_store.find(font_path) == font_store.end() || font_store[font_path].find(font_size) == font_store[font_path].end()) {
        if (!std::filesystem::exists(font_path)) {
            throw std::runtime_error("Invalid font path");
        }

        try {
            font_store[font_path][font_size] = TTF_OpenFont(font_path.c_str(), font_size);
        } catch (std::exception &e) {
            throw std::runtime_error("Invalid font path or file format. file_path must be of type .ttf");
        }
    }

    SDL_Surface *surface = TTF_RenderText_Solid(font_store[font_path][font_size], text.c_str(), color);
    SDL_Texture *texture = SDL_CreateTextureFromSurface(renderer, surface);

    text_queue.emplace_back(TextRender(texture, glm::vec2(x, y)));
}

void GraphicsEngine::draw_ui(const std::string &img_name, float x, float y) {
    if (image_store.find(img_name) == image_store.end()) {
        std::string filename = std::string("./resources/images/") + img_name + std::string(".png");
        if (!std::filesystem::exists(filename)) {
            std::cout << "error: missing image " << img_name;
            exit(0);
        }

        image_store[img_name] = IMG_LoadTexture(renderer, filename.c_str());
    }

    draw_ui_queue.emplace_back(DrawUIRender(image_store[img_name], glm::vec2(x, y), 0));
}

void GraphicsEngine::draw_ui_ex(const std::string &img_path, float x, float y, SDL_Color color, float sort_order) {
    if (image_store.find(img_path) == image_store.end()) {
        if (!std::filesystem::exists(img_path)) {
            throw std::runtime_error("Invalid image path: " + img_path);
        }

        image_store[img_path] = IMG_LoadTexture(renderer, img_path.c_str());
    }

    draw_ui_queue.emplace_back(DrawUIRender(image_store[img_path], glm::vec2(x, y), color, sort_order));
}

void GraphicsEngine::draw(const std::string &img_name, float x, float y) {
    if (image_store.find(img_name) == image_store.end()) {
        std::string filename = std::string("./resources/images/") + img_name + std::string(".png");
        if (!std::filesystem::exists(filename)) {
            std::cout << "error: missing image " << img_name;
            exit(0);
        }

        image_store[img_name] = IMG_LoadTexture(renderer, filename.c_str());
    }

    draw_queue.emplace_back(DrawRender(image_store[img_name], glm::vec2(x, y)));
}

void GraphicsEngine::draw_ex(const std::string &img_path, float x, float y, float rotation_degrees, float scale_x, float scale_y, float pivot_x, float pivot_y, SDL_Color color, float sort_order) {
    if (image_store.find(img_path) == image_store.end()) {
        if (!std::filesystem::exists(img_path)) {
            throw std::runtime_error("Invalid image path: " + img_path);
        }

        image_store[img_path] = IMG_LoadTexture(renderer, img_path.c_str());
    }

    draw_queue.emplace_back(DrawRender(image_store[img_path], glm::vec2(x, y), rotation_degrees, glm::vec2(scale_x, scale_y), glm::vec2(pivot_x, pivot_y), color, sort_order));
}

void GraphicsEngine::draw_pixel(float x, float y, SDL_Color color) {
    pixel_queue.emplace_back(DrawPixelRender(glm::vec2(x, y), color));
}

void GraphicsEngine::set_position(float x, float y) {
    camera_position = glm::vec2(x, y);
}

float GraphicsEngine::get_camera_pos_x() {
    return camera_position.x;
}

float GraphicsEngine::get_camera_pos_y() {
    return camera_position.y;
}

void GraphicsEngine::set_camera_zoom(float zoom) {
    rendering_config.zoom_factor = zoom;
}

float GraphicsEngine::get_camera_zoom() {
    return rendering_config.zoom_factor;
}