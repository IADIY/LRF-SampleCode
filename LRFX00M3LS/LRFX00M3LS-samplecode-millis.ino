unsigned char buf[50]; 
int index = 0; 
float distance = 0;

//Intialize the various laser rangefinder commands
//Commands not used in the sample code are commented out
byte stopMeasurement[8] = {0xAE, 0xA7, 0x04, 0x00, 0x0F, 0x13, 0xBC, 0xBE};  //Stop Measure
//byte laserOff[9] = {0xAE, 0xA7, 0x05, 0x00, 0x40, 0x00, 0x45, 0xBC, 0xBE};  //Laser OFF
byte laserOn[9] = {0xAE, 0xA7, 0x05, 0x00, 0x40, 0x01, 0x46, 0xBC, 0xBE};  //Laser ON
byte singleMeasurement[8] = {0xAE, 0xA7, 0x04, 0x00, 0x05, 0x09, 0xBC, 0xBE};  //Single Measure
//byte continuousMeasurement[8] = {0xAE, 0xA7, 0x04, 0x00, 0x0E, 0x12, 0xBC, 0xBE};  //Continus Measure


//Intialize Timer Variables
unsigned long startMillis;
unsigned long currentMillis;
//Duration needed to wait in milliseconds
const unsigned long period = 1500; //Currently set to 1.5 seconds

void setup() {
  //Serial.begin defaults to 8N1 with a timeout of 1000 milliseconds
  //Baud rate is 9600
  Serial.begin(9600);
    
  Serial.write(stopMeasurement, sizeof(stopMeasurement));
  delay(500);

  Serial.write(laserOn, sizeof(laserOn));
  delay(500);

  //Intial Start Time
  startMillis = millis();
}

void loop() {
  //Store Current Time
  currentMillis = millis();

  //Only once the period has elapsed should the measurement be printed
  //The duration of the period can be adjusted by changing the period variable above
  if(currentMillis - startMillis >= period){
    //Print Measurement result
    if(distance > 0){
      Serial.print(distance);
      Serial.println("m");
      //Reset the variable
      distance = 0;
    } else {
      Serial.println("Measurement Error. Object is too close or too far");
    }
    //small delay is necessasry, but too long of a delay will impact results
    delay(100);
    Serial.write(singleMeasurement, sizeof(singleMeasurement));
    

    startMillis = currentMillis;
  }

  //Data Processing
  if (Serial.available() > 0){
    buf[index] = Serial.read();
    index++;
    if (buf[index-1] == 190){  
      for(int i=0;i<index;i++)
      {
        Serial.print(buf[i]& 0xFF, HEX);
      } 
        Serial.println("");
      if(uint8_t(buf[4])==133)  //133=0x85 as Measurement Result Command code
      {
        distance = float(uint8_t(buf[7])*256+uint8_t(buf[8]))/10;
      } 
      
      index=0;
    }
  }
}
