//
//  AudioEngine.hpp
//  game_engine
//
//  Created by Jeremy Liu on 2/10/24.
//

#ifndef AudioEngine_hpp
#define AudioEngine_hpp

#include <stdio.h>
#include <string>
#include <unordered_map>
#include <filesystem>

#include "SDL2/SDL.h"
#include "SDL2_mixer/SDL_mixer.h"

#include "AudioHelper.h"

class AudioEngine {
private:
    static inline std::unordered_map<std::string, Mix_Chunk *> audio_store;
public:

    static void init();
    static void play(int channel, const std::string &audio_name, bool loops);
    static void stop(int channel);
    static void set_volume(int channel, int volume);
};

#endif /* AudioEngine_hpp */
