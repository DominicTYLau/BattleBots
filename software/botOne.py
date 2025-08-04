#!/usr/bin/env python3

import RPi.GPIO as GPIO
from http.server import BaseHTTPRequestHandler, HTTPServer
from gpiozero import Servo
import json
import time

# --- Configuration ---
host_name = "IP_ADDRESS"  # Replace with your Raspberry Pi's IP address
host_port = 8000
esc_pin = 21  # ESC pin

# Motor pin definitions
MOTOR1_IN1 = 25
MOTOR1_IN2 = 26
MOTOR1_EN = 27

MOTOR2_IN3 = 17
MOTOR2_IN4 = 18
MOTOR2_EN = 16

# --- GPIO Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(MOTOR1_IN1, GPIO.OUT)
GPIO.setup(MOTOR1_IN2, GPIO.OUT)
GPIO.setup(MOTOR1_EN, GPIO.OUT)

GPIO.setup(MOTOR2_IN3, GPIO.OUT)
GPIO.setup(MOTOR2_IN4, GPIO.OUT)
GPIO.setup(MOTOR2_EN, GPIO.OUT)

# --- PWM Setup ---
motor1_pwm = GPIO.PWM(MOTOR1_EN, 1000)
motor2_pwm = GPIO.PWM(MOTOR2_EN, 1000)

motor1_pwm.start(0)
motor2_pwm.start(0)

# --- ESC Setup using gpiozero ---
ESC_MIN_PULSE = 0.000
ESC_MAX_PULSE = 1.5 / 1000 
esc_servo = Servo(esc_pin, min_pulse_width=ESC_MIN_PULSE, max_pulse_width=ESC_MAX_PULSE)

# --- Motor Control ---
def set_motor(left_speed, right_speed):
    left_speed = max(-100, min(left_speed, 100))
    right_speed = max(-100, min(right_speed, 100))

    # Left motor
    GPIO.output(MOTOR1_IN1, left_speed > 0)
    GPIO.output(MOTOR1_IN2, left_speed < 0)

    # Right motor
    GPIO.output(MOTOR2_IN3, right_speed > 0)
    GPIO.output(MOTOR2_IN4, right_speed < 0)

    motor1_pwm.ChangeDutyCycle(abs(left_speed))
    motor2_pwm.ChangeDutyCycle(abs(right_speed))

    print(f"Set motors → Left: {left_speed}%, Right: {right_speed}%")


def set_esc(active):
    """Spin ESC motor if active=1, else stop."""
    if active:
        esc_servo.value = 1 
        print("ESC: Spinning")
    else:
        esc_servo.value = -1
        print("ESC: Stopped")


# --- HTTP Server ---
class MyServer(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        html = '''
       <html>
<head>
    <title>Smart Motor Controller</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin-top: 50px;
            background-color: #f9f9f9;
        }
        h1 {
            color: #333;
        }
        #status {
            font-size: 20px;
            margin-top: 20px;
            color: #444;
        }
        .instructions {
            margin-top: 30px;
            color: #666;
        }
    </style>
</head>
<body>
    <h1>Use Arrow Keys to Drive</h1>
    <div id="status">Waiting for input...</div>
    <div class="instructions">
        Use arrow keys to drive. Hold <b>Space</b> to spin the ESC motor.
    </div>

    <script>
        let keys = {
            ArrowUp: false,
            ArrowDown: false,
            ArrowLeft: false,
            ArrowRight: false,
            Space: false
        };

        let speed = 70;
        let timeout = null;

        function sendCommand() {
            let forward = keys.ArrowUp ? 1 : keys.ArrowDown ? -1 : 0;
            let turn = keys.ArrowRight ? -1 : keys.ArrowLeft ? 1 : 0;
            let esc = keys.Space ? 1 : 0;

            let left = speed * (forward - turn);
            let right = speed * (forward + turn);

            left = Math.max(-100, Math.min(100, left));
            right = Math.max(-100, Math.min(100, right));

            fetch("/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ left: left, right: right, esc: esc })
            });

            if (forward === 0 && turn === 0 && !esc) {
                document.getElementById("status").innerText = "Motors stopped.";
            } else {
                document.getElementById("status").innerText = 
                    `Left: ${Math.round(left)}%, Right: ${Math.round(right)}%, ESC: ${esc ? "ON" : "OFF"}`;
            }
        }

        function updateLoop() {
            sendCommand();
            timeout = setTimeout(updateLoop, 100);
        }

        document.addEventListener("keydown", function(e) {
            if (e.key === " ") {
                e.preventDefault(); // Prevent page scroll
                keys.Space = true;
                if (!timeout) updateLoop();
                return;
            }

            if (e.key in keys && !keys[e.key]) {
                keys[e.key] = true;
                if (!timeout) updateLoop();
            }
        });

        document.addEventListener("keyup", function(e) {
            if (e.key === " ") {
                keys.Space = false;
            }

            if (e.key in keys) {
                keys[e.key] = false;

                if (!Object.values(keys).some(v => v)) {
                    sendCommand();
                    clearTimeout(timeout);
                    timeout = null;
                }
            }
        });
    </script>
</body>
</html>
        '''
        self.do_HEAD()
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)

        left = int(data.get("left", 0))
        right = int(data.get("right", 0))
        esc = int(data.get("esc", 0))

        set_motor(left, right)
        set_esc(esc)

        self.send_response(200)
        self.end_headers()


# --- Main Program ---
if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print(f"Server Starts - {host_name}:{host_port}")

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
        set_motor(0, 0)
        set_esc(0)
        motor1_pwm.stop()
        motor2_pwm.stop()
        esc_servo.detach()
        GPIO.cleanup()
        http_server.server_close()
