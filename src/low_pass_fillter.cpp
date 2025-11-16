#include "low_pass_fillter.hpp"
#include "pico/stdlib.h"
#include "pico/time.h"

low_pass_fillter::low_pass_fillter()
    : cutoff_freq(0.0f),
      previous_time_us_uint32_t(0),
      lpf_value(0.0f),
      dot_value(0.0f),
      is_initialized(false)
{
}

low_pass_fillter::low_pass_fillter(float cutoff_freq)
    :cutoff_freq(cutoff_freq),
    is_initialized(false),
    previous_time_us_uint32_t(0),
    lpf_value(0.0f),
    dot_value(0.0f)
{
    reset();
}

bool low_pass_fillter::reset(){
    dot_value = 0.0f;
    is_initialized = false;
    return true;
}

float low_pass_fillter::get_lpf_value() const{
    return lpf_value;
}

float low_pass_fillter::get_dot_value() const{
    return dot_value;
}

int low_pass_fillter::update(float new_value){
    uint32_t current_time = time_us_32();
    uint32_t delta_time_us_uint32_t = current_time - previous_time_us_uint32_t;
    if(!is_initialized){
        previous_time_us_uint32_t = current_time;
        lpf_value = new_value;
        dot_value = 0.0f;
        is_initialized = true;
        return 1;
    }

    if(delta_time_us_uint32_t == 0 || delta_time_us_uint32_t > 10'000U){
        reset();
        return -1;//エラーコード
    }

    float delta_time_s = static_cast<float>(delta_time_us_uint32_t) * 1e-6f;
    dot_value = (new_value - lpf_value) * cutoff_freq;
    lpf_value += dot_value * delta_time_s;
    previous_time_us_uint32_t = current_time;
    return 0;
}