# 60m High Accuracy Laser Rangefinder Module - LRF60M3PS
## Introduction
The 60m High Accuracy Laser Rangefinder Module (LRF60M3PS), produced by IADIY, is a precision laser rangefinder module utilizing phase-shift technology, offering an accuracy of ±3mm. It is designed for measuring distances of approximately 60m indoors and 40m outdoors. The compact and lightweight features make it convenient for OEM users to integrate into systems and equipment.

## Communication

### UART Parameters
- Baud Rate: 19200
- Parity Bits: None
- Stop Bits: 1
- Byte Size: 8

### Command List
| Command | Command Code |
| --- | --- |
| Single Measurement(auto) | AA 00 00 20 00 01 00 00 21 |
| Continuous Measurement(auto) | AA 00 00 20 00 01 00 04 25 |
| Stop Measurement | 58 |
| Laser ON | AA 00 01 BE 00 01 00 01 C1 |
| Laser OFF | AA 00 01 BE 00 01 00 00 C0 |

## More Details
To learn more about this product and to see a full data sheet, please visit: https://www.iadiy.com/laser-module/laser-sensor/laser-distance-sensor/60m-High-Accuracy-Laser-Rangefinder-Module

To learn more about IADIY and browse other great products please visit: https://www.iadiy.com/