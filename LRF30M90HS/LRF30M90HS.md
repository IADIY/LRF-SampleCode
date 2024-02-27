# 30m High Frequency Laser Distance Measuring Module - LRF30M90HS
## Introduction
The High Frequency Laser Distance Measuring Module (LRF30M90HS), produced by IADIY, provides a maximum measurement frequency of 90Hz using a 780nm laser and can reach a maximum measurement distance of up to 30 meters.  It is particularly suitable for measuring dynamic targets and real-time applications. Its compact design facilitates seamless integration into users' systems or devices. Moreover, the module employs a standard TTL (UART) communication interface, empowering users to develop and program their own applications.

## Communication

### UART Parameters
- Baud Rate: 115200
- Parity Bits: None
- Stop Bits: 1
- Byte Size: 8

### Command List
| Command | Command Code |
| --- | --- |
| Single Measurement | ~01030100000185F6\r\n |
| Continuous Measurement | ~01060000000089CA\r\n |
| Stop Measurement | ~010600000001480A\r\n |
| Laser ON | ~0106003000014805\r\n |
| Laser OFF | ~01060030000089C5\r\n |

## More Details
To learn more about this product and to see a full data sheet, please visit: https://www.iadiy.com/laser-module/laser-sensor/laser-distance-sensor/high-frequency-laser-distance-measuring-module

To learn more about IADIY and browse other great products please visit: https://www.iadiy.com/