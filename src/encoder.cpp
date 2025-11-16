#include "encoder.hpp"


bool AS5601::begin(uint sda_pin, uint scl_pin, uint32_t baudrate_hz, float velocity_cutoff_freq) {
    i2c_init(i2c_, baudrate_hz);
    gpio_set_function(sda_pin, GPIO_FUNC_I2C);
    gpio_set_function(scl_pin, GPIO_FUNC_I2C);
    gpio_pull_up(sda_pin);
    gpio_pull_up(scl_pin);
    uint8_t status = 0;
    previous_angle_rad = 0.0f;
    angular_velocity_rad = 0.0f;
    velocity_initialized = false;
    velocity_filter = low_pass_fillter(velocity_cutoff_freq);
    uint8_t buf[2];
    readRegisters(REG_ANG_H, buf, 2);
    prev_count = combine12(buf[0], buf[1]);
    minus_count = false;
    plus_count = false;
    return readStatus(status);
}

bool AS5601::readRegisters(uint8_t reg, uint8_t* buf, size_t len) {

    int w = i2c_write_blocking(i2c_, addr_, &reg, 1, true);
    if (w != 1) return false;
    int r = i2c_read_blocking(i2c_, addr_, buf, len, false);
    return (r == static_cast<int>(len));
}

bool AS5601::writeRegisters(uint8_t reg, const uint8_t* buf, size_t len) {
    uint8_t tmp[1 + 4];
    if (len > 4) return false;
    tmp[0] = reg;
    for (size_t i = 0; i < len; ++i) tmp[1 + i] = buf[i];

    int w = i2c_write_blocking(i2c_, addr_, tmp, 1 + len, false);
    return (w == static_cast<int>(1 + len));
}

bool AS5601::readRawAngleCounts(uint16_t& counts) {
    uint8_t buf[2];
    if (!readRegisters(REG_RAW_ANG_H, buf, 2)) return false;
    counts = combine12(buf[0], buf[1]);
    return true;
}

float AS5601::readAngle(uint16_t& counts) {
    uint8_t buf[2];
    readRegisters(REG_ANG_H, buf, 2);
    counts = combine12(buf[0], buf[1]);
    int16_t diff_count = (int16_t)counts - (int16_t)prev_count;
    prev_count = counts;
    if(diff_count > 2048) {
        minus_count = true;
    }
    if(diff_count < -2048) {
        minus_count = false;
    }    
    float rad = countsToRad(counts);
    if(minus_count){
        rad -= 2*M_PI;
    }
    return rad;
}

bool AS5601::readRawAngleRad(float& rad) {
    uint16_t c;
    if (!readRawAngleCounts(c)) return false;
    rad = countsToRad(c);
    return true;
}

bool AS5601::readAngleRad(float& rad) {
    uint16_t c;
    rad = readAngle(c);
    return true;
}

bool AS5601::readRawAngleDeg(float& deg) {
    uint16_t c;
    if (!readRawAngleCounts(c)) return false;
    deg = countsToDeg(c);
    return true;
}


bool AS5601::readStatus(uint8_t& status) {
    return readRegisters(REG_STATUS, &status, 1);
}

bool AS5601::isMagnetDetected(bool& ok) {
    uint8_t st;
    if (!readStatus(st)) return false;
    ok = (st & STATUS_MD) != 0;
    return true;
}

bool AS5601::isMagnetTooWeak(bool& weak) {
    uint8_t st;
    if (!readStatus(st)) return false;
    weak = (st & STATUS_ML) != 0;
    return true;
}

bool AS5601::isMagnetTooStrong(bool& strong) {
    uint8_t st;
    if (!readStatus(st)) return false;
    strong = (st & STATUS_MH) != 0;
    return true;
}

bool AS5601::setZeroPosition(uint16_t zpos) {
    zpos &= 0x0FFF;
    uint8_t hi = static_cast<uint8_t>((zpos >> 8) & 0x0F);
    uint8_t lo = static_cast<uint8_t>(zpos & 0xFF);
    if (!writeRegisters(REG_ZPOS_H, &hi, 1)) return false;
    if (!writeRegisters(REG_ZPOS_L, &lo, 1)) return false;
    return true;
}

bool AS5601::setZeroAtCurrentPosition() {
    uint16_t cur;
    if (!readRawAngleCounts(cur)) return false;
    return setZeroPosition(cur);
}

bool AS5601::readZMCO(uint8_t& zmco) {
    return readRegisters(REG_ZMCO, &zmco, 1);
}


bool AS5601::updateAngularVelocity(float dt_sec, float current_angle_rad, float& omega_rad) {
    float delta_angle_rad = current_angle_rad - previous_angle_rad;
    velocity_filter.update(current_angle_rad);
    omega_rad = velocity_filter.get_dot_value();
    
    const float MAX_ANGULAR_VELOCITY = 10.786f; //最大角速度[rad/s] 103PRM
    if(fabs(omega_rad) > MAX_ANGULAR_VELOCITY){
        if(omega_rad < 0){
            omega_rad = -MAX_ANGULAR_VELOCITY;
        }
        else{
            omega_rad = MAX_ANGULAR_VELOCITY;
        }
        previous_angle_rad = current_angle_rad;
        return true;
    }
    previous_angle_rad = current_angle_rad;
    return true;
}