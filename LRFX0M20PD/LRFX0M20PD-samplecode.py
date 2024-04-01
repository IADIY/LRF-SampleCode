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
        baudrate=9600,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout=0.5)
except Exception as e:
    print(str(e))
    sys.exit()


#Select functions
while True:
    key=input("\nPlease enter the operation command:\n -s single measurement\n -o Laser ON\n -f Laser OFF\n -q Exit\n")

    #single measurement
    if key=='s':
        ser.reset_input_buffer()
        cmd=bytearray(b'\x80\x06\x02\x78')  
        ser.write(cmd) 
        data = ser.readline()
        #Under the resolution setting of 1mm
        if len(data)==11: 
            print('Module response: '+str(data))
            distance=float(data[3:10].decode('ascii'))
            print(str(distance)+"m")
        #Under the resolution setting of 0.1mm   
        elif len(data)==12: 
            print('Module response: '+str(data))
            distance=float(data[3:11].decode('ascii'))
            print(str(distance)+"m")

    #Laser ON
    elif key=='o':
        cmd=bytearray(b'\x80\x06\x05\x01\x74')  
        ser.write(cmd)  

    #Laser OFF
    elif key=='f':
        cmd=bytearray(b'\x80\x06\x05\x00\x75')  
        ser.write(cmd) 
        
    #Exit
    elif key=='q':
        ser.close()
        sys.exit()
    
    #Incorrect Input
    else:
        print("Invalid option. Please enter one of the above options.")