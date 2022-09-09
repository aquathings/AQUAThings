import time
import requests
import math
import random
import os
import time
import glob
import RPi.GPIO as GPIO
from DS18B20 import sensor,readSuhu
from ultra import distance
from servo import pakan

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

TOKEN = "BBFF-fOBpYuxMljGnFrL2x5FiyuUMA4ewon"  # Put your TOKEN here
DEVICE_LABEL = "aquathings"  # Put your device label here
# api=ApiClient(TOKEN)
# variable=api.get_variable("6314282ac68a7f000e8d8efe")
VARIABLE_LABEL_1 = "suhuair"  # Put your first variable label here
VARIABLE_LABEL_2 = "ketinggianair"  # Put your second variable label here
VARIABLE_LABEL_3 = "jam1"
VARIABLE_LABEL_4 = "jam2"
VARIABLE_LABEL_5 = "menit1"
VARIABLE_LABEL_6 = "menit2"
VARIABLE_LABEL_7 = "LED"

TIMER1 = 0
TIMER2 = 0


def build_payload(variable_1, variable_2,variable_3,variable_4,variable_5,variable_6,variable_7,serialNum):
    suhuair = readSuhu(serialNum)
    dist = distance()
    
    if suhuair < 25:
        print("heater nyala")
        
    else:
        print("heater mati")
        
    #----------------------------------------------------
    print ("Ketinggian Air = %.1f cm" % dist)
    print ("Suhu Air = %.1f C" % suhuair)
    if suhuair != None :
        if suhuair != 0:
            #anget(suhuair)
            payload = {variable_1: suhuair,
                       variable_2: dist,
                       variable_7:"led"
                      }
        else:
            payload = {variable_1: 0,
                       variable_2: 0
                      }
        #------------------------------------------------------
       
    return payload


def get_request(buka,varjam,varmenit):
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}/{}/lv".format(url, DEVICE_LABEL, varjam)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.get(url=url, headers=headers)
        status = req.status_code
        attempts += 1
        if status != 200:
            time.sleep(1)
    jam_1 = int(float(req.text))
    
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}/{}/lv".format(url, DEVICE_LABEL, varmenit)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.get(url=url, headers=headers)
        status = req.status_code
        attempts += 1
        if status != 200:
            time.sleep(1)
    menit_1=int(float(req.text))

    jamsekarang1=int(time.strftime("%H"))
    menitsekarang1=int(time.strftime("%M"))


    if jamsekarang1 == jam_1 and menitsekarang1 == menit_1:
        if buka < 1:
            pakan(0.3)
            print("Buka Pakan")
        buka+=1
    else:
        buka=0
    return buka
        


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)


    # Processes results
    #print(req.status_code, req.json())
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    
    print("[INFO] Data diperbarui")
    return True


def main(serialNum):

    payload = build_payload(VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3, VARIABLE_LABEL_4, VARIABLE_LABEL_5, VARIABLE_LABEL_6, VARIABLE_LABEL_7, serialNum)

    #print("[INFO] Attemping to send data")

    if payload['suhuair'] != 0 :
        post_request(payload)
        #print("[INFO] finished")

    else:
        print("[INFO] sensor suhu tidak terbaca")
        

if __name__ == '__main__':
    serialNum = sensor()
    try:
        while (True):
            main(serialNum)
            TIMER1 = get_request(TIMER1, VARIABLE_LABEL_3, VARIABLE_LABEL_5)
            TIMER2 = get_request(TIMER2, VARIABLE_LABEL_4, VARIABLE_LABEL_6)
            time.sleep(5)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
