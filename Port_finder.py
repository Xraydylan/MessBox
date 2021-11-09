# coding: utf-8

import sys
import os
base_path = os.path.dirname(os.path.abspath(__file__))
serial_path = base_path + "\packages\site-packages"
sys.path.insert(0, serial_path)
import serial.tools.list_ports
import serial

ports = serial.tools.list_ports.comports()

out = ""
for port, desc, hwid in sorted(ports):
    out += "{}: {} [{}]".format(port, desc, hwid) + "\n"

if out == "":
    print("No availabe ports...")
else:
    print(out)