import RPi.GPIO as GPIO
import time
import smbus2

GPIO.setmode(GPIO.BCM)
LED_PIN = 18
BUTTON_PIN = 27
BUZZER_PIN = 17

# setting up pins
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# MPU6050 setup
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B

bus = smbus2.SMBus(1)
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0) # wake up sensor

# Reads the 16-bit signed value from sensor
def read_word(reg):
    high = bus.read_byte_data(MPU6050_ADDR, reg)
    low = bus.read_byte_data(MPU6050_ADDR, reg + 1)
    value = (high << 8) + low
    if value >= 0x8000:
        value =- ((65535 - value) + 1)
    return value


def get_accel():
    x = read_word(ACCEL_XOUT_H) / 16384.0
    y = read_word(ACCEL_XOUT_H + 2) / 16384.0
    z = read_word(ACCEL_XOUT_H + 4) / 16384.0
    return x, y, z


alarm_triggered = False
# g-unit (gravity) change based on sensitivity
MOVEMENT_THRESHOLD = 1.3


try:
    print("Monitoring movement... Press button to reset alarm (Ctrl+C to exit).")
    
    while True:
        button_state = GPIO.input(BUTTON_PIN)

        # If button is pressed reset alarm
        if not button_state:
            alarm_triggered = False
            GPIO.output(LED_PIN, GPIO.LOW)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            print("Reset by button")
            time.sleep(0.3)
    
        # If alarm is not active, keep monitoring
        if not alarm_triggered:
            ax, ay, az = get_accel()
            total_accel = (ax**2 + ay**2 + az**2) ** 0.5 # magnitude of acceleration

            # Noraml stationary value is around 1g
            deviation = abs(total_accel - 1.0)

            if deviation > MOVEMENT_THRESHOLD:
                alarm_triggered = True
                GPIO.output(LED_PIN, GPIO.HIGH)
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                print(f"Big movement detected! acceleration = {total_accel:.2f}g -> ALARM ON")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nProgram Stopped by User")

finally:
    #buzzer_pwm.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")
