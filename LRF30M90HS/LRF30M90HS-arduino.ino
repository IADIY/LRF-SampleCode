#include <Arduino.h>
#define laserSerial Serial

void setup(void) {
  Serial.begin(115200);
  laserSerial.begin(115200);
  
  //Laser ON (ASCII)
  //char asciiString_1[] = "~0106003000014805\r\n";   
  //laserSerial.write(asciiString_1);

  //Laser ON (HEX)
  byte asciiString_1[19] = {0x7E, 0x30, 0x31, 0x30, 0x36, 0x30, 0x30, 0x33, 0x30, 0x30, 0x30, 0x30, 0x31, 0x34, 0x38, 0x30, 0x35, 0x0D, 0x0A};  
  laserSerial.write(asciiString_1, sizeof(asciiString_1));
  
  delay(100);
  char asciiString_2[] = "~01060000000089CA\r\n";   //Continuous Measurement 
  laserSerial.write(asciiString_2);
  delay(1000);
}

void loop(void) {
  String data = Serial.readStringUntil('\n');
  //Serial.println(data+",  "+(String)data.length());  //18
  if(data.length()>=18) {
    int distance=0;
    distance+=(data[9]  <= '9' ? data[9]  - '0' : data[9]  +  - '0' - 7)*4096;
    distance+=(data[10] <= '9' ? data[10] - '0' : data[10] +  - '0' - 7)*256;
    distance+=(data[11] <= '9' ? data[11] - '0' : data[11] +  - '0' - 7)*16;
    distance+=(data[12] <= '9' ? data[12] - '0' : data[12] +  - '0' - 7);
    Serial.println(data+",  distance="+(String)distance+"mm");
    //Serial.println(data+",  "+(String)A+", "+(String)B+", "+(String)C+", "+(String)D+",  distance="+(String)distance+"mm");
  }
  else
     Serial.println(data);


}
