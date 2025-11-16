#pragma once
#include "pico/stdlib.h"
#include "hardware/i2c.h"
#include <cstdint>
#include <cmath>
#include "low_pass_fillter.hpp"


class AS5601 {
public:

    static constexpr uint8_t I2C_ADDR = 0x36;
    enum : uint8_t {
        REG_ZMCO      = 0x00, 
        REG_ZPOS_H    = 0x01, 
        REG_ZPOS_L    = 0x02, 
        REG_STATUS    = 0x0B, 
        REG_RAW_ANG_H = 0x0C,
        REG_RAW_ANG_L = 0x0D, 
        REG_ANG_H     = 0x0E,
        REG_ANG_L     = 0x0F,
    };

    static constexpr uint8_t STATUS_MD = 0x20;
    static constexpr uint8_t STATUS_ML = 0x10;
    static constexpr uint8_t STATUS_MH = 0x08;

    static constexpr uint16_t kMaxCounts = 4096; // 0..4095
    static constexpr float    kTwoPi     = 6.28318530717958647692f;

    explicit AS5601(i2c_inst_t* i2c = i2c0, uint8_t addr7bit = I2C_ADDR)
    : i2c_(i2c), addr_(addr7bit) {}
    bool begin(uint sda_pin, uint scl_pin, uint32_t baudrate_hz = 400000, float velocity_cutoff_freq = 200.0f);

    bool readRawAngleCounts(uint16_t& counts);
    float readAngle(uint16_t& counts);

    bool readRawAngleRad(float& rad);
    bool readAngleRad(float& rad);

    bool readRawAngleDeg(float& deg);
    bool readAngleDeg(float& deg);

    bool readStatus(uint8_t& status);
    bool isMagnetDetected(bool& ok);
    bool isMagnetTooWeak(bool& weak);
    bool isMagnetTooStrong(bool& strong);

    bool setZeroPosition(uint16_t zpos);
    bool setZeroAtCurrentPosition();

    bool readZMCO(uint8_t& zmco);

    void setDiffGain(float g) {diff_g_ = g;}
    // 角速度を計算
    // dt_sec : 経過時間[秒]
    // omega_rad : 角速度[ラジアン/秒]の出力
    bool updateAngularVelocity(float dt_sec, float current_angle_rad, float& omega_rad);

private:
    i2c_inst_t* i2c_;
    uint8_t     addr_;
    float previous_angle_rad; //前回の角度[ラジアン]
    uint16_t prev_count;
    float angular_velocity_rad;//角速度
    uint32_t previous_time_us; //前回の時間[マイクロ秒]
    bool velocity_initialized; //角速度初期化
    bool minus_count;
    bool plus_count;
    low_pass_fillter velocity_filter;//角速度ローパスフィルタ

    bool readRegisters(uint8_t reg, uint8_t* buf, size_t len);
    bool writeRegisters(uint8_t reg, const uint8_t* buf, size_t len);

    static uint16_t combine12(const uint8_t hi, const uint8_t lo) {
        return (static_cast<uint16_t>(hi & 0x0F) << 8) | static_cast<uint16_t>(lo);
    }

    static float countsToRad(uint16_t c) {
        return (static_cast<float>(c) * kTwoPi) / static_cast<float>(kMaxCounts);
    }
    static float countsToDeg(uint16_t c) {
        return (static_cast<float>(c) * 360.0f) / static_cast<float>(kMaxCounts);
    }

    bool diff_initialized_ = false;
    uint16_t prev_counts_ = 0;
    float theta_unwrapped_ = 0.0f;//連続角度[ラジアン]
    float x_state_ = 0.0f; //1次遅れ内部状態x
    float omega_state_ = 0.0f; //出力保持
    float diff_g_ = 500.0f; //カットオフ周波数[rad/sec]

};
