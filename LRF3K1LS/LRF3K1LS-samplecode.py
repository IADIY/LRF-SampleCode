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
ser.baudrate = 19200
ser.bytesize = 8
ser.parity = 'N'
ser.topbits = 1
#ser.timeout = 3000
ser.open()
 
def receive():
    while(global_flag):
        #Read all data from the buffer
        data=ser.read_all()
        if(len(data)>=4):
            print(data)
            #When reading the measured distance returned by the module.
            if data[1]==0x01:
                if((data[2]>>7)&1)==1:
                    print("Distance is invalid")
                    continue
                if((data[2]>>6)&1)==1:
                    print("Angle is invalid")
                    continue
                if((data[2]>>5)&1)==0:
                    dataResolution=0.5
                else:
                    dataResolution=0.1
                #Calculate distance
                distance=(data[3]*256+data[4])*dataResolution
                print("Distance: "+str(round(distance,2))+ "mm")
                #Calculate angle
                if(data[5]<180):
                    angle=data[5]
                else:
                    angle=data[5]-256
                print("Angle: "+ str(round(angle,2))+" degree")
               
            #When reading the status of module
            elif data[1]==0x20:
                info=''
                if((data[2]>>7)&1)==0:
                    info+='Finish ranging, '
                else:
                    info+='Laser rangefinder is busy, '
                if((data[2]>>6)&1)==0:
                    info+='No Error\n'
                else:
                    info+='In Error\n'
                if((data[2]>>1)&1)==0:
                    info+='Tilt angle sensor off, '
                else:
                    info+='Tilt angle sensor ON, '
                if((data[2]>>0)&1)==0:
                    info+='Tilt angle sensor nornal'
                else:
                    info+='Tilt angle sensor abnormal'
                print(info)
                    


def main(args=None):
   
    global global_flag
    t = threading.Thread(target = receive)
    t.start()
    #Provide instructions for users
    print("\nPress the following commands:")
    print("   a: Single Measure (meter)")
    print("   s: Continuous Measure (meter)")
    print("   d: Stop Measurement")  
    print("   f: Read Status")  
    print("   q: Exit the program.")  
    #console operationq
    while global_flag:
        #laser on
        key=input("input:")
        if key=='a':
            ser.write(b'\x10\x83\x00\x7D')
        #laser off 
        if key=='s':
            ser.write(b'\x10\x83\x40\x3D')
        #laser measurment 
        if key=='d':
            ser.reset_input_buffer()
            ser.write(b'\x10\x84\x7C')
        if key=='f':
            ser.reset_input_buffer()
            ser.write(b'\x10\x80\x80')
        #quit out of
        if key=='q': 
            global_flag=False   
              
    ser.close()  
    print("End")
 
if __name__ == '__main__':
    main()

