/* lights.ino
 * Control the lights on simple Lux
 * 
 * Andrew Chan
 */

// define pins
#define HEAD_TAIL_LIGHTS 5  // corresponds to PIN D2
#define TURN_LIGHTS 11      // corresponds to PIN D8
#define LED_PIN 13          // onboard LED

// define mode
#define DEBUG true

void setup() {
  // put your setup code here, to run once:
  pinMode(HEAD_TAIL_LIGHTS, OUTPUT);
  pinMode(TURN_LIGHTS, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int timeToDelay = 250;
  digitalWrite(HEAD_TAIL_LIGHTS, HIGH);
  
  digitalWrite(TURN_LIGHTS, HIGH);
  if (DEBUG) {
    digitalWrite(LED_PIN, HIGH);
  }
  delay(timeToDelay);
  digitalWrite(TURN_LIGHTS, LOW);
  if (DEBUG) {
    digitalWrite(LED_PIN, LOW);
  }
  delay(timeToDelay);
}
