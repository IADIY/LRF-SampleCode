import serial 
import time
import sys

#declare
global_flag=True
#serial port
ser = serial.Serial()
ser.port = '/dev/ttyUSB0' #Note usb port should reflect which port the module is plugged in to - use ls /dev/ttyUSB* command to identify port
ser.baudrate = 19200
ser.bytesize = 8
ser.parity = 'N'
ser.topbits = 1
ser.timeout = .5
ser.open()
      
def main(args=None):
    global global_flag
    #Provide instructions for users
    print("\nPress the following commands:")
    print("   a: Laser ON")
    print("   s: Laser OFF")
    print("   d: Return the distance in millimeter\n")  
    #console operation
    while global_flag:
        #laser on
        key=input("input:")
        if key=='a':
            ser.write(b'\xAA\x00\x01\xBE\x00\x01\x00\x01\xC1')
        #laser off 
        if key=='s':
            ser.write(b'\xAA\x00\x01\xBE\x00\x01\x00\x00\xC0')
        #laser measurment 
        if key=='d':
            ser.write(b'\xAA\x00\x00\x20\x00\x01\x00\x00\x21')
            ser.reset_input_buffer()
            data = ser.readline()
            #wait for the module to respond with a message - empy message is shorter than 1
            while(len(data) < 1):
                data=ser.readline()
            #if the module returns error messsage 
            if(hex(data[0]) == '0xee'):
                print(data)
            else:
                #splice out the distance from the complete message - cast it as an int to eliminate leading 0's
                distance = hex(data[6])[2:] + hex(data[7])[2:] + hex(data[8])[2:] + hex(data[9])[2:]
                distance = int(distance, 16)
                print("Distance is: %smm"% distance)
        #quit out of
        if key=='q': 
            global_flag=False   
              
    ser.close()  
    print("End~")
    

if __name__ == '__main__':
    main()
