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
    sleep_ms(1000);

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

    // motor1.stop();
    // motor2.stop();
}

void core1_entry(){
    while(true){
        absolute_time_t next_time = make_timeout_time_ms(100);  // 今から100ms後
        motor1.setSpeed(-0.6f); // Forward at 50% speed
        motor2.setSpeed(-0.6f);

        uint16_t a1 = 0, a2 = 0;
        bool r1 = enc1.readAngleCounts(a1);
        bool r2 = enc2.readAngleCounts(a2);
        if(r1){
            float deg1 = (a1 * 360.0f)/4096.0f;
            printf("[ENC1] %7.2f deg", deg1);
        }
        else{
            printf("[ENC1] read fail (r1=%d)\n", r1);
        }
        if(r2){
            float deg2 = (a2 * 360.0f)/4096.0f;
            printf("[ENC2] %7.2f deg", deg2);
        }
        else{
            printf("[ENC2] read fail (r2=%d)\n", r2);
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
        absolute_time_t next_time = make_timeout_time_ms(100);
        static bool led_on = false;
        led_on = !led_on;
        cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, led_on);
        busy_wait_until(next_time); 
    }
}