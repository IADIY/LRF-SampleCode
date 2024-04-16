# 50m/150m/200m Industrial High Frequency Laser Rangefinder Module - LRFX0M20KHS
## Introduction
The 50m/150m/200m Industrial High Frequency Laser Rangefinder Module (LRFX0M20KHS), produced by IADIY, is a high-speed rangefinder module designed to deliver exceptional performance. Its maximum frequency can reach 20KHz, and users can configure the frequency from 20Hz to 20KHz through commands. With its compact size and lightweight design, it's perfect for seamless integration into various devices. This module is suitable for both indoor and outdoor use. We offer three measurement distance options: 50 meters, 150 meters, and 200 meters, catering to diverse needs. Experience precision, versatility, and convenience all in one advanced solution.

## Communication
Measurement frequency can be adjusted and set as necessary: 20Hz~20KHz
### UART Parameters
- Baud Rate: 9600 / 19200 / 115200 / 256000 / 460800 / 921600
- Parity Bits: None
- Stop Bits: 1
- Byte Size: 8

### Command List
| Command | Command Code |
| --- | --- |
| Set Frequency | 5A 0B 02 XX XX XX |
| Get Frequency | 5A 9B 02 1B 1B AC |
| Set Baud Rate | 5A 06 02 XX XX XX |

XX indicates that the user needs to change the input depending on their objective. For example, to set the Baud Rate at 115200, the command would be the following: 5A 06 02 80 04 73


## More Details
To learn more about this product and to see a full data sheet, please visit: https://www.iadiy.com/Industrial-High-Frequency-Laser-Rangefinder-Module

To learn more about IADIY and browse other great products please visit: https://www.iadiy.com/
