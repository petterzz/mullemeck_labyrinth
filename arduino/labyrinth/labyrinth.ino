#include <Servo.h> 
#include <SevSeg.h>
 
Servo servoX;
Servo servoY;
SevSeg sevseg;

float controlSignalX = 0, controlSignalY = 0;    
int servoSignalX = 90, servoSignalY = 90;   // should these be floats for better precision? can Serial write floats?
int calibrate_x=0, calibrate_y=0;
unsigned int cycleCounter = 0;

// invert mechanical direction
const int mechanicalDirX = -1;
const int mechanicalDirY = -1;

void setup() { 
  // 7-segment display
  pinMode(A2, OUTPUT);
  pinMode(A3, OUTPUT);
  pinMode(A4, OUTPUT);
  pinMode(A5, OUTPUT);
  byte numDigits = 4; 
  byte digitPins[] = {13, 12, 8, 7}; // {pin: 12, 9, 8, 6}
  byte segmentPins[] = {2, 3, A2, A4, A5, 4, 5, A3}; // {pin: 11, 7, 4, 2, 1, 10, 5, 3}
  sevseg.begin(COMMON_CATHODE, numDigits, digitPins, segmentPins); 
  sevseg.setBrightness(40);

  // Servos
  pinMode(11, OUTPUT);
  servoX.attach(11);
  //servoY.attach();
  
  calibrate_x = 0;
  calibrate_y = 0;

  // Serial
  Serial.begin(115200);
} 


 
void loop() { 
  
  if(Serial.available()) {
    if(Serial.peek() == 'x') {
      controlSignalX = Serial.parseFloat();
      servoSignalX = map(int(controlSignalX)*mechanicalDirX, -90, 90, 0, 180) + calibrate_x;
    }
    if(Serial.peek() == 'y') {
      controlSignalY = Serial.parseFloat();
      servoSignalY = map(int(controlSignalY)*mechanicalDirY, -90, 90, 0, 180) + calibrate_y;
    }
    if(Serial.read() == 'c') {
      if(Serial.peek() == 'x') {
        int cal = Serial.parseInt();
        calibrate_x += cal;
      }
      if(Serial.peek() == 'y') {
        int cal = Serial.parseInt();
        calibrate_y += cal;
      }
    }

    // empty serial buffer
    while(Serial.available()){
      Serial.read();
    }
    
    // write to servo only if within mechanical limits    
    if(servoSignalX > 30 && servoSignalX < 150){
      servoX.write(servoSignalX);
    }
    if(servoSignalY > 30 && servoSignalY < 150){
      servoY.write(servoSignalY);
    }
  }

  sevseg.setNumber(servoSignalX, 6);
  cycleCounter++;
  sevseg.refreshDisplay();  
  
  delay(5); 
   
} 
