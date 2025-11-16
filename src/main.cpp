#include "config.hpp"

DCMotor motor1;
DCMotor motor2;

AS5601 enc1(i2c0);
AS5601 enc2(i2c1);

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
    sleep_ms(10000);

    // motor1.stop();
    // motor2.stop();
}

void core1_entry(){
    // sin波pwm param
    constexpr float pwm_amp = 0.95f;
    constexpr float pwm_freq = 5.0f;
    constexpr float two_pi = 6.28318530717958647692f;
    float t = 0.0f;
    float dt = 0.001f;

    uint64_t prev_us = time_us_64();
    while(true){
        uint64_t now_us = time_us_64();
        uint64_t loop_dt_us = now_us - prev_us;
        prev_us = now_us;
        absolute_time_t next_time = make_timeout_time_ms(dt * 1000);  // 今から10ms後
        float u = pwm_amp * sinf(two_pi * pwm_freq * t);
        // motor1.setSpeed(-u); // Forward at 50% speed
        motor2.setSpeed(u);

        uint16_t a1 = 0, a2 = 0;
        float theta1 = THETA_OFFSET1 - enc1.readAngle(a1);
        float theta2 = THETA_OFFSET2 - enc2.readAngle(a2);
        float omega1;
        float omega2;
        enc1.updateAngularVelocity(dt, theta1, omega1);
        enc2.updateAngularVelocity(dt, theta2, omega2);

        static int cnt = 0;
        if(++cnt >= 100){
            printf("loop_dt = %llu us\n", (unsigned long long)loop_dt_us);
            cnt = 0;
            printf("t = %.3f, u = %.5f, Enc1: theta=%.3f rad, omega=%.3f rad/s | Enc2: theta=%.3f rad, omega=%.3f rad/s\n",
                t, u, 
                theta1, omega1,
                theta2, omega2
            );  
        }
              
        busy_wait_until(next_time);
        t += dt;
    }
}

int main(){
    init();
    stdio_init_all();
    cyw43_arch_init();
    sleep_ms(1000);

    multicore_launch_core1(core1_entry);

    while(true){
        absolute_time_t next_time = make_timeout_time_ms(100);
        static bool led_on = false;
        led_on = !led_on;
        cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, led_on);
        busy_wait_until(next_time); 
    }
}