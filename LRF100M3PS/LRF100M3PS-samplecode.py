# =============================================================================
# The sample code will use the pyserial lib. Please use the following command to install the required packages.
# $ sudo pip install pyserial
# =============================================================================

import serial.tools.list_ports
import sys

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
        baudrate=19200,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout=0.5)
except Exception as e:
    print(str(e))
    sys.exit()

#Stop Measurement(Prevent the module from being in continuous measurement mode.)
cmd=b'\x58'  
ser.write(cmd)  
   
#Select functions
while True:
    key=input("\nPlease enter the operation command:\n -s single measurement\n -o Laser ON\n -f Laser OFF\n -q Exit\n")

    #single measurement
    if key=='s':
        ser.reset_input_buffer()
        cmd=bytearray(b'\xAA\x00\x00\x20\x00\x01\x00\x00\x21')  
        ser.write(cmd)  
        data = ser.readline()
        #wait for the module to respond with a message - empty message is shorter than 1
        while(len(data) < 1):
            data=ser.readline()
        #if the module returns error messsage 
        if(hex(data[0]) == '0xee'):
                print(data)
        else:
            print('Module response: '+str(data))
            #splice out the distance from the complete message - cast it as an int to eliminate leading 0's
            distance = int.from_bytes(data[6:10], "big")
            print("Distance is: %smm"% distance)

    #Laser ON
    elif key=='o':
        cmd=bytearray(b'\xAA\x00\x01\xBE\x00\x01\x00\x01\xC1')  
        ser.write(cmd)  

    #Laser OFF
    elif key=='f':
        cmd=bytearray(b'\xAA\x00\x01\xBE\x00\x01\x00\x00\xC0')  
        ser.write(cmd) 
        
    #Exit
    elif key=='q':
        ser.close()
        sys.exit()
    
    #Incorrect Input
    else:
        print("Invalid option. Please enter one of the above options.")