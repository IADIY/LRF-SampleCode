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
        timeout=3)
except Exception as e:
    print(str(e))
    sys.exit()

#Laser OFF (Confirm LRF is in default off state)
cmd=b'$0003260029&'
ser.write(cmd) 

#Select functions
#4 main commands to choose: 1. Continuous Measurement (Not an option in sample code) 2. Single Measurement
#3. Laser ON 4. Laser OFF
while True:
    key=input("\nPlease enter the operation command:\n -s single measurement\n -o Laser ON\n -f Laser OFF\n -q Exit\n")

    #Single measurement
    if key=='s':
        ser.reset_input_buffer()
        cmd=b'$00022123&'
        ser.write(cmd)  
        #The confirmation response will be discard
        data=ser.read_until(b'&')
        #The second response includes the measurement
        data=ser.read_until(b'&')
        if(len(data)==18):
            print('Module response: '+str(data))
            distance = int(data[7:15])
            print(str(distance)+'mm\n')
            
    #Laser ON
    elif key=='o':
        cmd=b'$0003260130&'  
        ser.write(cmd)  

    #Laser OFF
    elif key=='f':
        cmd=b'$0003260029&'
        ser.write(cmd) 
        
    #Exit
    elif key=='q':
        ser.close()
        sys.exit()

    #Incorrect Input
    else:
        print("Invalid option. Please enter one of the above options.")
