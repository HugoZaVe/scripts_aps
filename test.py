
import ipcalc
import requests
import json
import subprocess
import os.path as path
import fileinput
import sys
import netifaces


#r = requests.post('http://tuwrt.tunerd.mx/api/aps/show?mac_ap=2c:4d:54:42:f7:c3', data = {'key':'value'})

r = requests.post('https://tuportal.tunerd.mx/api/aps/show?mac_ap=12:42:C5:02:02:0D')

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

addr = ipcalc.IP(ip, mask = mask)
network_with_cidr = str(addr.guess_network())
bare_network = network_with_cidr.split('/')[0]
bare_network_cidr = network_with_cidr.split('/')[1]


#Definición de funciones

def saveData():
    file_data = open("etc/dhcp/data", 'w')
    try:
        print(file_data.write(ip + "\n"))
        print(file_data.write(mask + "\n"))
        print(file_data.write(domain + "\n"))
        print(file_data.write(dns_server + "\n"))
        print(file_data.write(range_start + "\n"))
        print(file_data.write(range_end + "\n"))
        print(file_data.write(name_wifi))
        
    finally:
        file_data.close()
    return True

def updateDhcpd():
    file = open("etc/dhcp/dhcpd.conf", 'w')
    try:
        print(file.write("ddns-update-style none;\n"))
        print(file.write("option domain-name \"" + domain +  "\";\n"))
        print(file.write("option domain-name-servers "  + dns_server + ";\n\n"))

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
    #file = open("C:/Users/hugov/Documents/interfaces", 'w')
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
    for line in fileinput.FileInput("C:/Users/hugov/Documents/Azul School/Python Course/Wifidog/prueba.txt", inplace=1):
        if line.startswith("ssid="):
            new_line=line.replace(line, "ssid=" + name_wifi)
            print(new_line)
        else:
            print(line, end='')
    return True
# Comienza el programa

if path.exists('etc/dhcp/data'):
    print("El archivo ya existe\n")
    file_data = open("etc/dhcp/data", 'r')
    try:
        t1 = file_data.readlines(1)[0].rstrip('\n')
        t2 = file_data.readlines(1)[0].rstrip('\n')
        t3 = file_data.readlines(1)[0].rstrip('\n')
        t4 = file_data.readlines(1)[0].rstrip('\n')
        t5 = file_data.readlines(1)[0].rstrip('\n')
        t6 = file_data.readlines(1)[0].rstrip('\n')
        t7 = file_data.readlines(1)[0].rstrip('\n')

        if ip != t1 or mask != t2 or domain != t3 or dns_server != t4 or range_start != t5 or range_end != t6:
            #print("Los valores han cambiado, reiniciar los servicios")
            updateDhcpd()
            subprocess.run(["sudo", "ip", "link", "set", "wlan0", "down"])
            updateInterfaces()
            subprocess.run(["sudo", "ip", "address", "add", ip+"/" + bare_network_cidr ,"dev", "wlan0"])
            subprocess.run(["sudo", "service", "NetworkManager", "restart"])
            subprocess.run(["sudo", "ip", "link", "set", "wlan0", "up"])
            subprocess.run(["sudo", "service", "isc-dhcp-server", "restart"])
            saveData()
            
        elif name_wifi != t7:
            #print("El nombre la red ha sido actualizado")
            updateHostapd()
            subprocess.run(["sudo", "systemctl", "restart", "hostapd"])
            subprocess.run(["sudo", "service", "NetworkManager", "restart"])
            subprocess.run(["sudo", "service", "isc-dhcp-server", "restart"])

    finally:
        file_data.close()
else:
    saveData()