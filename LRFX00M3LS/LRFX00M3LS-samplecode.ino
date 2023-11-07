#define laserSerial Serial
unsigned char buf[50]; 
int index = 0; 

void setup() {
  Serial.begin(9600);
  laserSerial.begin(9600);
    
  //byte data1[9] = {0xAE, 0xA7, 0x05, 0x00, 0x40, 0x00, 0x45, 0xBC, 0xBE};  //Laser OFF
  byte data1[9] = {0xAE, 0xA7, 0x05, 0x00, 0x40, 0x01, 0x46, 0xBC, 0xBE};  //Laser ON
  laserSerial.write(data1, sizeof(data1));
  delay(500);
    
  //byte data2[8] = {0xAE, 0xA7, 0x04, 0x00, 0x05, 0x09, 0xBC, 0xBE};  //Single Measure
  byte data2[8] = {0xAE, 0xA7, 0x04, 0x00, 0x0E, 0x12, 0xBC, 0xBE};  //Continus Measure
  //byte data2[8] = {0xAE, 0xA7, 0x04, 0x00, 0x0F, 0x13, 0xBC, 0xBE};  //Stop Measure
  laserSerial.write(data2, sizeof(data2));
  delay(500);
}

void loop() {
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
        float distance = float(uint8_t(buf[7])*256+uint8_t(buf[8]))/10;
        Serial.print(distance);
        Serial.println("m");
      }
      index=0;
    }
  }
}
