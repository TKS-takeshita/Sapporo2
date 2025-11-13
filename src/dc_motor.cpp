#include "dc_motor.hpp"
#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/pwm.h"
#include "hardware/clocks.h"
#include <cmath>

void DCMotor::attach(uint pwm_pin, uint dir_pin) {
    pwm_pin_ = pwm_pin;
    dir_pin_ = dir_pin;
    ready_   = false;
}

void DCMotor::begin(bool set_pwm_func, uint32_t pwm_hz) {
    if (set_pwm_func) {
        gpio_set_function(pwm_pin_, GPIO_FUNC_PWM);
    }
    slice_num_ = pwm_gpio_to_slice_num(pwm_pin_);
    channel_   = pwm_gpio_to_channel(pwm_pin_);

    uint32_t clk = clock_get_hz(clk_sys);
    if (clk == 0) clk = 125000000u;

    uint32_t top32 = (clk / pwm_hz) - 1u;
    if (top32 > 0xFFFFu) top32 = 0xFFFFu;
    top_ = static_cast<uint16_t>(top32);

    pwm_config cfg = pwm_get_default_config();
    pwm_config_set_wrap(&cfg, top_);
    pwm_config_set_clkdiv(&cfg, 1.0f);

    pwm_init(slice_num_, &cfg, false);
    pwm_set_chan_level(slice_num_, channel_, 0);
    pwm_set_enabled(slice_num_, true);

    ready_ = true;
    stop();
}

void DCMotor::set_pwm(float duty){
    if (!ready_) return;
    if (duty < 0.0f) duty = 0.0f;
    if (duty > 1.0f) duty = 1.0f;
    uint16_t level = static_cast<uint16_t>(duty * top_);
    pwm_set_chan_level(slice_num_, channel_, level);
}

void DCMotor::setSpeed(float duty){
    if (!ready_) return;
    if (duty > 1.0f) duty = 1.0f;
    if (duty < -1.0f) duty = -1.0f;

    gpio_put(dir_pin_, duty >= 0.0f);
    set_pwm(std::fabs(duty));
}

void DCMotor::stop() {
    if (!ready_) return;
    set_pwm(0.0f);
}
