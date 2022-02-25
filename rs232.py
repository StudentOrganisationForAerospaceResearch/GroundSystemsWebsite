# import serial

# s = serial.Serial('COM3', 9600, timeout=10)

# cs = 'qwerty'
# i = 0
# buf = b''

# while True:
#     rx = s.read()
#     buf += rx

#     # print(rx.hex())

#     if (len(buf) > 3) and (buf[-3:] == b'END'):
#         print(f"{i} [RX] {' '.join(buf[5:-3].hex()[i : i+2] for i in range(0, (len(buf)-8)*2, 2))}")
#         buf = b''
#     i = (i+1)%2

# import serial
# import time
# import binascii
# import csv

# order = 'big'
# class AvionicsData:
#     def __init__(self):
#         self.imu = [0] * 9
#         self.bar = [0] * 2
#         self.gps = [0] * 6
#         self.oxi = -1
#         self.cmb = -1
#         self.phs = -1
#         self.upperVnt = -1
#         self.injValve = -1
#         self.lowerVnt = -1

#     def __str__(self):
#         phases = ["NA", "PRELAUNCH", "ARM", "BURN", "COAST", "DROGUE_DESCENT", "MAIN_DESCENT", "POSTLAUNCH", 
#         "ABORT_COMMAND_RECEIVED", "ABORT_COMMUNICATION_ERROR", "ABORT_OXIDIZER_PRESSURE", "ABORT_UNSPECIFIED_REASON"]
#         valveStatus = ["NA","Closed", "Open"]

#         string="IMU - ACCEL:\t\t"+ str(self.imu[0:3])+" mg"+ "~ \n"
#         string+="IMU - GYRO:\t\t"+ str(self.imu[3:6])+" mdps"+"~ \n"
#         string+="BAR - PRESS:\t\t"+ str(self.bar[0]/100) +" mbar"+"~ \n"
#         string+="BAR - TEMP:\t\t"+  str(self.bar[1]/100)+" degrees C"+"~ \n"
#         string+="GPS - Time:\t\t"+  str(self.gps[0])+" utc "+"~ \n"
#         string+="GPS - LAT:\t\t"+  str(self.gps[1])+" degrees "+"~ \n"
#         string+="GPS - LAT:\t\t"+  str(self.gps[2])+" mins "+"~ \n"
#         string+="GPS - LONG:\t\t"+  str(self.gps[3])+" degrees "+"~ \n"
#         string+="GPS - LONG:\t\t"+  str(self.gps[4])+" mins "+"~ \n"
#         string+="GPS - ALT:\t\t"+  str(self.gps[5])+"  meters"+"~ \n"
#         string+="OXI - P:\t\t"+ str(self.oxi/1000)+" psi"+"~ \n"
#         string+="CMB - P:\t\t"+ str(self.cmb/1000)+" psi"+"~ \n"
#         string+="PHS -  PHASE:\t\t"+ str(phases[self.phs+1])+"~ \n"
#         # string+="Inj Valve:\t\t" + str(valveStatus[self.injValve+1])+"\n"
#         # string+="Lower Vent:\t\t" + str(valveStatus[self.lowerVnt+1])+"\n"

#         with open('fligthData.csv', 'a') as csvfile:
#             spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
#             spamwriter.writerow([str(self.imu[0]), str(self.imu[1]), str(self.imu[2]), str(self.imu[3]), str(self.imu[4]), str(self.imu[5]), str(self.bar[0]), str(self.bar[1])])

#         return string

# def twos_complement(hexstr,bits):
#     value = int(hexstr,16)
#     if value & (1 << (bits-1)):
#         value -= 1 << bits
#     return value

# def disconnect(ser):
#     ser.close()
#     time.sleep(1)
#     return None

# def readSerial(ser,data):
#     line = ser.read(256).hex()
#     i = 0
#     # if(line != ""):
#     #     print(line)
#     while(i<len(line)):
#         # IMU Data
#         # print(line[i:i+8])
#         # i=i+8
#         if((line[i:i+8]=='31313131')):
#             # print('IMU detected')
#             # print(line[i:i+82])
#             if(line[i+82:i+84]=='f0'):
#                 # print('Inside second if')
#                 # print(line[i:i+82])
#                 data.imu[0] = twos_complement(line[i+8:i+16], 32)
#                 data.imu[1] = twos_complement(line[i+16:i+24], 32)
#                 data.imu[2] = twos_complement(line[i+24:i+32], 32)
#                 data.imu[3] = twos_complement(line[i+32:i+40], 32)
#                 data.imu[4] = twos_complement(line[i+40:i+48], 32)
#                 data.imu[5] = twos_complement(line[i+48:i+56], 32)
#                 data.imu[6] = twos_complement(line[i+56:i+64], 32)
#                 data.imu[7] = twos_complement(line[i+64:i+72], 32)
#                 data.imu[8] = twos_complement(line[i+72:i+80], 32)
#                 i+=81
#             else: i+=1  
#         # Barometer Data
#         elif((line[i:i+8])=='32323232' and len(line)-i>=25):
#             # print('Barometer detected')
#             if(line[i+26:i+28]=='f0'):
#                 # print('Inside second if')
#                 # print(line[i:i+26])
#                 data.bar[0] = twos_complement(line[i+8:i+16], 32)
#                 data.bar[1] = twos_complement(line[i+16:i+24], 32)
#                 i+=25
#             else:
#                  i+=1

#         #GPS Data
#         elif((line[i:i+8]=='33333333') and (len(line)-i>=41)):
#             # print('GPS detected')
#             # print(line[i:i+60])
#             if(line[i+58:i+60]=='f0'):
#                 # print('Inside second if')
#                 # print(line[i:i+42])
#                 data.gps[0] = twos_complement(line[i+8:i+16], 32)
#                 data.gps[1] = twos_complement(line[i+16:i+24], 32)
#                 data.gps[2] = twos_complement(line[i+24:i+32], 32)
#                 data.gps[3] = twos_complement(line[i+32:i+40], 32)  
#                 data.gps[4] = twos_complement(line[i+40:i+48], 32)  
#                 data.gps[5] = twos_complement(line[i+48:i+56], 32)  
#                 i+=57
#             else:
#                  i+=1

#         #Oxidizer Tank Pressure
#         elif((line[i:i+8]=='34343434') and (len(line)-i>=17)):
#             # print('Oxidizer detected')
#             if(line[i+16:i+18]=='f0'):
#                 # print('Inside second if')
#                 data.oxi = twos_complement(line[i+8:i+16], 32)
#                 i+=17
#             else: i+=1

#         #Combustion Chamber Pressure
#         elif((line[i:i+8]=='35353535') and (len(line)-i>=17)):
#             # print('CC detected')
#             if(line[i+16:i+18]=='f0'):
#                 # print('Inside second if')
#                 data.cmb = twos_complement(line[i+8:i+16], 32)
#                 i+=17
#             else: i+=1

#         #Flight Phase
#         elif((line[i:i+8]=='36363636') and (len(line)-i>=13)):
#             # print('Flight Phase Detected')
#             if(line[i+10:i+12]=='f0'):
#                 # print('Inside second if')
#                 data.phs = int(line[i+8:i+10], 16)
#                 i+=12
#             else: i+=1

#         # #Injection Valve Status
#         # elif((line[i:i+8]=='38383838') and (len(line)-i>=13)):
#         #     if(line[i+10:i+12]=='f0'):
#         #         data.injValve = int(line[i+8:i+10], 16)
#         #         i+=12
#         #     else: i+=1

#         # #Lower Vent Valve
#         # elif((line[i:i+8]=='39393939') and (len(line)-i>=13)):
#         #     if(line[i+10:i+12]=='f0'):
#         #         data.lowerVnt = int(line[i+8:i+10], 16)
#         #         i+=12
#         #     else: i+=1

#         #No packet detected
#         else: i+=1
        
#     # print(data)


# if __name__ == "__main__":
#     ser = None
#     data = AvionicsData()
#     while(True):

#         # port = input('Enter a Serial Port to connect to:') #Linux: /dev/ttyUSBx, Windows: COMx
#         # Ground systems: com3, 9600
#         # Radio: com6? 57600
#         ser = serial.Serial('COM6', 57600, timeout=0) 

#         while(ser!=None):
#             # time.sleep(1)
#             readSerial(ser, data)
#             print(data.__str__())

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Agam's new updated script 


import serial
import serial.tools.list_ports
import time
import binascii
import csv

order = 'big'
class AvionicsData:
    def __init__(self):
        self.imu = [0] * 9
        self.bar = [0] * 2
        self.gps = [0] * 6


    def __str__(self):
        phases = ["NA", "PRELAUNCH", "ARM", "BURN", "COAST", "DROGUE_DESCENT", "MAIN_DESCENT", "POSTLAUNCH",
        "ABORT_COMMAND_RECEIVED", "ABORT_COMMUNICATION_ERROR", "ABORT_OXIDIZER_PRESSURE", "ABORT_UNSPECIFIED_REASON"]
        valveStatus = ["NA","Closed", "Open"]

        string="IMU - ACCEL:\t\t"+ str(self.imu[0:3])+" mg"+ "~ \n"
        string+="IMU - GYRO:\t\t"+ str(self.imu[3:6])+" mdps"+"~ \n"
        string+="BAR - PRESS:\t\t"+ str(self.bar[0]/100) +" mbar"+"~ \n"
        string+="BAR - TEMP:\t\t"+  str(self.bar[1]/100)+" degrees C"+"~ \n"
        string+="GPS - Time:\t\t"+  str(self.gps[0])+" utc "+"~ \n"
        string+="GPS - LAT:\t\t"+  str(self.gps[1])+" degrees "+"~ \n"
        string+="GPS - LAT:\t\t"+  str(self.gps[2])+" mins "+"~ \n"
        string+="GPS - LONG:\t\t"+  str(self.gps[3])+" degrees "+"~ \n"
        string+="GPS - LONG:\t\t"+  str(self.gps[4])+" mins "+"~ \n"
        string+="GPS - ALT:\t\t"+  str(self.gps[5])+" meters"+"~ \n"

        with open('fligthData.csv', 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([str(self.imu[0]), str(self.imu[1]), str(self.imu[2]),
                                str(self.imu[3]), str(self.imu[4]), str(self.imu[5]),
                                str(self.bar[0]), str(self.bar[1]),
                                str(self.gps[0]), str(self.gps[1]), str(self.gps[2]),
                                str(self.gps[3]), str(self.gps[4]), str(self.gps[5])])
        return string

def twos_complement(hexstr,bits):
    if hexstr == '':
        return 0
    value = int(hexstr,16)
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return value

def disconnect(ser):
    ser.close()
    time.sleep(1)
    return None

def readSerial(line,data):
    i = 0
    #print(line)
    while(i<len(line)):

        # IMU Data
        if((line[i:i+8]=='31313131')):
            data.imu[0] = twos_complement(line[i+8:i+16], 32)
            data.imu[1] = twos_complement(line[i+16:i+24], 32)
            data.imu[2] = twos_complement(line[i+24:i+32], 32)
            data.imu[3] = twos_complement(line[i+32:i+40], 32)
            data.imu[4] = twos_complement(line[i+40:i+48], 32)
            data.imu[5] = twos_complement(line[i+48:i+56], 32)
            data.imu[6] = twos_complement(line[i+56:i+64], 32)
            data.imu[7] = twos_complement(line[i+64:i+72], 32)
            data.imu[8] = twos_complement(line[i+72:i+80], 32)
            i+=80

        # Barometer Data
        elif((line[i:i+8])=='32323232'):
            data.bar[0] = twos_complement(line[i+8:i+16], 32)
            data.bar[1] = twos_complement(line[i+16:i+24], 32)
            i+=24

        #GPS Data
        elif((line[i:i+8]=='33333333')):
            data.gps[0] = twos_complement(line[i+8:i+16], 32)
            data.gps[1] = twos_complement(line[i+16:i+24], 32)
            data.gps[2] = twos_complement(line[i+24:i+32], 32)
            data.gps[3] = twos_complement(line[i+32:i+40], 32)
            data.gps[4] = twos_complement(line[i+40:i+48], 32)
            data.gps[5] = twos_complement(line[i+48:i+56], 32)
            i+=57

        #No packet detected
        else: i+=1

    # print(data)


if __name__ == "__main__":
    ser = None
    data = AvionicsData()
    comPortList = serial.tools.list_ports.comports()
    rs232Port = '' # ASSUMING THERE IS ONLY ONE CONNECTED !!!!!!!
    for element in comPortList:
        rs232Port = (element.device)
    print (rs232Port)
    while(True):

        # port = input('Enter a Serial Port to connect to:') #Linux: /dev/ttyUSBx, Windows: COMx
        # radio: 57600, umbilical: 9600, debug: 115200 
        ser = serial.Serial(rs232Port, 57600, timeout=None)
        line = b''
        while(ser!=None):
            # time.sleep(1)
            rx = ser.read()
            line += rx
            print(line.hex()) 
            if (len(line) > 3) and (line[-3:] == b'END'):
                # print("---")
                # print(line.hex())
                # print("---")
                readSerial(line.hex(), data)
                line = b''
                print(data.__str__())
