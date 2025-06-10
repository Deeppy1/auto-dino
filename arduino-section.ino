#include <Servo.h>

Servo myServo;
const int servoPin = 9;
const int defaultPos = 0;
const int jumpPos = 90;

void setup() {
  Serial.begin(9600);      // Start serial communication
  myServo.attach(servoPin); // Attach the servo to pin 6
  myServo.write(defaultPos); // Move to default position
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n'); // Read input until newline
    input.trim(); // Remove any whitespace

    if (input.equalsIgnoreCase("jump")) {
      myServo.write(jumpPos);   // Move to 90 degrees
      delay(500);              // Hold position for a second (adjust if needed)
      myServo.write(defaultPos); // Return to original position
    }
  }
}
