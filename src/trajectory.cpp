#include "trajectory.hpp"
#include <cstdio>
#include <algorithm>
#include <math.h>
#include <stdio.h>

namespace {
    inline float clampf(float x, float lo, float hi){
        return std::max(lo, std::min(hi, x));
    }
}

Trajectory::Trajectory(float max_vel, float max_accel, float max_decel, float s_curve_ratio, Vec2 start_pos, Vec2 end_pos, float threshold_dist)
    : max_vel(max_vel),
      max_acc(max_accel),
      max_dec(max_decel),
      s_curve_ratio(s_curve_ratio),
      start_pos(start_pos),
      end_pos(end_pos),
      thereshold_dist(threshold_dist),
      total_dist{0.0},
      acc_time{0.0},
      const_vel_time{0.0},
      total_time{0.0}
      {
}

#if defined(CIRCLE_TRAJECTORY)
void Trajectory::set_circle_params(float radius, float cx, float cy){
    radius_ = radius;
    cx_ = cx;
    cy_ = cy;
}
#endif

void Trajectory::calculate_s_curve_trajectory_params(){
    float s_curve_ratio_sq = s_curve_ratio * s_curve_ratio;
#if defined(LINE_TRAJECTORY)
    float dx = end_pos.x - start_pos.x;
    float dy = end_pos.y - start_pos.y;
    total_dist = std::sqrt(dx * dx + dy * dy);
#elif defined(CIRCLE_TRAJECTORY)
    float dtheta = end_pos.x - start_pos.x;//xを角度[rad]として使用
    total_dist = std::fabs(dtheta);//角度差
#endif
    if(total_dist <= thereshold_dist){
        // 移動距離がしきい値以下の場合、すべての時間をゼロに設定
        acc_time = 0.0;
        dec_time = 0.0;
        const_vel_time = 0.0;
        s_curve_time = 0.0;
        total_time = 0.0;
        return;
    }
    else{
        acc_time = max_vel / max_acc;
        dec_time = (max_vel * (1.0f - s_curve_ratio)) / max_dec;
        s_curve_time = 2.0f * (max_vel * s_curve_ratio) / max_dec;////S字軌道の時間
        float acc_dist_0 = 0.5f * max_acc * acc_time * acc_time;//加速距離
        float dec_dist_0 = 0.5f * max_vel * max_vel * (1.0f - s_curve_ratio_sq)/max_dec;//減速距離
        float s_curve_dist_0 = max_dec * s_curve_time * s_curve_time / 6.0f;//S字軌道の距離

        // 加速距離 + 減速距離 + S字軌道距離 が 総移動距離 を超える場合、等速時間を0に設定
        if(acc_dist_0 + dec_dist_0 + s_curve_dist_0 >= total_dist){
            const_vel_time = 0.0f;
            float inter_value = 0.5f / max_acc + 0.5f * (1.0f - s_curve_ratio_sq) / max_dec + (2.0f * s_curve_ratio_sq / 3.0f / max_dec);
            max_vel = std::sqrt(total_dist / inter_value);
            acc_time = max_vel / max_acc;
            dec_time = max_vel * (1.0f - s_curve_ratio) / max_dec;
            s_curve_time = 2.0f * max_vel * s_curve_ratio / max_dec;
            total_time = acc_time + dec_time + s_curve_time;
        }
        else{
            const_vel_time = (total_dist - acc_dist_0 - dec_dist_0 - s_curve_dist_0) / max_vel;
            total_time = acc_time + dec_time + const_vel_time + s_curve_time;
        }
    }
}

void Trajectory::calc_scalar_profile(float current_time, float acc_time, float const_vel_time, float dec_time, float s_curve_time, float max_acc, float max_dec, float max_vel, float total_dist, float s, float sd, float sdd) const {
    if(current_time <= acc_time){
        //加速区間
        // 水平方向の往復運動
        sdd = max_acc;
        sd = max_acc * current_time;
        s = 0.5f * max_acc * current_time * current_time;
    }
    else if(current_time <= (acc_time + const_vel_time )){
        // 定速区間
        float t_const = current_time - acc_time;
        sdd = 0.0f;
        sd = max_vel;
        s = 0.5f * max_acc * acc_time * acc_time + max_vel * t_const;
    }
    else if(current_time <= (acc_time + const_vel_time + dec_time)){
        // 減速区間
        float t_dec = current_time - acc_time - const_vel_time;
        sdd = -max_dec;
        sd = max_vel;
        s = 0.5f * max_acc * acc_time * acc_time + max_vel * const_vel_time + max_vel * t_dec - 0.5f * max_dec * t_dec * t_dec;
        
    }
    else if(current_time <= total_time){
        // S字軌道区間
        float t_s_curve = current_time - acc_time - const_vel_time - dec_time;
        float s_curve_acc = (max_dec / s_curve_time) * t_s_curve;
        sdd = -s_curve_acc;
        sd = max_vel - 0.5f * (max_dec / s_curve_time) * t_s_curve * t_s_curve;
        s = 0.5f * max_acc * acc_time * acc_time + max_vel * const_vel_time + max_vel * dec_time - 0.5f * max_dec * dec_time * dec_time + max_vel * t_s_curve - (max_dec / (6.0f * s_curve_time)) * t_s_curve * t_s_curve * t_s_curve;
    }
    else{
        // 目標位置に到達
        s = total_dist;
        sd = 0.0f;
        sdd = 0.0f;
    }
}

// 現在時刻tにおける目標位置, 目標速度, 目標加速度を計算する関数
void Trajectory::get_s_curve_state(float current_time, Vec2& target_pos, Vec2& target_vel, Vec2& target_acc) const {
    if(total_time <= 0.0f){
        target_pos = end_pos;
        target_vel = {0.0f, 0.0f};
        target_acc = {0.0f, 0.0f};
        return;
    }
    float s, sd, sdd;
    calc_scalar_profile(current_time, acc_time, const_vel_time, dec_time, s_curve_time, max_acc, max_dec, max_vel, total_dist, s, sd, sdd);
#if defined(LINE_TRAJECTORY)
    // 直線軌道: 始点→終点方向に
    float dx = end_pos.x - start_pos.x;
    float dy = end_pos.y - start_pos.y;
    float L = (total_dist > 1e-6f) ? total_dist : 1e-6f;
    float ux = dx / L;
    float uy = dy / L;

    target_pos.x = start_pos.x + ux * s;
    target_pos.y = start_pos.y + uy * s;
    target_vel.x = ux * sd;
    target_vel.y = uy * sd;
    target_acc.x = ux * sdd;
    target_acc.y = uy * sdd;
#elif defined(CIRCLE_TRAJECTORY)
    // 円軌道: 角度に基づいて位置を計算, start_pos.x / end_pos.x を角度[rad]とみなす
    float start_angle = start_pos.x;
    float end_angle = end_pos.x;
    float dir = (end_angle >= start_angle) ? 1.0f : -1.0f;

    float angle = start_angle + dir * s;//角度
    float angular_vel = dir * sd;//角速度
    float alpha = dir * sdd;//角加速度

    target_pos.x = cx_ + radius_ * cosf(angle);
    target_pos.y = cy_ + radius_ * sinf(angle);

    target_vel.x = -radius_ * sinf(angle) * angular_vel;
    target_vel.y = radius_ * cosf(angle) * angular_vel;
    
    target_acc.x = -radius_ * cosf(angle) * angular_vel * angular_vel - radius_ * sinf(angle) * alpha;
    target_acc.y = -radius_ * sinf(angle) * angular_vel * angular_vel
#endif
}

