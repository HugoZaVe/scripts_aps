#!/usr/bin/python3

# ****** Linksys Configuration ****** #

import ipcalc
import requests
import json
import subprocess
import os.path as path
import fileinput
from getmac import get_mac_address

wlan_mac = get_mac_address(interface="wlan0").upper()
url = 'https://tufan.tunerd.mx/api/aps/show?mac_ap=' + wlan_mac
r = requests.post(url)
test = json.loads(r.text)

#Asignacion del json

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
fpool = str(max_pool)

#Variables
interface = "wlan0"

#Funciones
def createFile():
    subprocess.run(["touch", "/etc/config/data"])
    subprocess.run(["chmod", "775", "/etc/config/data"])
    file = open("/etc/config/data", 'w')
    try:
        print(file.write("test\n"))
        print(file.write("test\n"))
        print(file.write("test\n"))
        print(file.write("test\n"))
    finally:
        file.close()
    return True

def saveData():
    file = open("/etc/config/data", 'w')
    try:
        print(file.write(ip + "\n"))
        print(file.write(name_wifi + "\n"))
        print(file.write(start_list[3] + "\n"))
        print(file.write(fpool))
    finally:
        file.close()
    return True

def updateSsid():
    file = open("/etc/config/wireless", 'w')
    try:
        print(file.write("config wifi-device 'radio0'\n"))
        print(file.write("        option path 'platform/soc/a000000.wifi'\n"))
        print(file.write("        option country 'MX'\n"))
        print(file.write("        option hwmode '11g'\n"))
        print(file.write("        option type 'mac80211'\n"))
        print(file.write("        option txpower '0'\n"))
        print(file.write("        option channel '10'\n\n"))
        print(file.write("config wifi-device 'radio1'\n"))
        print(file.write("        option type 'mac80211'\n"))
        print(file.write("        option channel '36'\n"))
        print(file.write("        option hwmode '11a'\n"))
        print(file.write("        option path 'platform/soc/a800000.wifi'\n"))
        print(file.write("        option htmode 'VHT80'\n"))
        print(file.write("        option disabled '1'\n\n"))
        print(file.write("config wifi-iface 'wifinet0'\n"))
        print(file.write("        option wds '1'\n"))
        print(file.write(f"        option ssid '{name_wifi}'\n"))
        print(file.write("        option encryption 'none'\n"))
        print(file.write("        option device 'radio0'\n"))
        print(file.write("        option mode 'ap'\n"))
        print(file.write("        option network 'wlan0'\n"))
    finally:
        file.close()
    return True

def updateNetwork():
    file = open("/etc/config/network", 'w')
    try:
        print(file.write("config globals 'globals'\n"))
        print(file.write("        option ula_prefix 'fd00:26ff:4f20::/48'\n\n"))
        print(file.write("config interface 'lan'\n"))
        print(file.write("        option type 'bridge'\n"))
        print(file.write("        option ifname 'eth0'\n"))
        print(file.write("        option proto 'static'\n"))
        print(file.write("        option ipaddr '192.168.1.1'\n"))
        print(file.write("        option netmask '255.255.255.0'\n"))
        print(file.write("        option ip6assign '60'\n\n"))
        print(file.write("config device 'lan_dev'\n"))
        print(file.write("        option name 'eth0'\n"))
        print(file.write("        option macaddr '60:38:e0:91:94:c7'\n\n"))
        print(file.write("config interface 'wan'\n"))
        print(file.write("        option ifname 'eth1'\n"))
        print(file.write("        option proto 'dhcp'\n"))
        print(file.write("        option type 'bridge'\n\n"))
        print(file.write("config device 'wan_dev'\n"))
        print(file.write("        option name 'eth1'\n"))
        print(file.write("        option macaddr '60:38:e0:91:94:c6'\n\n"))
        print(file.write("config interface 'wan6'\n"))
        print(file.write("        option ifname 'eth1'\n"))
        print(file.write("        option proto 'dhcpv6'\n\n"))
        print(file.write("config interface 'loopback'\n"))
        print(file.write("        option ipaddr '127.0.0.1'\n"))
        print(file.write("        option ifname 'lo'\n"))
        print(file.write("        option netmask '255.0.0.0'\n"))
        print(file.write("        option proto 'static'\n\n"))
        print(file.write("config switch 'cfg083777'\n"))
        print(file.write("        option name 'switch0'\n"))
        print(file.write("        option enable_vlan '1'\n"))
        print(file.write("        option reset '1'\n\n"))
        print(file.write("config switch_vlan 'cfg091ec7'\n"))
        print(file.write("        option vid '1'\n"))
        print(file.write("        option device 'switch0'\n"))
        print(file.write("        option ports '0 1 2 3 4'\n"))
        print(file.write("        option vlan '1'\n\n"))
        print(file.write("config interface 'wlan0'\n"))
        print(file.write("       option proto 'static'\n"))
        print(file.write("       option netmask '255.255.255.0'\n"))
        print(file.write(f"       option ipaddr '{ip}'\n"))
    finally:
        file.close()
    return True

def updateDhcp():
    file = open("/etc/config/dhcp", 'w')
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
        print(file.write("        option ip '67.205.153.170'\n\n"))
        print(file.write("config dhcp 'wlan0'\n"))
        print(file.write(f"        option start '{start_list[3]}'\n"))
        print(file.write("        option leasetime '12h'\n"))
        print(file.write(f"        option limit '{fpool}'\n"))
        print(file.write("        option interface 'wlan0'\n"))
    finally:
       file.close()
    return True

def primaryFunction():
    file = open("/etc/config/data", 'r')
    try:
        anbu1 = file.readlines(1)[0].rstrip('\n')
        anbu2 = file.readlines(1)[0].rstrip('\n')
        anbu3 = file.readlines(1)[0].rstrip('\n')
        anbu4 = file.readlines(1)[0].rstrip('\n')

        if ip != anbu1 or name_wifi != anbu2 or start_list[3] != anbu3 or fpool != anbu4:
            updateNetwork()
            updateDhcp()
            updateSsid()
            saveData()
            subprocess.run(["reboot"])
        else:
            saveData()
    finally:
        file.close()
    return True


if path.exists('/etc/config/data'):
    primaryFunction()
else:
    createFile()
    saveData()
    primaryFunction()