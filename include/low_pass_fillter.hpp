#pragma once
#include <cstdint>


class low_pass_fillter{
    public:
        low_pass_fillter();
        low_pass_fillter(float cutoff_freq);
        // 初期化
        bool reset();
        float get_lpf_value() const;
        float get_dot_value() const;

        int update(float new_value);

    private:
        float cutoff_freq; //カットオフ周波数
        uint32_t previous_time_us_uint32_t; //前回の時間[us]
        float lpf_value;//フィルタ済み値
        float dot_value;//変化量
        bool is_initialized;
};
