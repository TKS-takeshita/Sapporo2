#pragma once
#include <cstdint>
#include "low_pass_fillter.hpp"

class PDControl {
public:
    PDControl(float Kp = 0.0f, float Kd = 0.0f, float tau = 0.0f);
    //目標値ref, 現在地value
    float update(float ref, float value);

    void reset(float init_error = 0.0f);
    void setGains(float Kp, float Kd);
    void setTau(float tau);

private:
    float Kp_;
    float Kd_;
    float tau_;

    float prev_error;
    float d_filtered;
    bool first;
    float cutoff = 100.0f;
    low_pass_fillter error_lpf;
};