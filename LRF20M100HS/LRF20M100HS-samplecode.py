# =============================================================================
# The sample code will use the pyserial lib. Please use the following command to install the required packages.
# $ sudo pip install pyserial
# =============================================================================

import serial.tools.list_ports
import sys
import threading
import time

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
        baudrate=921600,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout=0.5)
except Exception as e:
    print(str(e))
    sys.exit()

#Receive and print module return data
stop_thread = False
def th_read():
    while not stop_thread:
        data = ser.read_all() #read all buffer
        position = data.find(b'\xA5\x03\x20')
        if(len(data)>=position+23): #ensure the data frame is complete, 23 is the length of the measurement return data
            ser.reset_input_buffer()
            distance=data[position+13]+data[position+14]*256
            print(distance,"mm", flush=True)

t = threading.Thread(target=th_read) 
t.start()

#Select functions
while True:
    key=input("\nPlease enter the operation command:\n -a Start measurement\n -s Stop measurement\n -q Exit\n")

    #Start measurement
    if key=='a':
        cmd=bytearray(b'\xA5\x03\x20\x01\x00\x00\x00\x02\x6E')  
        ser.write(cmd)  
       
    #Stop measurement
    elif key=='s':
        cmd=bytearray(b'\xA5\x03\x20\x02\x00\x00\x00\x46\x6E')  
        ser.write(cmd)  

    #Exit
    elif key=='q':
        stop_thread=True
        ser.close()
        sys.exit()
    
    #Incorrect Input
    else:
        print("Invalid option. Please enter one of the above options.")