#include "config.h"
#include <Servo.h>

Servo myServo;
unsigned long sweep_id = 0;

void setup() {
  Serial.begin(115200);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  myServo.attach(servoPin);
  delay(500);
}

float measureDistanceCM() {
  // do 'samplesPerAngle' quick samples and average (ignore 0 results)
  long total = 0;
  int valid = 0;
  for (int i = 0; i < samplesPerAngle; ++i) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    unsigned long duration = pulseIn(echoPin, HIGH, echoTimeout);
    if (duration > 0) {
      float cm = duration / 58.0; // HC-SR04: microseconds/58 = cm approx
      total += (long)(cm * 1000); // accumulate in thousandths to keep precision
      valid++;
    }
    delay(30);
  }
  if (valid == 0) return -1.0; // no echo
  return (total / (float)valid) / 1000.0;
}

void loop() {
  sweep_id++;
  // sweep from start to end
  for (int a = angleStart; a <= angleEnd; a += angleStep) {
    myServo.write(a);
    delay(settleMs);
    float d = measureDistanceCM(); // -1.0 if no reading
    unsigned long ts = millis();
    // print a single-line JSON (no large buffers)
    Serial.print("{\"sweep_id\":");
    Serial.print(sweep_id);
    Serial.print(",\"angle\":");
    Serial.print(a);
    Serial.print(",\"distance_cm\":");
    if (d < 0) Serial.print("null");
    else Serial.print(d, 2);
    Serial.print(",\"ts\":");
    Serial.print(ts);
    Serial.println("}");
    // small inter-angle pause (optional)
    delay(25);
  }
  // optional pause between sweeps
  delay(250);
}
