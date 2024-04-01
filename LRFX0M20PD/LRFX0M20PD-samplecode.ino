//NOTE: before uploading code, it may be required to disconnect Tx/Rx cables,
//then reconnecting those cables after a successful upload to the Arduino board
//Additionally, ensure the Tx/Rx into the laser rangefinder module are at 3.3V, 
//the Arduino Tx/Rx are typically at 5V, thus a logic converter may be needed.

//Intialize the various laser rangefinder commands
//Commands not used in the sample code are commented out
byte stopMeasurement[4] = {0x80, 0x04, 0x02, 0x7A}; 
//byte laserOff[5] = {0x80, 0x06, 0x05, 0x00, 0x75};
byte laserOn[5] = {0x80, 0x06, 0x05, 0x01, 0x74};
byte singleMeasurement[4] = {0x80, 0x06, 0x02, 0x78};
//byte continuousMeasurement[4] = {0x80, 0x06, 0x03, 0x77};

void setup(void) {
  //Serial.begin defaults to 8N1 with a timeout of 1000 milliseconds
  //Baud rate is 9600
  Serial.begin(9600);

  //Stop Measurement(Prevent the module from being in continuous measurement mode.) 
  Serial.write(stopMeasurement, sizeof(stopMeasurement));
    
  //Laser ON
  Serial.write(laserOn, sizeof(laserOn));
  delay(1000);
}

void loop(void) { 
  //Single Measurement
  Serial.write(singleMeasurement, sizeof(singleMeasurement));
  delay(1000);
  

  //Read the Data
  String data = Serial.readString();
  distanceInterpreter(data);
}

void distanceInterpreter(String data){
  //Distance is stored in data[3:10/11] as ASCII representation of numbers including a period in the middle
  float distance = 0;
  //The number of decimal points changes based on how many 
  int numDecimalPoints= 3;

  //Under the resolution setting of 1mm
  if (data.length() == 11){ 
    distance = data.substring(3,10).toFloat();
  }

  //Under the resolution setting of 0.1mm 
  else if(data.length() == 12){
    distance = data.substring(3,11).toFloat();
    //Change number of decimal points displayed for the higher resolution
    numDecimalPoints = 4;
  }

  //Display Data and Distance to Serial Monitor
  Serial.print("Data:" + data + "  Distance:");
  //If the number of decimal points is not specified, it will default to 2
  Serial.print(distance, numDecimalPoints);
  Serial.println("m");
  return;
}