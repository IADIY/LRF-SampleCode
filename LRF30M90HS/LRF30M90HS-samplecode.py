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
    print(str(index)+": "+port)
    index+=1

#Select COMport
portname=input("Please input COMport number: ")
try:
    ser = serial.Serial(
        port=portlist[int(portname)],\
        baudrate=115200,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout=0.1)
except Exception as e:
    print(str(e))
    sys.exit()

#Stop Measurement(Prevent the module from being in continuous measurement mode.)
cmd=b'~010600000001480A\r\n'  
ser.write(cmd)  

#Select functions
#4 main commands to choose: 1. Continuous Measurement (Not an option in sample code) 2. Single Measurement
#3. Laser ON 4. Laser OFF
while True:
    key=input("\nPlease enter the operation command:\n -s single measurement\n -o Laser ON\n -f Laser OFF\n -q Exit\n")

    #Single measurement
    if key=='s':
        ser.reset_input_buffer()
        cmd=b'~01030100000185F6\r\n'
        ser.write(cmd)  
        data=ser.read_until(b'\r\n')
        if(len(data)==19):
            print('Module response: '+str(data))
            distance=int(data[9:13].decode('ascii'), 16)
            print(str(distance)+'mm\n')
            
    #Laser ON
    elif key=='o':
        cmd=b'~0106003000014805\r\n'  
        ser.write(cmd)  

    #Laser OFF
    elif key=='f':
        cmd=b'~01060030000089C5\r\n'
        ser.write(cmd) 
        
    #Exit
    elif key=='q':
        ser.close()
        sys.exit()

    #Incorrect Input
    else:
        print("Invalid option. Please enter one of the above options.")


