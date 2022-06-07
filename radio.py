import serial
import serial.tools.list_ports
import time
import binascii
import csv


class AvionicsData:
    def __init__(self):
        self.imu = [0] * 9
        self.bar = [0] * 2
        self.gps = [0] * 6
        self.flightPhase = 0
        self.tick = 0


    def __str__(self):
        phases = ["NA", "PRELAUNCH", "ARM", "BURN", "COAST", "DROGUE_DESCENT", "MAIN_DESCENT", "POSTLAUNCH",
        "ABORT_COMMAND_RECEIVED", "ABORT_COMMUNICATION_ERROR", "ABORT_OXIDIZER_PRESSURE", "ABORT_UNSPECIFIED_REASON"]
        valveStatus = ["NA","Closed", "Open"]

        string="IMU - ACCEL:\t\t"+ str(self.imu[0:3])+" mg"+ "\n"
        string+="IMU -  GYRO:\t\t"+ str(self.imu[3:6])+" mdps"+"\n"
        string+="BAR - PRESS:\t\t"+ str(self.bar[0]) +" mbar"+"\n"
        string+="BAR -  TEMP:\t\t"+  str(self.bar[1])+" degrees C"+"\n"
        string+="GPS -  Time:\t\t"+  str(self.gps[0])+" utc "+"\n"
        string+="GPS -   LAT:\t\t"+  str(self.gps[1])+" degrees "+"\n"
        string+="GPS -   LAT:\t\t"+  str(self.gps[2])+" mins "+"\n"
        string+="GPS -  LONG:\t\t"+  str(self.gps[3])+" degrees "+"\n"
        string+="GPS -  LONG:\t\t"+  str(self.gps[4])+" mins "+"\n"
        string+="GPS -   ALT:\t\t"+  str(self.gps[5])+" meters"+"\n"
        string+="      PHASE:\t\t"+  str(self.flightPhase)+" "+"\n"
        string+="       TICK:\t\t"+  str(self.tick)+" "+"\n"

        # with open('fligthData.csv', 'a') as csvfile:
        #     spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        #     spamwriter.writerow([str(self.imu[0]), str(self.imu[1]), str(self.imu[2]),
        #                         str(self.imu[3]), str(self.imu[4]), str(self.imu[5]),
        #                         str(self.bar[0]), str(self.bar[1]),
        #                         str(self.gps[0]), str(self.gps[1]), str(self.gps[2]),
        #                         str(self.gps[3]), str(self.gps[4]), str(self.gps[5])])
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

    while(i<len(line)):

        # check header
        # IMU Data
        if((line[i+4:i+8]=='f010')):
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
        elif((line[i:i+4])=='f011'):
            data.bar[0] = twos_complement(line[i+4:i+12], 32)
            data.bar[1] = twos_complement(line[i+12:i+20], 32)
            i+=20

        #GPS Data
        elif((line[i:i+4]=='f012')):
            data.gps[0] = twos_complement(line[i+4:i+12], 32)
            data.gps[1] = twos_complement(line[i+12:i+20], 32)
            data.gps[2] = twos_complement(line[i+20:i+28], 32)
            data.gps[3] = twos_complement(line[i+28:i+36], 32)
            data.gps[4] = twos_complement(line[i+36:i+44], 32)
            data.gps[5] = twos_complement(line[i+44:i+52], 32)
            i+=52

        # flight phase
        elif((line[i:i+4]=='f013')):
            data.flightPhase = twos_complement(line[i+4:i+12], 32)
            i+=12

        # tick
        elif((line[i:i+4]=='f014')):
            data.tick = twos_complement(line[i+4:i+12], 32)
            i+=12

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
    while(True):

        # port = input('Enter a Serial Port to connect to:') #Linux: /dev/ttyUSBx, Windows: COMx
        # radio: 57600, umbilical: 9600, debug: 115200
        ser = serial.Serial('COM3', 115200, timeout=None)
        line = b''
        while(ser!=None):
            # time.sleep(1)
            rx = ser.read()
            if (rx != b'\xf1') or (line[-1:] != b'\xf0'):
                line += rx

            print(line.hex())
            # print("ending: ", line[-2:])
            #
            # if (len(line) > 2) and (line[-2:] == b'\xf0\x01'):
            #     print(line.hex())
            #     line = b''
            #
            # if (len(line) == 250) and (line[2:] == '\x01\x01'):
            #     # espnow packet is always 250 bytes, payload data handling here
            #     print(data.__str__())


            if (len(line) > 50) and (line[-2:] == b'\xf0\xff'): # and (line[2:] == '\x02\x02')
                # print(line.hex())
                # print("---")
                readSerial(line.hex(), data)
                line = b''
                print(data.__str__())
