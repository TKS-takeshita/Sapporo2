#include "PID.hpp"

PDControl::PDControl(float Kp, float Kd, float tau)
    : Kp_(Kp),
      Kd_(Kd),
      tau_(tau),
      prev_error(0.0f),
      d_filtered(0.0f),
      first(true),
      error_lpf()
{
    setTau(tau);
}

void PDControl::setGains(float Kp, float Kd){
    Kp_ = Kp;
    Kd_ = Kd;
}

void PDControl::setTau(float tau){
    tau_ = tau;
    if(tau_ > 0.0f){
        error_lpf = low_pass_fillter(cutoff);
    }
    else{
        error_lpf = low_pass_fillter(0.0f);
    }
    error_lpf.reset();
    first = true;
    d_filtered = 0.0f;
    prev_error = 0.0f;
}

void PDControl::reset(float init_error){
    prev_error = init_error;
    d_filtered = 0.0f;
    first = true;
    error_lpf.reset();
}

float PDControl::update(float ref, float value){
    float error = ref - value;//角速度誤差
    if(first){
        prev_error = error;
        d_filtered = 0.0f;
        first = false;
    }

    int ret = error_lpf.update(error);
    if(ret < 0){
        error_lpf.reset();
        d_filtered = 0.0f;
    }
    else{
        d_filtered = error_lpf.get_dot_value();
    }
    float u = Kp_ * error + Kd_ * d_filtered;

    prev_error = error;
    return u;
}