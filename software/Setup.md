## Prerequisites

- Raspberry Pi (with GPIO support)
- Motors + ESC connected to correct GPIO pins
- Python 3 installed
- Access to the same Wi-Fi network as your control device

## Wiring

Update the GPIO pin numbers in the script if your wiring differs.

## Setup Instructions

### 1. Connect to Raspberry Pi

### 2. Clone this repository (or copy the script)

Go to the repository

### 3. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install gpiozero
```

Note: RPi.GPIO is preinstalled on most Raspberry Pi systems.

### 5. Set your Raspberry Pi’s IP address in the script

```bash
host_name = "IP_ADDRESS"
```
to your Pi’s actual local IP (e.g., "192.168.1.42")

### 6. Run the server

python3 botOne.py

If successful, you should see:

Server Starts - IP_ADDRESS

### 7. Open the controller

On a device connected to the same Wi-Fi network, open a browser and go to:

http://<raspberry-pi-ip>:8000

Controls
	•	↑ / ↓ — Forward / Backward
	•	← / → — Move left / right
	•	Spacebar — Toggle ESC-powered motor (weapon)
