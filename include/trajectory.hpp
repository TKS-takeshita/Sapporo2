#pragma once 
#include <stdbool.h>

//  台形速度軌道生成クラス
//  台形速度プロファイルを生成し、目標位置・速度・加速度を計算

#define LINE_TRAJECTORY//直線軌道
// #define CIRCLE_TRAJECTORY//円軌道

struct Vec2{
    float x;
    float y;
};

class Trajectory{
    private: 
        float max_vel;// 最高速度
        float max_acc;// 最高加速度
        float max_dec;// 最高減速度
        float s_curve_ratio;// S字加減速比率
        float s_curve_time;// S字加減速時間
        Vec2 start_pos;// 開始位置
        Vec2 end_pos;// 目標位置
        float thereshold_dist;//移動距離がこの値以下のとき、すべての時間をゼロに設定
        float total_dist;
        float acc_time;// 加速時間
        float dec_time;// 減速時間
        float const_vel_time; // 等速時間
        float total_time;// 総移動時間

    public:
        Trajectory(float max_vel, float max_acc, float max_dec, float s_curve_ratio, Vec2 start_pos, Vec2 end_pos, float thereshold_dist);
        // S字軌道パラメータを計算する関数
        void calculate_s_curve_trajectory_params();
        void calc_scalar_profile(float current_time, float acc_time, float const_vel_time, float dec_time, float s_curve_time, float max_acc, float max_dec, float max_vel, float total_dist, float s, float sd, float sdd) const;
        // 現在時刻tにおける目標位置, 目標速度, 目標加速度を計算する関数
        void get_s_curve_state(float current_time, Vec2& target_pos, Vec2& target_vel, Vec2& target_acc) const;
    #if defined(CIRCLE_TRAJECTORY)
        // 円軌道用の関数をここに追加
        void set_circle_params(float radius, float cx, float cy);
        void get_circle_xy(float& x, float& y) const;
    private:
        float radius_{0.0f};
        float cx_{0.0f};
        float cy_{0.0f};
    #endif
        // ゲッター関数
        float get_max_vel() const { return max_vel; }
        float get_max_acc() const { return max_acc; }
        Vec2 get_start_pos() const { return start_pos; }
        Vec2 get_end_pos() const { return end_pos; }
        float get_total_dist() const { return total_dist; }
        float get_acc_time() const { return acc_time; }
        float get_const_vel_time() const { return const_vel_time; }
        float get_total_time() const { return total_time; }

        // セッター関数
        void set_max_vel(float max_v) { max_vel = max_v; }
        void set_max_acc(float max_a) { max_acc = max_a; }
        void set_start_pos(Vec2 start_p) { start_pos = start_p; }
        void set_end_pos(Vec2 end_p) { end_pos = end_p; }
};  