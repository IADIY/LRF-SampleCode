//NOTE: before uploading code, it may be required to disconnect Tx/Rx cables,
//then reconnecting those cables after a successful upload to the Arduino board
//Additionally, ensure the Tx/Rx into the laser rangefinder module are at 3.3V, 
//the Arduino Tx/Rx are typically at 5V, thus a logic converter may be needed.
#include <Arduino.h>

//Intialize the various laser rangefinder commands
//Commands not used in the sample code are commented out
char stopMeasurement[] = "~010600000001480A\r\n";
//char laserOff[] = "~01060030000089C5\r\n";
char laserOn[] = "~0106003000014805\r\n"; 
//char singleMeasurement[] = "~01030100000185F6\r\n";
char continuousMeasurement[] = "~01060000000089CA\r\n";


//intialize hexadecimal converter function
int distanceInterpreter(String data);

void setup(void) {
  //Serial.begin defaults to 8N1 with a timeout of 1000 milliseconds
  //Baud rate is 115200
  Serial.begin(115200);

  //Stop Measurement(Prevent the module from being in continuous measurement mode.)
  Serial.write(stopMeasurement);

  //Laser ON
  Serial.write(laserOn);

  //Continuous Measurement
  Serial.write(continuousMeasurement);
  delay(1000);
}

void loop(void) {
  
  //Read the Data
  String data = Serial.readStringUntil('\n');
  if(data.length()>=18) {
    Serial.println("Data:" + data + ",  Distance:" + (String)distanceInterpreter(data) + "mm");
  }
  //Too long of a delay will likely cause accuracy issues. If a longer delay is needed,
  //please look at the millis sample code
  delay(10);
}

int distanceInterpreter(String data){
  //Distance is stored in data[9:12] as hexidecimal, thus need to convert that portion into decimal
  int distance = 0;
  //Use the Conditional or Ternary Operator (?:) to determine the digit's hexadecimal value in decimal
  //That decimal value is then scaled according to the each digits corresponding value *16^(x) and then all added together
  distance+=(data[9]  <= '9' ? data[9]  - '0' : data[9]  +  - '0' - 7)*4096;
  distance+=(data[10] <= '9' ? data[10] - '0' : data[10] +  - '0' - 7)*256;
  distance+=(data[11] <= '9' ? data[11] - '0' : data[11] +  - '0' - 7)*16;
  distance+=(data[12] <= '9' ? data[12] - '0' : data[12] +  - '0' - 7);
  return distance;
}