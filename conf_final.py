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

def updateSsid():
    file = open("/etc/network/wireless", 'w')
    try:
        print(file.write("config dhcp 'lan'\n"))
        print(file.write("        option interface 'lan'\n"))
        print(file.write("        option dhcpv6 'server'\n"))
        print(file.write("        option ra 'server'\n"))
        print(file.write("        option ra_management '1'\n"))
        print(file.write("        option ignore '1'\n\n"))
        print(file.write("config dhcp 'wan'\n"))
        print(file.write("        option interface 'wan'\n"))
        print(file.write("        option ignore '1'\n\n"))
        print(file.write("config dhcp 'vlan10'\n"))
        print(file.write("        option start '100'\n"))
        print(file.write("        option leasetime '12h'\n"))
        print(file.write("        option limit '150'\n"))
        print(file.write("        option interface 'vlan10'\n"))
        print(file.write("        option dynamicdhcp '0'\n"))
        print(file.write("        option force '1'\n\n"))
        print(file.write("config odhcpd 'odhcpd'\n"))
        print(file.write("        option maindhcp '0'\n"))
        print(file.write("        option leasefile '/tmp/hosts/odhcpd'\n"))
        print(file.write("        option leasetrigger '/usr/sbin/odhcpd-update'\n"))
        print(file.write("        option loglevel '4'\n\n"))
        print(file.write("config dnsmasq 'cfg01411c'\n"))
        print(file.write("        option readethers '1'\n"))
        print(file.write("        option expandhosts '1'\n"))
        print(file.write("        option boguspriv '1'\n"))
        print(file.write("        option localise_queries '1'\n"))
        print(file.write("        option nonegcache '0'\n"))
        print(file.write("        option nonwildcard '1'\n"))
        print(file.write("        option resolvfile '/tmp/resolv.conf.auto'\n"))
        print(file.write("        option rebind_localhost '1'\n"))
        print(file.write("        option domain 'lan'\n"))
        print(file.write("        option localservice '1'\n"))
        print(file.write("        option rebind_protection '1'\n"))
        print(file.write("        option filterwin2k '0'\n"))
        print(file.write("        option local '/lan/'\n"))
        print(file.write("        option authoritative '1'\n"))
        print(file.write("        option domainneeded '1'\n"))
        print(file.write("        option leasefile '/tmp/dhcp.leases'\n\n"))
        print(file.write("config domain\n"))
        print(file.write("        option name 'tufan.tunerd.mx'\n"))
        print(file.write("        option ip '192.168.0.67'\n\n"))
        print(file.write("config domain\n"))
        print(file.write("        option name 'tuportal.tunerd.mx'\n"))
        print(file.write("        option ip '67.205.153.170'\n\n"))
        print(file.write("config dhcp 'wlan0'\n"))
        print(file.write(f"        option start '{start_list[3]}'\n"))
        print(file.write("        option leasetime '12h'\n"))
        print(file.write(f"        option limit '{max_pool}'\n"))
        print(file.write("        option interface 'wlan0'\n"))