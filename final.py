#!/usr/bin/python3

import ipcalc
import requests
import json
import subprocess
import os.path as path
import fileinput
from getmac import get_mac_address

wlan_mac = get_mac_address(interface="wlan0").upper()
url = 'https://tuportal.tunerd.mx/api/aps/show?mac_ap=' + wlan_mac


#r = requests.post('https://tuportal.tunerd.mx/api/aps/show?mac_ap=12:42:C5:02:02:0D')
r = requests.post(url)
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

#Funciones

#Funciones

def saveData():
    file = open("/etc/dhcp/data", 'w')
    try:
        print(file.write(ip + "\n"))
        print(file.write(mask + "\n"))
        print(file.write(domain + "\n"))
        print(file.write(dns_server + "\n"))
        print(file.write(range_start + "\n"))
        print(file.write(range_end + "\n"))
        print(file.write(name_wifi))
    finally:
        file.close()
    return True

def updateDhcpd():
    file = open("/etc/dhcp/dhcpd.conf", 'w')
    try:
        print(file.write("ddns-update-style none;\n"))
        print(file.write("option domain-name \"" + domain + "\";\n"))
        print(file.write("option domain-name-servers " + dns_server + ";\n\n"))
        print(file.write("default-lease-time 600;\n"))
        print(file.write("max-lease-time 7200;\n\n"))
        print(file.write("authoritative;\n\n"))
        print(file.write("subnet " + bare_network + " netmask " + mask + " {\n"))
        print(file.write("  range " + range_start + " " + range_end + ";\n"))
        print(file.write("  option routers " + ip + ";\n"))
        print(file.write("}"))
    finally:
        file.close()
    return True

def updateInterfaces():
    file = open("/etc/network/interfaces", 'w')
    try:
        print(file.write("source-directory /etc/network/interfaces.d\n\n"))
        print(file.write("allow-hotplug wlan0\n"))
        print(file.write("iface wlan0 inet static\n"))
        print(file.write("  address " + ip + "\n"))
        print(file.write("  netmask " + mask + "\n"))
    finally:
        file.close()
    return True

def updateHostapd():
    file = open("/etc/hostapd/hostapd.conf", 'w')
    try:
        print(file.write("interface=wlan0\n"))
        print(file.write("ssid="+ name_wifi + "\n"))
        print(file.write("hw_mode=g\n"))
        print(file.write("channel=6\n"))
        print(file.write("ieee80211n=1\n"))
        print(file.write("wmm_enabled=1"))
        print("Se cambio el nombre de la red")
    finally:
        file.close()
    return True

#Comienza el programa

if path.exists('/etc/dhcp/data'):
    file = open("/etc/dhcp/data", 'r')
    try:
        t1 = file.readlines(1)[0].rstrip('\n')
        t2 = file.readlines(1)[0].rstrip('\n')
        t3 = file.readlines(1)[0].rstrip('\n')
        t4 = file.readlines(1)[0].rstrip('\n')
        t5 = file.readlines(1)[0].rstrip('\n')
        t6 = file.readlines(1)[0].rstrip('\n')
        t7 = file.readlines(1)[0].rstrip('\n')

        if ip != t1 or mask != t2 or domain != t3 or dns_server != t4 or range_start != t5 or range_end != t6 or name_wifi != t7:
            updateHostapd()
            updateDhcpd()
            subprocess.run(["sudo", "ip", "link", "set", "wlan0", "down"])
            updateInterfaces()
            subprocess.run(["sudo", "ip", "addr", "flush", "dev", "wlan0"])
            subprocess.run(["sudo", "ip", "address", "add", ip + "/" + bare_network_cidr, "dev", "wlan0"])
            subprocess.run(["sudo", "service", "NetworkManager", "restart"])
            subprocess.run(["sudo", "ip", "link" , "set", "wlan0", "up"])
            subprocess.run(["sudo", "service", "isc-dhcp-server", "restart"])
            subprocess.run(["sudo", "systemctl", "restart", "hostapd"])
            saveData()
            subprocess.run(["sudo", "systemctl", "restart", "wifidog.service"])
            subprocess.run(["sudo", "shutdown", "-r"])
            #elif name_wifi != t7:
            #updateHostapd()
            #subprocess.run(["sudo", "systemctl", "restart", "hostapd"]
    finally:
        file.close()
else:
    saveData()