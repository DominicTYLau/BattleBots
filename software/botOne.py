import RPi.GPIO as GPIO
from time import sleep
from lib_nrf24 import NRF24
import spidev
import string

# NRF24 Setup
pipes = [b"00001"]
radio = NRF24()
radio.begin(0, 0)  # CE on GPIO 22, CSN on GPIO 8 (CE0)
radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_LOW)
radio.openReadingPipe(1, pipes[0])
radio.startListening()

# GPIO Setup
GPIO.setmode(GPIO.BCM)

# Motor control pins
motor1_in1 = 17
motor1_in2 = 18
motor1_en = 16

motor2_in1 = 25
motor2_in2 = 26
motor2_en = 27

# Weapon ESC on GPIO 4
weapon_pwm_pin = 4

# Setup output pins
GPIO.setup([motor1_in1, motor1_in2, motor1_en,
            motor2_in1, motor2_in2, motor2_en,
            weapon_pwm_pin], GPIO.OUT)

# Setup PWM
motor1_pwm = GPIO.PWM(motor1_en, 100)
motor2_pwm = GPIO.PWM(motor2_en, 100)
weapon_pwm = GPIO.PWM(weapon_pwm_pin, 50)  # 50 Hz typical for ESCs

motor1_pwm.start(0)
motor2_pwm.start(0)
weapon_pwm.start(0)

def set_motor(pin1, pin2, pwm, direction, speed):
    if direction == 'F':
        GPIO.output(pin1, GPIO.HIGH)
        GPIO.output(pin2, GPIO.LOW)
    elif direction == 'R':
        GPIO.output(pin1, GPIO.LOW)
        GPIO.output(pin2, GPIO.HIGH)
    pwm.ChangeDutyCycle(speed)

def set_weapon_pwm(speed):
    # Convert speed (0–100%) to duty cycle for ESC (usually 5% to 10%)
    duty = (speed / 100.0) * 5 + 5
    weapon_pwm.ChangeDutyCycle(duty)

try:
    while True:
        if radio.available():
            received = []
            radio.read(received, radio.getDynamicPayloadSize())
            command = "".join([chr(n) for n in received if 32 <= n <= 126]).strip()
            print(f"Received: {command}")

            if command.startswith("M1"):
                direction = command[2]
                speed = int(command[3:])
                set_motor(motor1_in1, motor1_in2, motor1_pwm, direction, speed)

            elif command.startswith("M2"):
                direction = command[2]
                speed = int(command[3:])
                set_motor(motor2_in1, motor2_in2, motor2_pwm, direction, speed)

            elif command.startswith("M3F"):
                speed = int(command[3:])
                set_weapon_pwm(speed)

except KeyboardInterrupt:
    pass

finally:
    motor1_pwm.stop()
    motor2_pwm.stop()
    weapon_pwm.stop()
    GPIO.cleanup()