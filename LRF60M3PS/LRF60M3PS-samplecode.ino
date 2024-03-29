//NOTE: before uploading code, it may be required to disconnect Tx/Rx cables,
//then reconnecting those cables after a successful upload to the Arduino board
//Additionally, ensure the Tx/Rx into the laser rangefinder module are at 3.3V, 
//the Arduino Tx/Rx are typically at 5V, thus a logic converter may be needed.

unsigned char buf[16];
int index = 0;

//Intialize the various laser rangefinder commands
//Commands not used in the sample code are commented out
byte stopMeasurement[1] = {0x58}; 
//byte laserOff[9] = {0xAA, 0x00, 0x01, 0xBE, 0x00, 0x01, 0x00, 0x00, 0xC0};
byte laserOn[9] = {0xAA, 0x00, 0x01, 0xBE, 0x00, 0x01, 0x00, 0x01, 0xC1}; 
byte singleMeasurement[9] = {0xAA, 0x00, 0x00, 0x20, 0x00, 0x01, 0x00, 0x00, 0x21};
//byte continuousMeasurement[9] = {0xAA, 0x00, 0x00, 0x20, 0x00, 0x01, 0x00, 0x04, 0x25};

void setup(void) {
  //Serial.begin defaults to 8N1 with a timeout of 1000 milliseconds
  //Baud rate is 19200
  Serial.begin(19200);

  //Stop Measurement(Prevent the module from being in continuous measurement mode.) 
  Serial.write(stopMeasurement, sizeof(stopMeasurement));
    
  //Laser ON
  Serial.write(laserOn, sizeof(laserOn));
  delay(1000);
}

void loop(void) {
  //Clear the read buffer
  while(Serial.available() >0){
    Serial.read();
  }
  
  //Single Measurement
  Serial.write(singleMeasurement, sizeof(singleMeasurement));
  delay(1000);

  //When there is data available read the measurement byte by byte
  while(Serial.available()>0){
    buf[index] = Serial.read();
    index++;

    if (index == 13){ //Measurement reading's length is 13 bytes
      
      Serial.print("Data: ");
      for(int i =0;i<index;i++){
        Serial.print(buf[i], HEX);
      }
      
      //Convert hexadecimal bytes to decimal integers
      int distance = uint8_t(buf[6])*256*256*256+uint8_t(buf[7])*256*256+uint8_t(buf[8])*256+uint8_t(buf[9]);
      Serial.println(",  Distance: "+ (String)distance + "mm");

      //Reset counter
      index=0;
    }
  }
}
