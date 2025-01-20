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
    #NOTE: Depending on what the baud rate was changed to, may need to edit the baudrate here too before you can reconnect
    ser = serial.Serial(
        port=portlist[int(portname)],\
        baudrate=460800,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout=3) 
except Exception as e:
    print(str(e))
    sys.exit()

#Set up continuous measurement function
globalFlag=False
threadFlag=True
def continuousMeasurement():
    while(threadFlag):
        while(globalFlag):
            #clear buffer
            ser.reset_input_buffer()
            #the next 4 bytes will be the newest measurement data
            data = ser.read(4)
            #only print the data if it is in the right order
            if data[0] == 92:
                distance = int.from_bytes(data[1:3],'little')
                print('Distance: ' + str(distance)+'cm')
            elif data[2] == 92:
                #rearrange data if in wrong order
                temp = []
                temp[0:2]=data[2:4]
                temp[2:4]=data[0:2]
                data=temp
                distance = int.from_bytes(data[1:3],'little')
                print('Distance: ' + str(distance)+'cm')

#Set up threading for continuous measurement
t = threading.Thread(target = continuousMeasurement)
t.start()

#Select functions
while True:
    key=input("\nPlease enter the operation command:\n -s set frequency\n -g get frequency\n \
-b set baud rate\n -r single measurement\n -c continuous measurement\n -q Exit\n")

    #Set frequency
    if key=='s':
        freqSelection=input("\nPlease choose the desired frequency:\n -a 20Hz\n -b 200Hz\n -c 2000Hz\n -d 20000Hz\n")
        #20Hz
        if freqSelection=='a':
             
            cmd=bytearray(b'\x5A\x0B\x02\x4F\xC3\xE0')  
            ser.write(cmd)
            print("\nfrequency set to 20Hz")
        #200Hz
        elif freqSelection=='b':
            cmd=bytearray(b'\x5A\x0B\x02\x87\x13\x58')  
            ser.write(cmd)
            print("\nfrequency set to 200Hz")
        #2000Hz
        elif freqSelection=='c':
            cmd=bytearray(b'\x5A\x0B\x02\xF3\x01\xFE')  
            ser.write(cmd)
            print("\nfrequency set to 2000Hz")
        #20000Hz
        elif freqSelection=='d':
            cmd=bytearray(b'\x5A\x0B\x02\x31\x00\xC1')  
            ser.write(cmd)
            print("\nFrequency set to 20000Hz")
        #Incorrect Input
        else:
            print("Invalid option. Please enter one of the above options.")
    
    #Get frequency
    elif key=='g':
        #clear buffer
        ser.reset_input_buffer()
        cmd=bytearray(b'\x5A\x1B\x02\x1B\x1B\xAC')  
        ser.write(cmd)  
        #read until the relevant data
        #155 decimal == b'\x9b', finds the relevant data
        flag = True
        while flag:
            temp = ser.read()
            if temp == b'\x9b':
                flag = False
        #after \x9b, 2 of the next 3 bytes contain the frequency
        data = ser.read(3)
        #take only the portion that contains the frequency factor
        factor = int.from_bytes(data[1:3],'little')
        freq = int(1000000/(factor + 1))
        print('Frequency: '+str(freq)+'Hz')


    #Set baudrate
    #Depending on the frequency, the baud rate may need to change
    elif key=='b':
        baudSelection=input("\nPlease choose a baud rate:\n -a 9600\n -b 460800\n -c 921600\n")
        #9600 bps
        if baudSelection =='a':
            cmd=bytearray(b'\x5A\x06\x02\x60\x00\x97')
            ser.write(cmd)
            ser.baudrate=9600
            print("\nBaud rate set to 9600")
        #460800 bps
        elif baudSelection=='b':
            cmd=bytearray(b'\x5A\x06\x02\x00\x12\xEB')
            ser.write(cmd)
            ser.baudrate=460800
            print("\nBaud rate set to 460800")
        #921600 bps
        elif baudSelection=='c':
            ser.reset_input_buffer()
            cmd=bytearray(b'\x5A\x06\x02\x00\x24\xD3')
            ser.write(cmd)
            ser.baudrate=921600
            print("\nBaud rate set to 921600")

        #Incorrect Input
        else:
            print("Invalid option. Please enter one of the above options.")
         
    #Single measurement
    elif key=='r':
        #clear buffer
        ser.reset_input_buffer()
        #the next 4 bytes will be the newest measurement data
        data = ser.read(4)
        #only print the data if it is in the right order
        if data[0] == 92:
            distance = int.from_bytes(data[1:3],'little')
            print('Distance: ' + str(distance)+'cm')
        elif data[2] == 92:
            #rearrange data if in wrong order
            temp = []
            temp[0:2]=data[2:4]
            temp[2:4]=data[0:2]
            data=temp
            distance = int.from_bytes(data[1:3],'little')
            print('Distance: ' + str(distance)+'cm')
        
    #Continuous measurement
    elif key=='c':
        #start continous measurement   
        globalFlag=True
        stopMeasurement=input("\nPlease press any key to stop the measurement\n")
        globalFlag=False
        
    #Exit
    elif key=='q':
        threadFlag=False
        ser.close()
        sys.exit()
    
    #Incorrect Input
    else:
        print("Invalid option. Please enter one of the above options.")
