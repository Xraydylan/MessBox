import sys
import os
base_path = os.path.dirname(os.path.abspath(__file__)) + "\\packages\\site-packages"
sys.path.insert(0, base_path)

import serial
import time
from datetime import datetime
try:
    import matplotlib.pyplot as plt
    mat_not_imported = False
except:
    print("================================")
    print("Warning! No matplotlib installed!")
    print("================================")
    mat_not_imported = True

# Here are the default values
port = 'COM4'
name = "data"
live_save = True

interval = 30
total = 60 * 35

cutoff = True
max_cutoff = 20


plot = True
micros = True
speed = 0.5

# ---------------------------------------------------------------


baudrate = 57600
defaults = {
    "port": port,
    "baudrate": baudrate,
    "interval": interval,
    "total": total,
    "speed": speed,
    "micros": micros,
    "plot": plot,
    "name": name,
    "live_save": live_save,
    "cutoff": cutoff,
    "max_cutoff": max_cutoff}

ser = None

def setup():
    global ser, defaults
    info = sys.argv[1:]
    for tup in info:
        if tup.__contains__("="):
            var, val = tup.split("=")
            if var in defaults:
                ty = type(defaults[var])
                try:
                    if ty == bool:
                        vals = str(val)
                        dat = vals == "True" or vals == "true" or vals == "1"
                    elif ty == int or ty == float:
                        dat = float(val)
                    else:
                        dat = str(val)
                except:
                    raise Exception("Can´t convert your input (%s) to desired type of (%s)" % (val, ty))
                defaults[var] = dat
            else:
                raise Exception("There is no changable property (%s)" % (var))
        else:
            raise Exception("Missing '='")
    globals().update(defaults)
    try:
        ser = serial.Serial(port, baudrate=baudrate, timeout=speed)
    except:
        raise Exception("Couldn´t find device.")
    time.sleep(2)

def main():
    setup()
    print("Start")
    start()
    print("Starting Measurement")
    print("Interval: %ss\nTotal: %smin" % (interval, round(total / 60, 1)))
    data = run(live_save=live_save, name=name)
    print("Completed Measurement")
    stop()

    save(data, name=name)
    if plot:
        plot_data(data)


def start():
    while 1:
        adata = ser.readline().decode('ascii').rstrip()
        if adata.rstrip() == "t":
            print("Received connection test")
            if (micros):
                send("n")
            else:
                send("m")
            adata2 = ser.readline().decode('ascii').rstrip()
            if adata2 == "r":
                print("Arduino is online")
                break
        time.sleep(0.05)


def stop():
    send("s")
    print(ser.readline().decode('ascii').rstrip())


def run(live_save=False, name="data"):
    if micros:
        c = 1000000.0
    else:
        c = 1000.0

    dataout = []

    cut_off = 5
    buffer = []
    b_len = 5

    pre = 0
    freq = 0
    t1 = datetime.now()
    T1 = datetime.now()
    no_data_counter = 0
    while 1:
        val = get_new_val()
        if cut_off:
            cut_off -= 1
        else:
            if check(val):
                no_data_counter = 0
                f = round(c / val, 4)

                if (f != pre):
                    sys.stdout.write("\rFrequency: %s" % (f))
                    sys.stdout.flush()
                pre = f

                if len(buffer) == b_len:
                    buffer.pop(0)
                    buffer.append(f)
                    freq = sum(buffer)/b_len
                else:
                    if len(buffer) > b_len:
                        print("Buffer Error")
                    buffer.append(f)
            else:
                no_data_counter += 1
                if no_data_counter > max_cutoff and cutoff:
                    print("")
                    print("Cutoff was hit.")
                    break

        if check_time(t1, interval):
            I1 = check_time(T1, interval, l=True)
            sys.stdout.write("\rSaved: %f\n" % (freq))
            sys.stdout.flush()
            t1 = datetime.now()
            dataout.append([I1[1], freq])
            if live_save:
                save(dataout, name)
        if check_time(T1, total):
            print("")
            #print(dataout)
            break
    return dataout


def check_time(t1, comp, l=False):
    t2 = datetime.now()
    delta = t2 - t1
    if delta.total_seconds() >= comp:
        if l:
            return [True, delta.total_seconds()]
        return True
    if l:
        return [False, 0]
    return False


def check(val):
    if val != "N":
        if val > 0:
            return True
    return False


def get_new_val():
    aData = ser.readline().decode('ascii').rstrip()
    if aData != "":
        return int(aData)
    else:
        return "N"


def send(val):
    global ser
    # print("Sending: %s" % val)
    ser.write(val.encode('ascii'))


def save(data, name):
    tmp = "Time,Frequency\n(s),(1/s)\n"
    for d in data:
        tmp += str(d[0]) + ", " + str(d[1]) + "\n"
    path = "out/"+ name + ".csv"
    with open(path, "w") as f:
        f.write(tmp)
    # print("Saved data as %s" % (name))


def plot_data(data):
    if mat_not_imported:
        return
    x = []
    y = []
    for d in data:
        x.append(d[0])
        y.append(d[1])

    plt.plot(x, y)
    plt.title("Dämpfung des Kreisels")
    plt.xlabel("t in s")
    plt.ylabel("f in 1/s")
    plt.show()


if __name__ == "__main__":
    main()