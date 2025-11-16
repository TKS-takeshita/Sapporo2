#include "config.hpp"

DCMotor motor1;
DCMotor motor2;

AS5601 enc1(i2c0);
AS5601 enc2(i2c1);

struct RefState{
    float x;
    float y;
    float vx;
    float vy;
    float ax;
    float ay;
    bool valid;
};
RefState g_ref;

PDControl pid_omega1(Kp1, Kd1, tau1);
PDControl pid_omega2(Kp2, Kd2, tau2);

float motor1_line_trajectory(float x_ref, float y_ref, float vx_ref, float vy_ref, float ax_ref, float ay_ref){
    float r_ref_sq = x_ref * x_ref + y_ref * y_ref;
    float r_ref = std::sqrt(r_ref_sq);
    float K = length + fin_length;
    float A = r_ref_sq - K*K + length * length;
    float g = (r_ref_sq + K*K - length * length) / (2 * K * r_ref);
    float B = std::sqrt(1 - g*g);

    float theta1_acc = ((2 * x_ref * y_ref) / (r_ref_sq * r_ref_sq) - ((A + 2 * x_ref * x_ref) * r_ref_sq * r_ref * B - x_ref * A * (3*x_ref*r_ref*B - (g * x_ref * A)/(2 * K * B)))/(2 * K * r_ref_sq * r_ref_sq * r_ref_sq * B * B)) * vx_ref * vx_ref + (-y_ref / r_ref_sq - x_ref / (2 * K * r_ref_sq * r_ref * B)) * ax_ref;
    return theta1_acc;
}

float motor2_line_trajectory(float x_ref, float y_ref, float vx_ref, float vy_ref, float ax_ref, float ay_ref){
    float r_ref_sq = x_ref * x_ref + y_ref * y_ref;
    float r_ref = std::sqrt(r_ref_sq);
    float K = length + fin_length;

    float A2 = r_ref_sq + K*K - length * length;
    float g2 = (r_ref_sq + length * length - K * K) / (2 * length * r_ref);
    float B2 = std::sqrt(1 - g2 * g2);

    float theta2_acc = (2 * x_ref * y_ref) / (r_ref_sq * r_ref_sq) - ((A2 + 2 * x_ref * x_ref) * r_ref_sq * r_ref * B2 - x_ref * A2 * (3*x_ref*r_ref*B2 + (r_ref_sq * r_ref * B2))/2 * length * r_ref_sq * r_ref_sq * r_ref_sq * B2 * B2) * vx_ref * vx_ref + (-y_ref / r_ref_sq + (x_ref * A2)/(2 * length * r_ref_sq * r_ref * B2)) * ax_ref;
    return theta2_acc;
}
// 現在位置計算
void calc_pos(float theta1, float theta2, float& x_cur, float& y_cur){
    x_cur = length * std::cos(theta2) + (length + fin_length) * std::cos(theta1);
    y_cur = length * std::sin(theta2) + (length + fin_length) * std::sin(theta1);   
}

Trajectory g_traj(
    8.0f,
    20.0f,
    20.0f,
    0.30f,
    {-0.050f, 0.120f},
    {0.050f, 0.120f},
    1e-2f
);

float g_traj_time = 0.0f;
const float TRAJ_DT = 0.001f;

Vec2 g_start_pos = {-0.05, 0.12};
Vec2 g_end_pos = {0.05, 0.12};
bool g_forward = true;
float pre_theta1_vel = 0.0f;
float pre_theta2_vel = 0.0f;

void init(){
    // motor pin initialization
    gpio_init(MOTOR_DIR_PIN1);
    gpio_set_dir(MOTOR_DIR_PIN1, GPIO_OUT); 
    gpio_put(MOTOR_DIR_PIN1, 0); // Initial direction
    gpio_init(MOTOR_DIR_PIN2);
    gpio_set_dir(MOTOR_DIR_PIN2, GPIO_OUT);
    gpio_put(MOTOR_DIR_PIN2, 0); // Initial direction
    gpio_init(MOTOR_PWM_PIN1);
    gpio_set_dir(MOTOR_PWM_PIN1, GPIO_OUT);
    gpio_put(MOTOR_PWM_PIN1, 0); // Initial PWM low
    gpio_init(MOTOR_PWM_PIN2);
    gpio_set_dir(MOTOR_PWM_PIN2, GPIO_OUT);
    gpio_put(MOTOR_PWM_PIN2, 0); // Initial PWM low
    sleep_ms(500);

    gpio_init(ENCODER_SCL_PIN1);
    gpio_init(ENCODER_SDA_PIN1);
    gpio_init(ENCODER_SCL_PIN2);
    gpio_init(ENCODER_SDA_PIN2);
    sleep_ms(1000);

    motor1.attach(MOTOR_PWM_PIN1, MOTOR_DIR_PIN1);
    motor2.attach(MOTOR_PWM_PIN2, MOTOR_DIR_PIN2);
    sleep_ms(1000);

    motor1.begin(true, 20000);
    motor2.begin(true, 20000);
    sleep_ms(1000);

    enc1.begin(ENCODER_SDA_PIN1, ENCODER_SCL_PIN1, 400000, omega_n);
    enc2.begin(ENCODER_SDA_PIN2, ENCODER_SCL_PIN2, 400000, omega_n);

    bool enc_test1 = enc1.begin(ENCODER_SDA_PIN1, ENCODER_SCL_PIN1, 400000);

    if(!enc_test1){
        printf("Encoder 1 init failed!\n");
    }
    else{
        printf("Encoder 1 init succeeded.\n");
    }
    bool enc_test2 = enc2.begin(ENCODER_SDA_PIN2, ENCODER_SCL_PIN2, 400000);
    if(!enc_test2){
        printf("Encoder 2 init failed!\n");
    }
    else{
        printf("Encoder 2 init succeeded.\n");
    }
    sleep_ms(1000);

    // motor1.stop();
    // motor2.stop();
}

void core1_entry(){
    // sin波pwm param
    // constexpr float pwm_amp = 0.95f;
    // constexpr float pwm_freq = 5.0f;
    // constexpr float two_pi = 6.28318530717958647692f;
    // float t = 0.0f;
    float dt = 0.001f;
    uint64_t prev_us = time_us_64();
    while(true){
        uint64_t now_us = time_us_64();
        uint64_t loop_dt_us = now_us - prev_us;
        prev_us = now_us;
        absolute_time_t next_time = make_timeout_time_ms(dt * 1000);  // 今から10ms後
        // float u = pwm_amp * sinf(two_pi * pwm_freq * t);
        // motor1.setSpeed(-u); // Forward at 50% speed
        // motor2.setSpeed(u);
        uint16_t a1 = 0, a2 = 0;
        float theta1 = THETA_OFFSET1 - enc1.readAngle(a1);
        float theta2 = THETA_OFFSET2 - enc2.readAngle(a2);
        float omega1;
        float omega2;
        enc1.updateAngularVelocity(dt, theta1, omega1);
        enc2.updateAngularVelocity(dt, theta2, omega2);

        float theta1_acc = (omega1 - pre_theta1_vel)/dt;
        float theta2_acc = (omega2 - pre_theta2_vel)/dt;

        pre_theta1_vel = omega1;
        pre_theta2_vel = omega2;

        float x_cur, y_cur;
        calc_pos(theta1, theta2, x_cur, y_cur);
        float x_ref, y_ref, vx_ref, vy_ref, ax_ref, ay_ref;
        if(g_ref.valid){
            x_ref  = g_ref.x;
            y_ref  = g_ref.y;
            vx_ref = g_ref.vx;
            vy_ref = g_ref.vy;
            ax_ref = g_ref.ax;
            ay_ref = g_ref.ay;
        }
        else{
            x_ref = x_cur;
            y_ref = y_cur;
            vx_ref = vy_ref = ax_ref = ay_ref = 0.0f;
        }

        float theta1_acc_ref = motor1_line_trajectory(x_ref, y_ref, vx_ref, vy_ref, ax_ref, ay_ref);
        float theta2_acc_ref = motor2_line_trajectory(x_ref, y_ref, vx_ref, vy_ref, ax_ref, ay_ref);

        float u1 = pid_omega1.update(theta1_acc_ref, theta1_acc);
        float u2 = pid_omega2.update(theta2_acc_ref, theta2_acc);

        if(u1 > 0.95){
            u1 = 0.95;
        }
        else if(u1 < -0.95){
            u1 = -0.95;
        }

        if(u2 > 0.95){
            u2 = 0.95;
        }

        else if(u2 < -0.95){
            u2 = -0.95;
        }

        motor1.setSpeed(u1);
        motor2.setSpeed(u2);
        
        static int cnt = 0;
        if (++cnt >= 50) { // 0.1秒ごと
            printf("u1 =%.5f, u2 = %.5f,  x_ref=%.3f, y_ref=%.3f | x_cur=%.3f, y_cur=%.3f\n",
                u1, u2, x_ref, y_ref, x_cur, y_cur);
            cnt = 0;
        }
        busy_wait_until(next_time);
    }
}

int main(){
    init();
    stdio_init_all();
    cyw43_arch_init();
    sleep_ms(1000);

    multicore_launch_core1(core1_entry);

    while(true){
        absolute_time_t next_time = make_timeout_time_ms(TRAJ_DT * 1000.0f);
        static bool led_on = false;
        led_on = !led_on;
        cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, led_on);
        float total_time = g_traj.get_total_time();
        if(g_traj_time >= total_time){
            g_forward != g_forward;
            if(g_forward){
                g_traj.setPoints(g_start_pos, g_end_pos);
            }
            else{
                g_traj.setPoints(g_end_pos, g_start_pos);
            }
            g_traj.calculate_s_curve_trajectory_params();
            g_traj_time = 0.0f;
        }
        Vec2 target_pos, target_vel, target_acc;
        g_traj.get_s_curve_state(g_traj_time, target_pos, target_vel, target_acc);
        g_ref.x = target_pos.x;
        g_ref.y = target_pos.y;
        g_ref.vx = target_vel.x;
        g_ref.vy = target_acc.x;
        g_ref.ax = target_acc.y;
        g_ref.valid = true;
        busy_wait_until(next_time);
        g_traj_time += TRAJ_DT;
    }
    
}