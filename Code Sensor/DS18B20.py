import os
import time
import glob

def sensor():
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            ds18b20 = i
    return ds18b20

def readSuhu(ds18b20):
    temperature = 0.0
    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    if(len(text) >  0):
        secondline = text.split("\n")[1]
        #print(len(secondline))
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
    celsius = temperature / 1000
    farenheit = (celsius * 1.8) + 32
    return celsius

# def loop(ds18b20):
#     while True:
#         if readSuhu(ds18b20) != None:
#             print ("%0.3f C" % readSuhu(ds18b20))
# 
# def kill():
#     quit()
# 
# if __name__ == '__main__':
#     temperature = 0
#     try:
#         serialNum = sensor()
#         loop(serialNum)
#     except KeyboardInterrupt:
#         kill()