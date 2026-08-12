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
        baudrate=115200,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout=1)
except Exception as e:
    print(str(e))
    sys.exit()
    
#Select functions
while True:
    key=input("\nPlease enter the operation command:\n -s single measurement\n -q Exit\n")

    #single measurement
    if key=='s':
        ser.reset_input_buffer()
        cmd=bytearray(b'\xEE\x16\x02\x03\x02\x05')  
        ser.write(cmd)  
        data=ser.read(10)
        print('Module response: '+str(data))
        if(data[5]==4):
            print('out of Range')
        else:
            distance=(data[6]*256+data[7]+(data[8]/10))
            print(str(distance)+'m\n')

    #Exit
    elif key=='q':
        ser.close()
        sys.exit()

    #Incorrect Input
    else:
        print("Invalid option. Please enter one of the above options.")