#ifndef DC_MOTOR_HPP
#define DC_MOTOR_HPP
#pragma once
#include <cstdint>
#include "hardware/pwm.h"

class DCMotor {
public:
    DCMotor() = default;                 
    void attach(uint pwm_pin, uint dir_pin);
    void begin(bool set_pwm_func = true, uint32_t pwm_hz = 20000);

    void setSpeed(float duty);           
    void stop();                         
    void set_pwm(float duty);            

private:
    bool     ready_     = false;
    uint     pwm_pin_   = 0;
    uint     dir_pin_   = 0;
    uint     slice_num_ = 0;
    uint     channel_   = 0;
    uint16_t top_       = 0;
};

#endif // DC_MOTOR_HPP
