//
// Created by Jeremy Liu on 4/20/24.
//

#include "Application.hpp"

void Application::quit() {
    exit(0);
}

void Application::sleep(int dur_ms) {
    std::this_thread::sleep_for(std::chrono::milliseconds(dur_ms));
}

int Application::get_frame() {
    return Helper::GetFrameNumber();
}

void Application::open_url(const std::string &url) {
#ifdef _WIN32
    std::system(("start " + url).c_str());
#elif __APPLE__
    std::system(("open " + url).c_str());
#else
    std::system(("xdg-open " + url).c_str());
#endif
}