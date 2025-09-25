//NOTE: before uploading code, it may be required to disconnect Tx/Rx cables,
//then reconnecting those cables after a successful upload to the Arduino board
//Additionally, ensure the Tx/Rx into the laser rangefinder module are at 3.3V, 
//the Arduino Tx/Rx are typically at 5V, thus a logic converter may be needed.

//Intialize the various laser rangefinder commands
//Commands not used in the sample code are commented out
byte stopMeasurement[8] = {0x55, 0xAA, 0x8E, 0xFF, 0xFF, 0xFF, 0xFF, 0x8A};  //Stop Measure
//byte singleMeasurement[8] = {0x55, 0xAA, 0x88, 0xFF, 0xFF, 0xFF, 0xFF, 0x84};  //Single Measure
byte continuousMeasurement[8] = {0x55, 0xAA, 0x89, 0xFF, 0xFF, 0xFF, 0xFF, 0x85};  //Continus Measure
//intialize data array for measurements
byte data[8];
float distance = 0;

void setup() {
  //Serial.begin defaults to 8N1 with a timeout of 1000 milliseconds
  //Baud rate is 115200 by default, but can be changed
  Serial.begin(115200);
    
  Serial.write(stopMeasurement, sizeof(stopMeasurement));
  delay(500);

  //Intial Start Time
  Serial.write(continuousMeasurement, sizeof(continuousMeasurement));
  delay(500);
}

void loop() {
  //Once a measurement has been taken, read it
  if(Serial.available() > 0){
    Serial.print("Data: ");
    //read all bytes into data
    for(int i=0;i<8;i++){
      data[i] = Serial.read();
      Serial.print(data[i]);
    }
    
    //Process Data
    Serial.println("");
    //Error
    if(data[4]==0){
      Serial.println("Measurement Failed");
    }
    else{
      distance = ((float)data[5]*256 + (float)data[6])/10;
      Serial.print("Distance: ");
      //Only print 1 decimal place
      Serial.print(distance, 1);
      Serial.println(" m");
    }

  }
}
