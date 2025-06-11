#include <Servo.h>
Servo myServo;

void setup() {
  myServo.attach(6);
  Serial.begin(115200);
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == 'R') {
      myServo.write(0);  // Rotate to 90°
      delay(500);         // Hold position
      myServo.write(90);   // Return to rest
    }
  }
}
