import sys
import os
base_path = os.path.dirname(os.path.abspath(__file__)) + "\\packages\\site-packages"
sys.path.insert(0, base_path)
import serial
import time

port = "COM4"

arg = sys.argv[1:]

if arg != []:
    port = arg[0]

print("Testing Port: %s" % (port))

baudrate = 57600
ser = None
try:
    ser = serial.Serial(port, baudrate=baudrate, timeout=0.5)
except:
    raise Exception("Couldn´t find device.")

time.sleep(2)

print("Test active")

while 1:
    adata = ser.readline().decode('ascii').rstrip()
    if adata.rstrip() == "t":
        print("Received connection test")
        val = "c"
        ser.write(val.encode('ascii'))
        adata2 = ser.readline().decode('ascii').rstrip()
        if adata2 == "c":
            print("Arduino is online")
            break
    time.sleep(0.05)
