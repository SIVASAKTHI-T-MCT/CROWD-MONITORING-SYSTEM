# Wiring Details

The "Crowd Monitoring System" uses a standard HC-SR04 ultrasonic sensor and an SG90 servo motor.

## Connection Table

| Component | Pin (Project) | Microcontroller Pin | Notes |
|-----------|---------------|-------------------|-------|
| HC-SR04 VCC | 5V | 5V | |
| HC-SR04 GND | GND | GND | |
| HC-SR04 Trig | 7 | D7 | Configurable in `config.h` |
| HC-SR04 Echo | 6 | D6 | Configurable in `config.h` |
| Servo VCC | 5V | 5V | Use external power if possible |
| Servo GND | GND | GND | |
| Servo PWM | 9 | D9 | Configurable in `config.h` |

## Notes on Power
The SG90 servo and HC-SR04 can be powered directly from the Arduino 5V pin for testing, but for stable operation, an external 5V power supply is recommended (connecting the GNDs).
