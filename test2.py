import re
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
import fileinput
import sys
import netifaces
from getmac import get_mac_address



word = "ssid"
ocurrencias = []
name_wifi = "Red Sara"
name_wifi2 = "Red Sara 2"

start_pool = "'50'"

'''
with open("C:/Users/hugov/Documents/Azul School/Python Course/Wifidog/prueba.txt", "r+") as file:  
    for lines in file:
        if word in lines:
            file.write(lines.replace(word, "ssid="+name_wifi))
            ocurrencias.append(lines)
            name = ocurrencias[0]
    print(ocurrencias)
    print(type(ocurrencias))
    print(name)
    new_name = name.replace(name, "ssid="+name_wifi)
    print(new_name)
    file.close()
'''

'''
with open("C:/Users/hugov/Documents/Azul School/Python Course/Wifidog/prueba.txt", "r+") as file:
    filedata = file.readlines()
    print(filedata)
    print(type(filedata))
    
    
    for count in range(0, len(filedata)):
        if filedata[count].startswith("ssid"):
            file.write(filedata[count].replace(filedata[count], "ssid = "+name_wifi2))
            print(filedata[count])
            a = filedata[count].replace(filedata[count], "ssid = "+name_wifi2)
            print(a)
    
    file.close()
'''

'''
def replace(file, pattern, subst):
    # Read contents from file as a single string
    file_handle = open(file, 'r')
    file_string = file_handle.read()
    file_handle.close()

    # Use RE package to allow for replacement (also allowing for (multiline) REGEX)
   
    file_string = (re.sub(pattern.startswith("ssid"), subst, file_string))

    # Write contents to file.
    # Using mode 'w' truncates the file.
    file_handle = open(file, 'w')
    file_handle.write(file_string)
    file_handle.close()


replace("C:/Users/hugov/Documents/Azul School/Python Course/Wifidog/prueba.txt", "ssid", "newssid=sara")
'''

'''
for line in fileinput.input("C:/Users/hugov/Documents/Azul School/Python Course/Wifidog/prueba.txt", inplace=True):
    # Whatever is written to stdout or with print replaces
    # the current line
    if line.startswith("ssid="):
        print("ssid="+name_wifi2)
    else:
        sys.stdout.write(line)
        
'''

for line in fileinput.FileInput("C:/Users/hugov/Documents/Azul School/Python Course/Wifidog/prueba.txt", inplace=1):
    if line.startswith("        option start"):       
        new_line=line.replace(line, "        option start " + start_pool)
        print(new_line)
    else:
        print(line, end='')

newValue = "192.168.1.54"
interface = "wlan0"

with fileinput.FileInput("C:/Users/hugov/Documents/Azul School/Python Course/Wifidog/network", inplace=True) as file:
    target = False
    for line in file:
        if  not target and line.startswith(f"config interface '{interface}'"):
            target = True
        elif target and line.startswith("        option ipaddr"):
            line = f"        option ipaddr '{newValue}'"
            target = False
        print(line, end="")


'''
with open("C:/Users/hugov/Documents/Azul School/Python Course/Wifidog/prueba.txt","r") as f:
    for line in f:
        searchphrase = "config dhcp 'wlan0'"
        if searchphrase in line:
            print("found it\n")
            print (next(f)) # skip 1 line
            #print (next(f))  # and return the line after that.
'''
'''
f=open("C:/Users/hugov/Documents/Azul School/Python Course/Wifidog/prueba.txt","r")
for i,linea in enumerate(f):
  if i<5:
    continue
  print (linea)
'''

'''
def test():
    file = open("C:/Users/hugov/Documents/Azul School/Python Course/Wifidog/prueba.txt","r+")
    try:
        for line in file:
            searchphrase = "config dhcp 'wlan0'"
            if searchphrase in line:
                twophrase = "option start '100'"
                #next(file)
                if twophrase in line:
                    new_line = line.replace(line, "test")
                    print(new_line)
    finally:
        file.close()
    
test()
'''
'''


print(netifaces.interfaces())






wlan_mac = get_mac_address(interface="wlan0").upper()
print(wlan_mac)
print(type(wlan_mac))



wlan_mac = get_mac_address(interface="wlan0").upper()
print(wlan_mac)

url = 'https://tuportal.tunerd.mx/api/aps/show?mac_ap=' + wlan_mac
print(url)

#r = requests.post('https://tuportal.tunerd.mx/api/aps/show?' + wlan_mac)

r = requests.post(url)
test = json.loads(r.text)
print(test)
print(r)
print(url)
'''

#print("option ssid '" + name_wifi + "'\n\n")
#print("Hi")

#f=open("C:/Users/hugov/Documents/Azul School/Python Course/Wifidog/prueba.txt","r")
#it=(linea for i,linea in enumerate(f) if i>=2)
#for linea in it:
#  print (linea)
