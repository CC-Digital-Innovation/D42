#!/usr/bin/env python3

import ast
import csv
import json
from queue import Empty
from tkinter.font import names
import requests
import pandas as pd
import urllib3

##disables warning for unverified HTTPS (url)
urllib3.disable_warnings()

#url = 'https://10.201.10.198/api/1.0/devices/all/'
url = 'https://swaggerdemo.device42.com/api/1.0/devices/all/'
username = 'guest'
password = 'device42_rocks!'
headers = {
            'Content-Type': 'application/json'
        }

r = requests.request("GET", url, auth=(username, password), headers=headers, verify=False)
dictionary = json.loads(r.text)

#---------------------------------------------------------------------------------------------
##Device name is 'Name'
#if dictionary is Empty:
deviceNames = []
for e in range(len(dictionary.get('Devices'))):
    deviceNames.append(dictionary.get('Devices')[e]['name'])
        
#print(deviceNames)

#---------------------------------------------------------------------------------------------
## [NEEDS TESTING IN VERIZON]
# Device location is 'Location' **SHOULD ONLY WORK IN VERIZON BOX NOT IN SANDBOX**
#if dictionary is Empty:
locations = []
i = 0

for e in dictionary['Devices'][:]:
    if 'custom_fields' in e:
        for x in e['custom_fields']:
           if 'hdd_details' in x:
               locations.append(dictionary.get('Devices')[x].get('location'))
           elif 'location' not in x:
                locations.append(None)
    i=i+1
'''
for e in range(len(dictionary.get('Devices'))):
    locations.append('')
'''
'''
for e in range(len(dictionary.get('Devices'))):
    if len(dictionary.get('Devices')[e]['location']) == 0:
        locations.append('')
    else:
        locations.append(dictionary.get('Devices')[e]['location'])
            
    #print(locations)
'''
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

#print(service_levels)

#---------------------------------------------------------------------------------------------
## [MISSING]? set to default 'Installed'
## Status
##Status in ServiceNow is ____ in Verizon_Box? I don't see it.
#if dictionary is Empty:
statuses = []
#if dictionary is Empty:
for e in range(len(dictionary.get('Devices'))):
    statuses.append('Installed')
    #print(statuses)
#---------------------------------------------------------------------------------------------
## [MISSING]? set to default 'Storage Device'
##Class in ServiceNow is ____ in Verizon_Box? IDK.
#if dictionary is Empty:
classes = []
for e in range(len(dictionary.get('Devices'))):
    classes.append('Storage Device')
'''
    if dictionary is Empty:
        for e in range(len(dictionary.get('Devices'))):
            classes.append('Storage Device')
        print(classes)
'''
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
    if 'custom_fields' in e:
        for x in e['custom_fields']:
           if 'manufacturer' in x:
               manufacturer[i].append(x['manufacturer'])
           elif 'manufacturer' not in x:
                manufacturer[i].append(None)
    i=i+1

for e in range(len(dictionary.get('Devices'))):
    manufacturer.append('')
'''
    for e in range(len(dictionary.get('Devices'))):
        if dictionary.get('Devices')[e]['manufacturer'] is None:
            manufacturer.append('')
        else:
            manufacturer.append(dictionary.get('Devices')[e]['manufacturer'])

    print(manufacturer)
'''

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
ip_addresses = [[] for i in range(len(dictionary['Devices'][:]))]
i = 0
print(len(ip_addresses))
print(len(dictionary['Devices'][:]))
for e in dictionary['Devices'][:]:
    if 'ip_addresses' in e:
        for x in e['ip_addresses']:
           ip_addresses[i].append(x['ip'])
           #if len(x) in e['ip_addresses'] == 0:
           #    ip_addresses[i].append(None)
    i=i+1

#---------------------------------------------------------------------------------------------
## Host Name [Configuration Item] in ServiceNow is 'virtual_host_name' in Verizon_Box (I think?)
#if dictionary is Empty:
virtual_host_names = []
for e in range(len(dictionary.get('Devices'))):
    if dictionary.get('Devices')[e]['virtual_host_name'] is None:
        virtual_host_names.append(None)
    else:
        virtual_host_names.append(dictionary.get('Devices')[e]['virtual_host_name'])
#print(virtual_host_names)

#---------------------------------------------------------------------------------------------
## Serial number in ServiceNow is 'serial_no' in Verizon_Box
#if dictionary is Empty:
serial_numbers = []
for e in range(len(dictionary.get('Devices'))):
    if dictionary.get('Devices')[e]['serial_no'] is None:
        serial_numbers.append(None)
    else:
        serial_numbers.append(dictionary.get('Devices')[e]['serial_no'])
#print(serial_numbers)

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

#---------------------------------------------------------------------------------------------
## [NOT WORKING; NEEDS TESTING IN VERIZON]
## 'Description [Configuration Item]' in ServiceNow is 'description' in Verizon_Box
## Needs to be coded in Verizon_Box since D42 sandbox is not giving proper output.
## Test in the box and parse hdd_details to get description or it might retrieve from just Devices than hdd_details
#if dictionary is Empty:
descriptions = []
for e in range(len(dictionary.get('Devices'))):
    descriptions.append('')

'''
    #print(type(dictionary.get('Devices')[0]['hdd_details']))
    for e in range(len(dictionary.get('Devices'))):
        if dictionary.get('Devices')[e]['hdd_details'] is None:
            descriptions.append(None)
        else:
            descriptions.append(dictionary.get('Devices')[e].get('hdd_details')) #Needs to retrieve description after 'hdd_details'
    print(descriptions)
'''

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
device_sub_type = []
for e in range(len(dictionary.get('Devices'))):
    if 'virtual_subtype' not in dictionary.get('Devices')[e]:
        device_sub_type.append(None)
    else:
        device_sub_type.append(dictionary.get('Devices')[e]['virtual_subtype'])

'''
    for e in range(len(dictionary.get('Devices'))):
        if 'virtual_subtype' not in dictionary.get('Devices')[e]:
            device_sub_type.append(None) 
            #or device_sub_type.append('')
        else:
            device_sub_type.append(dictionary.get('Devices')[e]['virtual_subtype'])

    print(device_sub_type)
'''
#---------------------------------------------------------------------------------------------

# 16/17 working properly (test in Verizon: description(unsure, test it), add(notes? *optional*), and manufacturer(working))
CMDB_Items = ['Name', 
              'Location', 
              'Used for [Configuration Item]', 
              'Status',                               #Set to 'Installed'
              'Class',                                #Set to 'Storage Device'
              'CC Type [Configuration Item]',         #IGNORED IN CODE
              'Manufacturer', 
              'Model number [Configuration Item]', 
              'IP Address [Configuration Item',       
              'Host Name [Configuration Item]', 
              'Serial number', 
              'MAC Address [Configuration Item]',     
              'Description [Configuration Item]',     #In Verizon
              'Username [Configuration Item]',        #IGNORED IN CODE
              'FS Password [Configuration Item]',     #IGNORED IN CODE
              'Active Contract [Configuration Item]', #Always 'True'
              'Physical Subtype'                      #In Verizon
              ]



CMDB_Data = list(zip(deviceNames, 
                     locations, 
                     service_levels, 
                     statuses, 
                     classes,  
                     cc_types, 
                     manufacturer, 
                     model_numbers, 
                     ip_addresses, 
                     virtual_host_names, 
                     serial_numbers, 
                     mac_addresses, 
                     descriptions,
                     usernames,
                     fs_passwords,
                     active_contract,
                     device_sub_type
                     ))

with open('testD42_Data.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the headers
    writer.writerow(CMDB_Items)
    # write the rows
    for data in CMDB_Data:
        writer.writerow(data)