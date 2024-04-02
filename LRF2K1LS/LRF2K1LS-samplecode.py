# =============================================================================
# The sample code will use the pyserial lib. Please use the following command to install the required packages.
# $ sudo pip install pyserial
# =============================================================================

import serial.tools.list_ports
import sys
import threading

#declare
global_flag=True

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
        timeout=3)
except Exception as e:
    print(str(e))
    sys.exit()
 
def receive():
    while(global_flag):
        #Read all data from the buffer
        data=ser.read_all()
        if(len(data)>=4):
            print('Module response: ' +str(data))
            #Depending on the response, perform different tasks
            #When reading a range finder result
            if data[1]==0x01:
                #Data 2nd byte's 7th bit states if distance is invalid
                if((data[2]>>7)&1)==1:
                    print("Distance is invalid")
                    continue
                
                #Data 2nd byte's 6th bit states if angle is invalid
                if((data[2]>>6)&1)==1:
                    print("Angle is invalid")
                    continue

                #Data 2nd byte's 5th bit states measurement's data resolution
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
               
            #When reading the status of  the module
            elif data[1]==0x20:
                info=''

                #Data 2nd byte's 7th bit displays measurement state
                if((data[2]>>7)&1)==0:
                    info+='Finish ranging, '
                else:
                    info+='Laser rangefinder is busy, '

                #Data 2nd byte's 6th bit states if an error occured
                if((data[2]>>6)&1)==0:
                    info+='No Error\n'
                else:
                    info+='In Error\n'

                #Data 2nd byte's 1st bit displays tilt angle sensor state
                if((data[2]>>1)&1)==0:
                    info+='Tilt angle sensor off, '
                else:
                    info+='Tilt angle sensor ON, '

                #Data 2nd byte's 0th bit states tilt angle sensor status
                if((data[2]>>0)&1)==0:
                    info+='Tilt angle sensor nornal'
                else:
                    info+='Tilt angle sensor abnormal'
                print(info)
                    


def main(args=None):
   
    global global_flag
    t = threading.Thread(target = receive)
    t.start()
 
    #console operation
    while global_flag:
        #Provide instructions for the user 
        key=input("\nPlease enter the operation command:\n -s single measurement (meter)\n\
                   -c continuous measurement (meter)\n -x stop measurement\n\
                   -r read status\n -q Exit\n")

        #Single measurement (meter)
        if key=='s':
            ser.reset_input_buffer()
            cmd=bytearray(b'\x10\x83\x00\x7D')
            ser.write(cmd)    

        #Continuous measurement (meter)
        elif key=='c':
            ser.reset_input_buffer()
            cmd=bytearray(b'\x10\x83\x40\x3D') 
            ser.write(cmd)   

        #Stop measurement
        elif key=='x':
            ser.reset_input_buffer()
            cmd=bytearray(b'\x10\x84\x7C')
            ser.write(cmd) 
        
        #Read status
        elif key=='r':
            ser.reset_input_buffer()
            cmd=bytearray(b'\x10\x80\x80')
            ser.write(cmd) 
            
        #Exit
        elif key=='q':
            global_flag = False
            ser.close()
            sys.exit()

        #Incorrect Input
        else:
            print("Invalid option. Please enter one of the above options.")
 
if __name__ == '__main__':
    main()

