# =============================================================================
# The sample code will use the pyserial lib. Please use the following command to install the required packages.
# $ sudo pip install pyserial
# =============================================================================

import serial 
import time

#declare
global_flag=True
#serial port
ser = serial.Serial()
#ser.port = '/dev/ttyUSB0' #Note usb port should reflect which port the module is plugged in to - use ls /dev/ttyUSB* command to identify port
ser.port = 'COM5'
ser.bytesize = 8
ser.parity = 'N'
ser.topbits = 1
ser.baudrate = 9600
ser.timeout = .5
ser.open()
      
def main(args=None):
    global global_flag
    #Provide instructions for users
    print("\nPress the following commands:")
    print("   a: Laser ON")
    print("   s: Laser OFF")
    print("   d: Single Measurement\n")  
    #console operation
    while global_flag:
        #laser on
        key=input("input:")
        if key=='a':
            ser.write(b'\x80\x06\x05\x01\x74')
        #laser off 
        if key=='s':
            ser.write(b'\x80\x06\x05\x00\x75')
        #laser measurment 
        if key=='d':
            ser.reset_input_buffer()
            ser.write(b'\x80\x06\x02\x78')
            time.sleep(1)
            data = ser.readline()
            if data[2]==0x82 and len(data)==11: #(Under the resolution setting of 1mm)
                ascii_string = ''.join([chr(byte) for byte in data[3:10]])
                float_value = float(ascii_string)
                print(str(float_value)+"m")
            elif data[2]==0x82 and len(data)==12: #(Under the resolution setting of 0.1mm)
                ascii_string = ''.join([chr(byte) for byte in data[3:11]])
                float_value = float(ascii_string)
                print(str(float_value)+"m")
        #quit out of
        if key=='q': 
            global_flag=False   
              
    ser.close()  
    print("exit sample code")
    

if __name__ == '__main__':
    main()
