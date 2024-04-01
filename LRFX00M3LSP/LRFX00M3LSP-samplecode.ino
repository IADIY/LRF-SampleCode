//NOTE: before uploading code, it may be required to disconnect Tx/Rx cables,
//then reconnecting those cables after a successful upload to the Arduino board
//Additionally, ensure the Tx/Rx into the laser rangefinder module are at 3.3V, 
//the Arduino Tx/Rx are typically at 5V, thus a logic converter may be needed.

//Intialize the various laser rangefinder commands
//Commands not used in the sample code are commented out
byte stopMeasurement[8] = {0xAE, 0xA7, 0x04, 0x00, 0x0F, 0x13, 0xBC, 0xBE};  //Stop Measure
//byte laserOff[9] = {0xAE, 0xA7, 0x05, 0x00, 0x40, 0x00, 0x45, 0xBC, 0xBE};  //Laser OFF
byte laserOn[9] = {0xAE, 0xA7, 0x05, 0x00, 0x40, 0x01, 0x46, 0xBC, 0xBE};  //Laser ON
//byte singleMeasurement[8] = {0xAE, 0xA7, 0x04, 0x00, 0x05, 0x09, 0xBC, 0xBE};  //Single Measure
byte continuousMeasurement[8] = {0xAE, 0xA7, 0x04, 0x00, 0x0E, 0x12, 0xBC, 0xBE};  //Continus Measure

unsigned char buf[50]; 
int index = 0; 

void setup() {
  //Serial.begin defaults to 8N1 with a timeout of 1000 milliseconds
  //Baud rate is 9600
  Serial.begin(9600);

  //Laser ON
  Serial.write(laserOn, sizeof(laserOn));
  delay(500);
  
  //Continuous Measurement
  Serial.write(continuousMeasurement, sizeof(continuousMeasurement));
  delay(500);
}

void loop() {
  //Every iteration read a byte if available
  if (Serial.available() > 0){
    buf[index] = Serial.read();
    index++;

    //Check to see if previous byte was an end marker
    if (buf[index-1] == 190){  
      for(int i=0;i<index;i++)
      {
        Serial.print(buf[i]& 0xFF, HEX);
      } 
        Serial.println("");
      if(uint8_t(buf[4])==133)  //133=0x85 as Measurement Result Command code
      {
        float distance = float(uint8_t(buf[7])*256+uint8_t(buf[8]))/10;
        Serial.print(distance);
        Serial.println("m");
      }
      //Reset the index
      index=0;
    }
  }
}
