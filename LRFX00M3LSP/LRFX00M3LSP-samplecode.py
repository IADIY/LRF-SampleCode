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
        timeout=None)
except Exception as e:
    print(str(e))
    sys.exit()
    
#Select functions
while True:
    key=input("\nPlease enter the operation command:\n -s single measurement\n -o Laser ON\n -f Laser OFF\n -q Exit\n")

    #single measurement
    if key=='s':
        cmd=bytearray(b'\xAE\xA7\x04\x00\x05\x09\xBC\xBE')  
        ser.write(cmd)  
        data=ser.read_until(b'\xBC\xBE')
        print(data)
        if(len(data)==8):
            print('Invalid result (too close or too far)')
        elif(len(data)==27):
            distance=(data[7]*256+data[8] / 10)
            print(str(distance)+'mm\n')

    #Laser ON
    elif key=='o':
        cmd=bytearray(b'\xAE\xA7\x05\x00\x40\x01\x46\xBC\xBE')  
        ser.write(cmd)  

    #Laser OFF
    elif key=='f':
        cmd=bytearray(b'\xAE\xA7\x05\x00\x40\x00\x45\xBC\xBE')  
        ser.write(cmd) 
        
    #Exit
    elif key=='q':
        ser.close()
        sys.exit()


