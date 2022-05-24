#!/usr/bin/env python3

import ast
import csv
import json
from queue import Empty
from tkinter.font import names
from unittest import skipIf
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
##Device location is 'Location' **SHOULD ONLY WORK IN VERIZON BOX NOT IN SANDBOX**
#if dictionary is Empty:
locations = []
for e in range(len(dictionary.get('Devices'))):
    locations.append('')
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
## 'Manufacturer' in ServicenNow is 'manufacturer' in Verizon_Box
##will not pull correctly, must be more nested...
#if dictionary is Empty:
    manufacturer = []
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
## [NOT WORKING]
## 'IP Address [Configuration Item]' in ServiceNow is 'IP Address' in Verizon_Box GUI (not in the output.txt)
## using temporarily subnet or 'ip' since it's the closest to the IP Address, but missing part of it...
#if dictionary is Empty:
ip_addresses = []
print(dictionary.get('Devices')[0]['ip_addresses'][0].get('ip'))
print(len(dictionary.get('Devices')[-1]['ip_addresses'][-1]))

for e in range(len(dictionary.get('Devices'))):
    #ip_addresses.append('x.x.x.x.x')

    '''if 'last_updated' in dictionary.get('Devices')[e].keys() and 'ip' not in dictionary.get('Devices')[e]['ip_addresses'][e].keys():
        ip_addresses.append('')'''
    if 'ip_addresses' in dictionary.get('Devices')[e] is None:
        ip_addresses.append('')
    elif 'ip' in dictionary.get('Devices')[e]['ip_addresses'][e].keys():
        ip_addresses.append(dictionary.get('Devices')[e]['ip_addresses'][e].get('ip'))

print(ip_addresses)


'''
    for e in range(len(dictionary.get('Devices'))):
        if dictionary.get('Devices')[e]['ip_addresses']: #If this works then the addresses will append properly.
            ip_addresses.append(None) 
            #or ip_addresses.append('')
        else:
            #converts list to string
            makeitastring = ''.join(map(str, dictionary.get('Devices')[e]['ip_addresses']))
            dictionary = makeitastring.translate({ord('{'): None})
            dictionary = dictionary.replace("\'type\': None", '')
            dictionary = '{' + dictionary.translate({ord('}'): None}) + '}'
            dictionary = dictionary.replace(', }', '}')
            dictionary = ast.literal_eval(dictionary)
            print(dictionary)
            print(type(dictionary))
            ip_addresses.append(dictionary.get('ip'))

    print(ip_addresses)
'''

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
## [NOT WORKING PROPERLY]
## HWAddress (macaddress) belongs to 'MAC Address [Configuration Item]' in CSV file
##Needs to filter tuples, works currently for Empty and dictionaries.
#if dictionary is Empty:
mac_addresses = []
for e in range(len(dictionary.get('Devices'))):
    mac_addresses.append('x.x.x.x.x')
'''
for e in range(len(dictionary.get('Devices'))):
    mac_address.append('')
    if len(dictionary.get('Devices')[2]['ip_addresses']) == 0:
        print('ip_addresses:', 'Empty')
    else:
        ip = 'ip_addresses:', dictionary.get('Devices')[2]['ip_addresses']

        #converts list to string
        makeitastring = ''.join(map(str, ip))
        #removes unecessary chars to create dictionary
        makeitastring = makeitastring.replace('ip_addresses:[', '')
        dictionary = ast.literal_eval(makeitastring[:-1])
        print(dictionary)
        print(dictionary.get('macaddress'))
'''

#---------------------------------------------------------------------------------------------
## [NOT WORKING]
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

# 12/16 working properly
CMDB_Items = ['Name', 
              'Location', 
              'Used for [Configuration Item]', 
              'Status',                               #Set to 'Installed'
              'Class',                                #Set to 'Storage Device'
              'CC Type [Configuration Item]',         #IGNORED IN CODE
              'Manufacturer', 
              'Model number [Configuration Item]', 
              'IP Address [Configuration Item',       #WIP
              'Host Name [Configuration Item]', 
              'Serial number', 
              'MAC Address [Configuration Item]',     #WIP
              'Description [Configuration Item]',     #WIP
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