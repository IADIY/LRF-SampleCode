#include <HardwareSerial.h>

HardwareSerial serialDevice(1);  // Use UART1 (Serial1)

void setup() {
  Serial.begin(115200);                                // Debug output to Serial Monitor
  serialDevice.begin(921600, SERIAL_8N1, 19, 18);      // RX=GPIO19, TX=GPIO18
  delay(100);                                          // Short wait before sending command

  // Send the "start measurement" command
  uint8_t cmd[] = {0xA5, 0x03, 0x20, 0x01, 0x00, 0x00, 0x00, 0x02, 0x6E};
  serialDevice.write(cmd, sizeof(cmd));
  Serial.println("Command sent. Waiting for measurement frame...");
}

void loop() {
  static uint8_t buffer[21];
  static uint8_t idx = 0;

  while (serialDevice.available()) {
    uint8_t b = serialDevice.read();
    if (idx == 0 && b != 0xA5) continue;  // Wait for start-of-frame byte

    buffer[idx++] = b;

    if (idx == 21) {
      // Validate fixed header/frame format
      if (buffer[0] == 0xA5 && buffer[1] == 0x03 && buffer[2] == 0x20 &&
          buffer[3] == 0x01 && buffer[6] == 0x0E) {
        // Extract distance: bytes 13 (low) and 14 (high)
        uint16_t distance = (buffer[14] << 8) | buffer[13];
        Serial.print("Distance (mm): ");
        Serial.println(distance);
      } else {
        Serial.println("Invalid frame detected");
      }
      idx = 0;  // Reset to look for a new frame
    }
  }
}
