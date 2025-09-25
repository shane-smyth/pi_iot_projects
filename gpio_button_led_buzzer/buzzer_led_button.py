import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
LED_PIN = 18
BUTTON_PIN = 27
BUZZER_PIN = 17

# setting up pins
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        button_state = GPIO.input(BUTTON_PIN)

        if not button_state:
            GPIO.output(LED_PIN, GPIO.HIGH)
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
    
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
            GPIO.output(BUZZER_PIN, GPIO.LOW)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nProgram Stopped by User")

finally:
    #buzzer_pwm.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")
