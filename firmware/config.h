#ifndef CONFIG_H
#define CONFIG_H

// Pin Definitions
const int trigPin = 7;
const int echoPin = 6;
const int servoPin = 9;

// Sweep Parameters
const int angleStart = 0;
const int angleEnd = 180;
const int angleStep = 2;      // adjust resolution (larger step = fewer points)
const int settleMs = 200;     // servo settle time (ms)
const int samplesPerAngle = 3;
const unsigned long echoTimeout = 30000UL; // microseconds (~5m)

// Communication
const long SERIAL_BAUD = 115200;

#endif
