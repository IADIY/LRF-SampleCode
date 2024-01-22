# =============================================================================
# The sample code will use the pyserial lib. Please use the following command to install the required packages.
# $ sudo pip install pyserial
# =============================================================================

import serial 
import threading

#declare
global_flag=True
#serial port
ser = serial.Serial()
#ser.port = '/dev/ttyUSB0' #(Linux)Note usb port should reflect which port the module is plugged in to - use ls /dev/ttyUSB* command to identify port
ser.port = 'COM4'          #(Windows)Note usb port should reflect which port the module is plugged in to COM port, usw device manager to identify port
ser.baudrate = 115200
ser.bytesize = 8
ser.parity = 'N'
ser.topbits = 1
ser.timeout = 3000
ser.open()

def receive():
    while(global_flag):
        data=ser.read_all()
        if(len(data)>0):
            if(data[0:7]==b'$000621'):
                #decode from bytes to string for formatting
                data = data.decode('utf-8')
                print(data)
                #splice out the distance from the complete message - cast it as an int to eliminate leading 0's
                distance = int(data[7:15])
                print("Distance is: %smm"% distance)



def main(args=None):
    global global_flag
    t = threading.Thread(target = receive)
    t.start()
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
            ser.reset_input_buffer()
            ser.write(b'$0003260130&')
        #laser off 
        if key=='s':
            ser.reset_input_buffer()
            ser.write(b'$0003260029&')
        #laser measurment 
        if key=='d':
            ser.reset_input_buffer()
            ser.write(b'$00022123&')
        #quit out of
        if key=='q': 
            global_flag=False   
              
    ser.close()  
    print("End~")
    

if __name__ == '__main__':
    main()
