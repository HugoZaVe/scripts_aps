#!/usr/bin/python3

import ipcalc
import requests
import json
import subprocess
import os.path as path
import fileinput
from getmac import get_mac_address


r = requests.post('https://tuportal.tunerd.mx/api/aps/show?mac_ap=12:42:C5:02:02:0D')
#Obtención de la MAC
#wlan_mac = get_mac_address(interface="wlan0").upper()
#url = 'https://tuportal.tunerd.mx/api/aps/show?mac_ap=' + wlan_mac
#r = requests.post(url)
test = json.loads(r.text)



#Asignación del json

ip = test['ip']
mask = test['mask']
domain = test['domain']
dns_server = test['dns_server']
name = test['name']
mac_ap = test['mac_ap']
ap_name = test['ap_name']
range_start = test['range_start']
range_end = test['range_end']
name_wifi = test['name_wifi']

#Subneteo
addr = ipcalc.IP(ip, mask = mask)
network_with_cidr = str(addr.guess_network())
bare_network = network_with_cidr.split('/')[0]
bare_network_cidr = network_with_cidr.split('/')[1]

start_list = range_start.split('.')
end_list = range_end.split('.')
max_pool = abs(int(start_list[3]) - int(end_list[3]))


#Variables
interface = "wlan0"

#Funciones
def createFile():
    subprocess(["touch", "/etc/config/data"])
    subprocess(["chmod", "775", "data"])
    file = open("/etc/config/data", 'w')
    try:
        print(file.write(ip + "\n"))
        print(file.write(name_wifi + "\n"))
        print(file.write(start_list[3] + "\n"))
        print(file.write(max_pool))
    finally:
        file.close()
    return True

def saveData():
    file = open("/etc/dhcp/data", 'w')
    try:
        print(file.write(ip + "\n"))
        print(file.write(name_wifi + "\n"))
        print(file.write(start_list[3] + "\n"))
        print(file.write(max_pool))
    finally:
        file.close()
    return True

def updateSsid():
    with fileinput.FileInput("c:/Users/hugov/Documents/Azul School/Python Course/Wifidog/prueba.txt", inplace=True) as file:
        target = False
        for line in file:
            if  not target and line.startswith("config wifi-iface 'wifinet0'"):
                target = True
            elif target and line.startswith("        option ssid"):
                line = f"        option ssid '{name_wifi}'\n"
                target = False
            print(line, end="")
    return True

def updateSsidTest():
    with fileinput.input("c:/Users/hugov/Documents/Azul School/Python Course/Wifidog/prueba.txt", inplace=True) as file:
        print(type(file))
        for line in file:
            print (line)
    return True


def updateNetwork():
    with fileinput.FileInput("c:/Users/hugov/Documents/Azul School/Python Course/Wifidog/prueba.txt", inplace=True) as file:
        target = False
        for line in file:
            if  not target and line.startswith(f"config interface '{interface}'"):
                target = True
            elif target and line.startswith("        option ipaddr"):
                line = f"        option ipaddr '{ip}'"
                target = False
            print(line, end="")
    return True

def updateDhcp():
    with fileinput.FileInput("c:/Users/hugov/Documents/Azul School/Python Course/Wifidog/prueba.txt", inplace=True) as file:
        target = False
        for line in file:
            if  not target and line.startswith(f"config dhcp '{interface}'"):
                target = True
            elif target and line.startswith("        option start"):
                line = f"        option start '{start_list[3]}'\n"
                target = False
            elif  not target and line.startswith("        option limit"):
                line = f"        option start '{max_pool}'\n"
                target = False
            print(line, end="")
    return True

def mainFunction():
    file = open("/etc/dhcp/data", 'r')
    try:
        anbu1 = file.readlines(1)[0].rstrip('\n')
        anbu2 = file.readlines(1)[0].rstrip('\n')
        anbu3 = file.readlines(1)[0].rstrip('\n')
        anbu4 = file.readlines(1)[0].rstrip('\n')
        
        if ip != anbu1:
            updateNetwork()
        elif name_wifi != anbu2:
            updateSsid()
        elif start_list[3] != anbu3 or max_pool != anbu4:
            updateDhcp()
        subprocess.run(["reboot"])
    finally:
        file.close()
    return True

'''
if path.exists('/etc/config/data'):
    mainFunction()
    saveData() 
else:
    createFile()
    saveData()
    mainFunction()
'''

updateSsidTest()