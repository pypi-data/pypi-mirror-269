//
//  AudioEngine.cpp
//  game_engine
//
//  Created by Jeremy Liu on 2/10/24.
//

#include "AudioEngine.hpp"

void AudioEngine::init() {
    SDL_Init(SDL_INIT_AUDIO);
    AudioHelper::Mix_OpenAudio498(44100, MIX_DEFAULT_FORMAT, 2, 2048);
    AudioHelper::Mix_AllocateChannels498(50);
    
    // TODO preload all audios into store
}

void AudioEngine::play(int channel, const std::string &audio_path, bool loops) {
    if (audio_store.find(audio_path) == audio_store.end()) {
        if (!std::filesystem::exists(audio_path)) {
            throw std::runtime_error("Audio file not found: " + audio_path);
        }
        
        audio_store[audio_path] = AudioHelper::Mix_LoadWAV498(audio_path.c_str());
    }
    
    AudioHelper::Mix_PlayChannel498(channel, audio_store[audio_path], loops ? -1 : 0);
}

void AudioEngine::stop(int channel) {
    AudioHelper::Mix_HaltChannel498(channel);
}

void AudioEngine::set_volume(int channel, int volume) {
    AudioHelper::Mix_Volume498(channel, volume);
}
