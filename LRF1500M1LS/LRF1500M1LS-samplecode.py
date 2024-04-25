# =============================================================================
# The sample code will use the pyserial lib. Please use the following command to install the required packages.
# $ sudo pip install pyserial
# =============================================================================

import serial.tools.list_ports
import sys
import threading

#List available COMport
ports = serial.tools.list_ports.comports()
portlist=[]
index=0
for port, desc, hwid in ports:
    portlist.append(port)
    print(str(index)+") "+desc+"|"+port)
    index+=1
if portlist == []:
    print("No serial ports detected")
    sys.exit()

#Select COMport
portname=input("Please input the number of the desired port: \n")
try:
    ser = serial.Serial(
        port=portlist[int(portname)],\
        baudrate=115200,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout=0.5)
except Exception as e:
    print(str(e))
    sys.exit()

#Stop Measurement(Prevent the module from being in continuous measurement mode.)
cmd=bytearray(b'\x55\xAA\x8E\xFF\xFF\xFF\xFF\x8A') 
ser.write(cmd)  

#Set up continuous measurement function
globalFlag=False
threadFlag=True
def continuousMeasurement():
    while(threadFlag):
        while(globalFlag):
            #clear buffer
            ser.reset_input_buffer()
            data = ser.read(8)
            print(data)
            #if thread is ended before it is able to read measurement
            if(len(data)<7):
                 print("Continuous Measurement Quit")
            #If there is an error
            elif((hex(data[5]) == '0xff') | (hex(data[4]) == '0x00')):
                    print("Measurement Failed")
            else:
                #splice out the distance from the complete message - cast it as an int to eliminate leading 0's
                distance = (int.from_bytes(data[5:7], "big"))/10
                print("Distance is: %sm"% distance)

#Set up threading for continuous measurement
t = threading.Thread(target = continuousMeasurement)
t.start()
   
#Select functions
while True:
    key=input("\nPlease enter the operation command:\n -s single measurement\n -c continuous measurement\n -q Exit\n")

    #single measurement
    if key=='s':
        ser.reset_input_buffer()
        cmd=bytearray(b'\x55\xAA\x88\xFF\xFF\xFF\xFF\x84')  
        ser.write(cmd)  
        data = ser.readline()
        #data = ser.readline()
        print(data)
        #if the module returns error messsage 
        if((hex(data[5]) == '0xff') | (hex(data[4]) == '0x00')):
                print("Measurement Failed")
        else:
            #splice out the distance from the complete message - cast it as an int to eliminate leading 0's
            distance = (int.from_bytes(data[5:7], "big"))/10
            print("Distance is: %sm"% distance)

    #Continuous measurement
    elif key=='c':
        #start continous measurement
        cmd=bytearray(b'\x55\xAA\x89\xFF\xFF\xFF\xFF\x85')  
        ser.write(cmd)   
        globalFlag=True
        stopMeasurement=input("\nPlease press any key to stop the measurement\n")
        #Stop Measurement
        cmd=bytearray(b'\x55\xAA\x8E\xFF\xFF\xFF\xFF\x8A') 
        ser.write(cmd) 
        globalFlag=False
        
    #Exit
    elif key=='q':
        threadFlag=False
        ser.close()
        sys.exit()
    
    #Incorrect Input
    else:
        print("Invalid option. Please enter one of the above options.")