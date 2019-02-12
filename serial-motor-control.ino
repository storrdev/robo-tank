#include <BidirectionalMotor.h>

const byte numBytes = 32;
byte receivedBytes[numBytes];
byte numReceived = 0;

boolean newData = false;

int leftSpeed = 0;
boolean leftDirection = true;
int rightSpeed = 0;
boolean rightDirection = true;

BidirectionalMotor leftMotor(11, 10, 9);
BidirectionalMotor rightMotor(6, 5, 3);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  // Hopefully this causes the weird bug with the extra characters in front of the
  // <Arduino is ready> println (this seems to have fixed it)
  while (Serial.available() > 0) {
    Serial.read();
  }
  
  Serial.println("<Arduino is ready>");
}

void loop() {
  checkAndParseSerialCommands();
  setVars();
}

void checkAndParseSerialCommands() {
  static boolean recvInProgress = false;
  static byte ndx = 0;
  byte startMarker = 0x3C;
  byte endMarker = 0x3E;
  byte rb;

  while (Serial.available() > 0 && newData == false) {
    rb = Serial.read();

    if (recvInProgress == true) {
      if (rb != endMarker) {
        receivedBytes[ndx] = rb;
        ndx++;
        if (ndx >= numBytes) {
          ndx = numBytes - 1;
        }
      }
      else {
        receivedBytes[ndx] = '\0';
        recvInProgress = false;
        numReceived = ndx;
        ndx = 0;
        newData = true;
      }
    }
    else if (rb == startMarker) {
      recvInProgress = true;
    }
  }
}

void setVars() {
  if (newData == true) {
    newData = false;
    
    leftSpeed      = (int) receivedBytes[0];
    leftDirection  = (bool) receivedBytes[1];
    rightSpeed     = (int) receivedBytes[2];
    rightDirection = (bool) receivedBytes[3];

//    Serial.println(leftSpeed);
//    Serial.println(direction);

    leftMotor.setMotor(leftSpeed, leftDirection);
    rightMotor.setMotor(rightSpeed, !rightDirection);
  
    leftMotor.drive();
    rightMotor.drive();
  } else {
    // Reset motors to doing nothing
//    leftMotor.setMotor(0, leftDirection);
//    rightMotor.setMotor(0, !rightDirection);
//  
//    leftMotor.drive();
//    rightMotor.drive();
  }
}

