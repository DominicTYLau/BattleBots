#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

// NRF24L01 Setup
RF24 radio(9, 10); // CE, CSN
const byte address[6] = "00001";

// Joystick Pins
const int joyLeftY = A0;  // Controls motor 1
const int joyRightY = A1; // Controls motor 2

// Button Pins
const int button1 = 2;     // Weapon forward
const int button2 = 3;     // Weapon reverse

void setup() {
  Serial.begin(9600);
  pinMode(button1, INPUT_PULLUP);
  pinMode(button2, INPUT_PULLUP);

  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_LOW);
  radio.setDataRate(RF24_1MBPS);
  radio.stopListening();
}

void loop() {
  String command = "";

  // === Motor 1 ===
  int m1Y = analogRead(joyLeftY);
  if (m1Y > 570) {
    int speed = map(m1Y, 570, 1023, 0, 100);
    command = "M1F" + String(speed);
  } else if (m1Y < 450) {
    int speed = map(m1Y, 450, 0, 0, 100);
    command = "M1R" + String(speed);
  }

  if (command != "") {
    sendCommand(command);
    delay(30);
  }

  // === Motor 2 ===
  command = "";
  int m2Y = analogRead(joyRightY);
  if (m2Y > 570) {
    int speed = map(m2Y, 570, 1023, 0, 100);
    command = "M2F" + String(speed);
  } else if (m2Y < 450) {
    int speed = map(m2Y, 450, 0, 0, 100);
    command = "M2R" + String(speed);
  }

  if (command != "") {
    sendCommand(command);
    delay(30);
  }

  // === Weapon Control Buttons ===
  if (digitalRead(button1) == LOW) {
    sendCommand("M3F100");  // Spin weapon (Can only go One Direction)
    delay(30);
  }
}

void sendCommand(String cmd) {
  char message[32];
  cmd.toCharArray(message, 32);
  radio.write(&message, sizeof(message));
  Serial.println("Sent: " + cmd);
}