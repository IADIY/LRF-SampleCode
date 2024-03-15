//NOTE: before uploading code, it may be required to disconnect Tx/Rx cables,
//then reconnecting those cables after a successful upload to the Arduino board
//Additionally, ensure the Tx/Rx into the laser rangefinder module are at 3.3V, 
//the Arduino Tx/Rx are typically at 5V, thus a logic converter may be needed.
#include <Arduino.h>

//Intialize the various laser rangefinder commands
//Commands not used in the sample code are commented out
//char confirmationComm[] = "$00023335&";
char laserOff[] = "$0003260029&";
char laserOn[] = "$0003260130&"; 
char singleMeasurement[] = "$00022123&";
//char continuousMeasurement[] = "$00022426&";

//intialize distance converter function
int distanceInterpreter(String data);

void setup(void) {
  //Serial.begin defaults to 8N1 with atimeout of 1000 milliseconds
  //Baud rate is 115200
  Serial.begin(115200);

  //#Laser OFF (Confirm LRF is in default off state)
  Serial.write(laserOff);

  //Laser ON
  Serial.write(laserOn);
  delay(1000);
}

void loop(void) {
  Serial.write(singleMeasurement);
  delay(1000);

  //Read the Data
  String data = Serial.readStringUntil('&');
  if(data == "$00023335") {
    //Do nothing, the act of reading the confirmation will clear it from the Serial buffer
    Serial.println("\nCommand Received");
  } else if(data.length()==17) {
    Serial.println("Data:" + data + ",  Distance:" + (String)distanceInterpreter(data) + "mm");
  } 
  
}

int distanceInterpreter(String data){
  //Distance is stored in data[7:15], thus need to extract that portion
  //For LRF20M3PS, distance is stored as a decimal representation
  int distance = 0;
  distance += data.substring(7,15).toInt();
  return distance;
}