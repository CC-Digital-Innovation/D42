#!/usr/bin/env python3

import ast
import csv
import json
from queue import Empty
from tkinter.font import names
import requests
import pandas as pd
import urllib3
import logging

##disables warning for unverified HTTPS (url)
urllib3.disable_warnings()

url = 'https://134.71.163.233/api/1.0/devices/all/'
'''
#url = 'https://swaggerdemo.device42.com/api/1.0/devices/all/'
username = 'guest'
password = 'device42_rocks!'
headers = {
            'Content-Type': 'application/json'
        }
'''

##disables warning for unverified HTTPS (url)
urllib3.disable_warnings()

url = 'https://134.71.163.233/api/1.0/devices/all/'
username = 'admin'
password = 'kXAkqKiMwyIxUk#gpfXuymz7yRYthmuJWUs!'
headers = {
            'Content-Type': 'application/json'
        }


r = requests.request("GET", url, auth=(username, password), headers=headers, verify=False)
dictionary = json.loads(r.text)
print(dictionary)
#---------------------------------------------------------------------------------------------    
##Device name is 'Name'
deviceNames = []
for e in range(len(dictionary.get('Devices'))):
    deviceNames.append(dictionary.get('Devices')[e]['name'])
#---------------------------------------------------------------------------------------------
device_IDs = [[] for i in range(len(dictionary['Devices'][:]))]
i = 0

for e in dictionary['Devices'][:]:
    if 'id' in e:
        device_IDs[i].append(e['id'])
    elif 'id' not in e:
        device_IDs[i].append(None)
    i=i+1  

locations = [[] for i in range(len(dictionary['Devices'][:]))]
i = 0

for e in dictionary['Devices'][:]:
    if 'location' in e:
        locations[i].append(e['location'])
    elif 'location' not in e:
        locations[i].append(None)
    i=i+1  
#---------------------------------------------------------------------------------------------

##Used For [Configuration Item] --> not in Verizon_Box, entered Manually ex.: 'Production' as the value
##BUT, it's probably 'service_level'
#if dictionary is Empty:
service_levels = []
for e in range(len(dictionary.get('Devices'))):
    if dictionary.get('Devices')[e]['service_level'] is None:
            service_levels.append('')
    else:
        service_levels.append(dictionary.get('Devices')[e]['service_level'])

#---------------------------------------------------------------------------------------------

## [MISSING]? set to default 'Installed'
## Status
##Status in ServiceNow is ____ in Verizon_Box? I don't see it.
#if dictionary is Empty:
statuses = []
#if dictionary is Empty:
for e in range(len(dictionary.get('Devices'))):
    statuses.append('Installed')

#---------------------------------------------------------------------------------------------

## [MISSING]? set to default 'Storage Device'
##Class in ServiceNow is ____ in Verizon_Box? IDK.
#if dictionary is Empty:
classes = []
for e in range(len(dictionary.get('Devices'))):
    classes.append('Storage Device')

#---------------------------------------------------------------------------------------------

## 'CC Type' not in Verizon_Box
cc_types = []
for e in range(len(dictionary.get('Devices'))):
    cc_types.append('')

#---------------------------------------------------------------------------------------------

## [WORKING] NEED TO TEST
## 'Manufacturer' in ServicenNow is 'manufacturer' in Verizon_Box
##will not pull correctly, must be more nested...
#if dictionary is Empty:
manufacturer = [[] for i in range(len(dictionary['Devices'][:]))]
i = 0

for e in dictionary['Devices'][:]:
    if 'manufacturer' in e:
        manufacturer[i].append(e['manufacturer'])
    elif 'manufacturer' not in e:
        manufacturer[i].append(None)
    i=i+1

#---------------------------------------------------------------------------------------------

## 'Model Number [Configuration Item]' in ServiceNow is Hardware Model 'hw_model' in Verizon_Box
#if dictionary is Empty:
model_numbers = []
for e in range(len(dictionary.get('Devices'))):
    if dictionary.get('Devices')[e]['hw_model'] is None:
        model_numbers.append(None)
    else:
        model_numbers.append(dictionary.get('Devices')[e]['hw_model'])

#---------------------------------------------------------------------------------------------

## [WORKING]
## 'IP Address [Configuration Item]' in ServiceNow is 'IP Address' in Verizon_Box GUI (not in the output.txt)
## using temporarily subnet or 'ip' since it's the closest to the IP Address, but missing part of it...
#if dictionary is Empty:
ip_addr = [[] for i in range(len(dictionary['Devices'][:]))]
i = 0

for e in dictionary['Devices'][:]:
    if 'ip_addresses' in e:
        for x in e['ip_addresses']:
            ip_addr[i].append(x['ip'])
    i=i+1

ip_addresses = []
for values in ip_addr:
    if len(values) == 0:
        ip_addresses.append("")
    else:
        ip_addresses.append(values[0])
#---------------------------------------------------------------------------------------------

## Host Name [Configuration Item] in ServiceNow is 'virtual_host_name' in Verizon_Box (I think?)
#if dictionary is Empty:
virtual_host_names = []
for e in range(len(dictionary.get('Devices'))):
    if dictionary.get('Devices')[e]['virtual_host_name'] is None:
        virtual_host_names.append(None)
    else:
        virtual_host_names.append(dictionary.get('Devices')[e]['virtual_host_name'])

#---------------------------------------------------------------------------------------------

## Serial number in ServiceNow is 'serial_no' in Verizon_Box
#if dictionary is Empty:
serial_numbers = []
for e in range(len(dictionary.get('Devices'))):
    if dictionary.get('Devices')[e]['serial_no'] is None:
        serial_numbers.append(None)
    else:
        serial_numbers.append(dictionary.get('Devices')[e]['serial_no'])

#---------------------------------------------------------------------------------------------

## [WORKING]
## HWAddress (macaddress) belongs to 'MAC Address [Configuration Item]' in CSV file
##Needs to filter tuples, works currently for Empty and dictionaries.
#if dictionary is Empty:
mac_addresses = [[] for i in range(len(dictionary['Devices'][:]))]
i = 0

for e in dictionary['Devices'][:]:
    if 'ip_addresses' in e:
        for x in e['ip_addresses']:
            if 'macaddress' in x:
                mac_addresses[i].append(x['macaddress'])
            elif 'macaddress' not in x:
                    mac_addresses[i].append(None)
    i=i+1

mac_address = []
for values in mac_addresses:
    if len(values) == 0:
        mac_address.append("")
    else:
        mac_address.append(values[0])
'''
for e in len(mac_addresses):
    newLst.append(mac_addresses[e][0])

mac_addresses = newLst
'''

        

#---------------------------------------------------------------------------------------------

## [WORKING]
## 'Description [Configuration Item]' in ServiceNow is 'description' in Verizon_Box
## Needs to be coded in Verizon_Box since D42 sandbox is not giving proper output.
## Test in the box and parse hdd_details to get description or it might retrieve from just Devices than hdd_details
#if dictionary is Empty:
descriptions = [[] for i in range(len(dictionary['Devices'][:]))]
i = 0

for e in dictionary['Devices'][:]:
    if 'description' in e:
        descriptions[i].append(e['description'])
    elif 'description' not in e:
        descriptions[i].append(None)
    i=i+1

#---------------------------------------------------------------------------------------------

## Username [IGNORED, manually entered]
usernames = []
for e in range(len(dictionary.get('Devices'))):
    usernames.append('')

#---------------------------------------------------------------------------------------------

## Password [IGNORED, manually entered]
fs_passwords = []
for e in range(len(dictionary.get('Devices'))):
    fs_passwords.append('')

#---------------------------------------------------------------------------------------------

## 'Active Contract [Configuration Item]' in ServiceNow is not in Verizon_Box
## Always True
## [WORKING PROPERLY]
#if dictionary is Empty:
active_contract = []
for e in range(len(dictionary.get('Devices'))):
    active_contract.append(True)
    #print(len(active_contract))

#---------------------------------------------------------------------------------------------

## [WORKING] Physical subtype (device_sub_type) in Verizon_Box is ____ in ServiceNow? Idk.
##D42 sandbox is called (virtual_subtype)
#if dictionary is Empty:
device_sub_type = [[] for i in range(len(dictionary['Devices'][:]))]
i = 0

for e in dictionary['Devices'][:]:
    if 'device_sub_type' in e:
        device_sub_type[i].append(e['device_sub_type'])
    elif 'device_sub_type' not in e:
        device_sub_type[i].append(None)
    i=i+1

#---------------------------------------------------------------------------------------------
# 'rack' is 'location' but for now default and hardcode to 'Location'
# which will then be read and replaced by a location that will be
# posted to ServiceNow/D42
rack_locations = []
for e in range(len(dictionary.get('Devices'))):
    rack_locations.append('Location')
'''
rack_locations = [[] for i in range(len(dictionary['Devices'][:]))]

i = 0

for e in dictionary['Devices'][:]:
    if 'rack' in e:
        rack_locations[i].append(e['rack'])
    elif 'rack' not in e or 'rack' == Empty:
        rack_locations[i].append("")
    i=i+1
'''
#---------------------------------------------------------------------------------------------

# 'customer'
customers = [[] for i in range(len(dictionary['Devices'][:]))]
i = 0

for e in dictionary['Devices'][:]:
    if 'customer' in e:
        customers[i].append(e['customer'])
    elif 'customer' not in e:
        customers[i].append("")
    i=i+1

#---------------------------------------------------------------------------------------------

discovery_source = []
for e in range(len(dictionary.get('Devices'))):
    discovery_source.append('Device42')

#---------------------------------------------------------------------------------------------


# [WORKING]
CMDB_Items = [
            'ID',
            'Name', 
            'Customer', 
            'Location', 
            'Used for [Configuration Item]', 
            'Status',                               #Set to 'Installed'
            'Class',                                #Set to 'Storage Device'
            'CC Type [Configuration Item]',         #IGNORED
            'Manufacturer', 
            'Model number [Configuration Item]', 
            'IP Address [Configuration Item',       
            'Host Name [Configuration Item]', 
            'Serial number', 
            'MAC Address [Configuration Item]',     
            'Description [Configuration Item]',     
            'Username [Configuration Item]',        #IGNORED
            'FS Password [Configuration Item]',     #IGNORED
            'Active Contract [Configuration Item]', #Always 'True'
            'Physical Subtype',
            'Discovery Source'
            ]

CMDB_Data = list(zip(device_IDs,
                    deviceNames, 
                    customers,
                    rack_locations, 
                    service_levels, 
                    statuses, 
                    classes,  
                    cc_types, 
                    manufacturer, 
                    model_numbers, 
                    ip_addresses, 
                    virtual_host_names, 
                    serial_numbers, 
                    mac_address, 
                    descriptions,
                    usernames,
                    fs_passwords,
                    active_contract,
                    device_sub_type,
                    discovery_source
                    ))

with open('testD42_Data.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the headers
    writer.writerow(CMDB_Items)
    # write the rows
    for data in CMDB_Data:
        writer.writerow(data)

# Removes all unnecessary chars/symbols from csv file
# reading the CSV file
text = open("testD42_Data.csv", "r")

#join() method combines all contents of 
# csvfile.csv and formed as a string
text = ''.join([i for i in text]) 

# search and replace the contents
text = text.replace("[None]", "") 
text = text.replace("[]", "") 
text = text.replace("[", "") 
text = text.replace("]", "") 
text = text.replace(f"[\'", "")
text = text.replace(f"\']", "")
text = text.replace(f"\'", "")

# testD42_Data.csv is the output file opened in write mode
x = open("testD42_Data.csv","w")

# all the replaced text is written in the output.csv file
x.writelines(text)
x.close()
