//
// Created by Jeremy Liu on 4/20/24.
//

#ifndef PYGERM_APPLICATION_HPP
#define PYGERM_APPLICATION_HPP

#include <thread>
#include <chrono>

#include "Helper.h"

class Application {
public:
    static void quit();
    static void sleep(int dur_ms);
    static int get_frame();
    static void open_url(const std::string &url);
};


#endif //PYGERM_APPLICATION_HPP
