#!/usr/bin/env python3
import csv
from datetime import datetime
import json
from loguru import logger
import requests
import urllib3
import configparser
import glob, os

date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p")
D42_username=''
D42_password=''
D42_url=''
D42_location=''
D42_type=''
SNOW_username=''
SNOW_password=''
SNOW_url=''
dictionary=''
console_level=''
file_level=''
syslog_level=''

device_IDs=[]
deviceNames=[]
customers=[]
locations=[]
service_levels=[]
statuses=[]
classes=[]
cc_types=[]
manufacturer=[]
model_numbers=[]
ip_addresses=[]
virtual_host_names=[]
serial_numbers=[]
mac_address=[]
descriptions=[]
usernames=[]
fs_passwords=[]
active_contract=[]
device_sub_type=[]
discovery_source=[]

@logger.catch
def logLevels():
    global console_level
    global file_level
    global syslog_level

    ##log levels
    config = configparser.ConfigParser()
    config.read('config.ini')
    logger.info("Setting log levels...")
    console_level = config.get('Log Level', 'console_level')
    file_level = config.get('Log Level', 'file_level')
    syslog_level = config.get('Log Level', 'syslog_level')
    logger.success("Log levels set.")

logger.add(f"{date}.log")
@logger.catch
def config():
    if file_level == 'QUIET' and console_level != 'QUIET':
        logger.warning("[Config] File level set to 'QUIET', can cause errors in other functions. If so, change level to 'DEBUG'.")
    elif file_level != 'QUIET':
        logger.info("--- NOTE: Running 'config()' function ---")
        try:
            logger.info("Initializing configuration parser...")
            config = configparser.ConfigParser()
            logger.info("Reading configuration file 'config.ini'...")
            config.read('config.ini')

            #referencing global variables
            global D42_username
            global D42_password
            global D42_customer
            global D42_location
            global D42_url
            global D42_type
            global SNOW_username
            global SNOW_password
            global SNOW_url

            #credentials for D42
            D42_username = config.get('Device42', 'user')
            D42_password = config.get('Device42', 'pass')
            D42_url = config.get('Device42', 'url')
            D42_customer = config.get('Device42', 'customer')
            D42_location = config.get('Device42', 'location')
            D42_type = config.get('Device42', 'content-type')
            ##credentials for SNOW
            SNOW_username = config.get('ServiceNow', 'user')
            SNOW_password = config.get('ServiceNow', 'pass')
            SNOW_url = config.get('ServiceNow', 'url')

            logger.success("Configuration details have been retrieved.")
        except:
            logger.error("Failed to read 'config.ini' file...")

@logger.catch
def pullD42():
    logger.info("--- NOTE: Running 'pullD42()' function ---")
    logger.warning("Disabled all unverified HTTPS warnings...")
    ##disables warning for unverified HTTPS (url)
    urllib3.disable_warnings()
    headers = {
                'Content-Type': D42_type
            }

    logger.info("[GET] Requesting Device42 data...")
    try:
        global dictionary
        logger.info("Converting JSON payload into a dictionary, this may take a brief moment...")
        r = requests.request("GET", D42_url, auth=(D42_username, D42_password), headers=headers, verify=False)
        dictionary = json.loads(r.text)
        logger.success("JSON payload has been converted into a dictionary.")
    except:
        logger.error("[GET] Failed to request Device42 data. Make sure the information stored in the 'config.ini' file is correct. If it is, make sure the 'config()' function runs before the 'pullD42()' function.")

@logger.catch
def fields():
    if file_level == 'QUIET':
        logger.warning("[Fields] File level set to 'QUIET', can cause errors in other functions. If so, change level to 'DEBUG'.")
    else:
        logger.info("--- NOTE: Running 'fields()' function ---")

        global device_IDs
        global deviceNames 
        global customers
        global locations
        global service_levels 
        global statuses 
        global classes  
        global cc_types 
        global manufacturer 
        global model_numbers 
        global ip_addresses
        global virtual_host_names 
        global serial_numbers 
        global mac_address 
        global descriptions
        global usernames
        global fs_passwords
        global active_contract
        global device_sub_type
        global discovery_source
        #---------------------------------------------------------------------------------------------    
        ##Device name is 'Name'
        logger.debug("Appending 'Name' data...")
        deviceNames = []
        for e in range(len(dictionary.get('Devices'))):
            deviceNames.append(dictionary.get('Devices')[e]['name'])
        logger.success("Appending of 'Name' complete.")
        #---------------------------------------------------------------------------------------------
        logger.debug("Appending 'ID' data...")
        device_IDs = [[] for i in range(len(dictionary['Devices'][:]))]
        i = 0

        for e in dictionary['Devices'][:]:
            if 'id' in e:
                device_IDs[i].append(e['id'])
            elif 'id' not in e:
                device_IDs[i].append(None)
            i=i+1  
        logger.success("Appending of 'ID' complete.")

        #---------------------------------------------------------------------------------------------
        logger.debug("Appending 'Location' data...")
        locations = [[] for i in range(len(dictionary['Devices'][:]))]
        i = 0

        for e in dictionary['Devices'][:]:
            if 'location' in e:
                locations[i].append(D42_location)
            elif 'location' not in e:
                locations[i].append(D42_location)
            i=i+1  
        logger.success("Appending of 'Location' complete.")
        #---------------------------------------------------------------------------------------------

        ##Used For [Configuration Item] --> not in Verizon_Box, entered Manually ex.: 'Production' as the value
        ##BUT, it's probably 'service_level'
        #if dictionary is Empty:
        logger.debug("Appending 'Used For [Configuration Item]' data...")
        service_levels = []
        for e in range(len(dictionary.get('Devices'))):
            if dictionary.get('Devices')[e]['service_level'] is None:
                    service_levels.append('')
            else:
                service_levels.append(dictionary.get('Devices')[e]['service_level'])
        logger.success("Appending of 'Used For [Configuration Item]' complete.")

        #---------------------------------------------------------------------------------------------

        ## [MISSING]? set to default 'Installed'
        ## Status
        ##Status in ServiceNow is ____ in Verizon_Box? I don't see it.
        #if dictionary is Empty:
        logger.debug("Appending 'Status' data...")
        statuses = []
        #if dictionary is Empty:
        for e in range(len(dictionary.get('Devices'))):
            statuses.append('Installed')
        logger.success("Appending of 'Status' complete.")

        #---------------------------------------------------------------------------------------------

        ## [MISSING]? set to default 'Storage Device'
        ##Class in ServiceNow is ____ in Verizon_Box? IDK.
        #if dictionary is Empty:
        logger.debug("Appending 'Storage Device' data...")
        classes = []
        for e in range(len(dictionary.get('Devices'))):
            classes.append('Storage Device')
        logger.success("Appending of 'Storage Device' complete.")

        #---------------------------------------------------------------------------------------------

        ## 'CC Type' not in Verizon_Box
        logger.debug("Ignoring 'CC Type'...")
        cc_types = []
        for e in range(len(dictionary.get('Devices'))):
            cc_types.append('')
        logger.success("Ignoring of 'CC Type' complete.")

        #---------------------------------------------------------------------------------------------

        ## [WORKING] NEED TO TEST
        ## 'Manufacturer' in ServicenNow is 'manufacturer' in Verizon_Box
        ##will not pull correctly, must be more nested...
        #if dictionary is Empty:
        logger.debug("Appending 'Manufacturer' data...")
        manufacturer = [[] for i in range(len(dictionary['Devices'][:]))]
        i = 0

        for e in dictionary['Devices'][:]:
            if 'manufacturer' in e:
                manufacturer[i].append(e['manufacturer'])
            elif 'manufacturer' not in e:
                manufacturer[i].append(None)
            i=i+1
        logger.success("Appending of 'Manufacturer' complete.")

        #---------------------------------------------------------------------------------------------

        ## 'Model Number [Configuration Item]' in ServiceNow is Hardware Model 'hw_model' in Verizon_Box
        #if dictionary is Empty:
        logger.debug("Appending 'Model Number [Configuration Item]' data...")
        model_numbers = []
        for e in range(len(dictionary.get('Devices'))):
            if dictionary.get('Devices')[e]['hw_model'] is None:
                model_numbers.append(None)
            else:
                model_numbers.append(dictionary.get('Devices')[e]['hw_model'])
        logger.success("Appending of 'Model Number [Configuration Item]' complete.")

        #---------------------------------------------------------------------------------------------

        ## [WORKING]
        ## 'IP Address [Configuration Item]' in ServiceNow is 'IP Address' in Verizon_Box GUI (not in the output.txt)
        ## using temporarily subnet or 'ip' since it's the closest to the IP Address, but missing part of it...
        #if dictionary is Empty:
        logger.debug("Appending 'IP Address [Configuration Item]' data...")
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
        logger.success("Appending of 'IP Address [Configuration Item]' complete.")
        #---------------------------------------------------------------------------------------------

        ## Host Name [Configuration Item] in ServiceNow is 'virtual_host_name' in Verizon_Box (I think?)
        #if dictionary is Empty:
        logger.debug("Appending 'Host Name [Configuration Item]' data...")
        virtual_host_names = []
        for e in range(len(dictionary.get('Devices'))):
            if dictionary.get('Devices')[e]['virtual_host_name'] is None:
                virtual_host_names.append(None)
            else:
                virtual_host_names.append(dictionary.get('Devices')[e]['virtual_host_name'])
        logger.success("Appending of 'Host Name [Configuration Item]' complete.")

        #---------------------------------------------------------------------------------------------

        ## Serial number in ServiceNow is 'serial_no' in Verizon_Box
        #if dictionary is Empty:
        logger.debug("Appending 'Serial Number' data...")
        serial_numbers = []
        for e in range(len(dictionary.get('Devices'))):
            if dictionary.get('Devices')[e]['serial_no'] is None:
                serial_numbers.append(None)
            else:
                serial_numbers.append(dictionary.get('Devices')[e]['serial_no'])
        logger.success("Appending of 'Serial Number' complete.")

        #---------------------------------------------------------------------------------------------

        ## [WORKING]
        ## HWAddress (macaddress) belongs to 'MAC Address [Configuration Item]' in CSV file
        ##Needs to filter tuples, works currently for Empty and dictionaries.
        #if dictionary is Empty:
        logger.debug("Appending 'MAC Address [Configuration Item]' data...")
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
        logger.success("Appending of 'MAC Address [Configuration Item]' complete.")

        #---------------------------------------------------------------------------------------------

        ## [WORKING]
        ## 'Description [Configuration Item]' in ServiceNow is 'description' in Verizon_Box
        ## Needs to be coded in Verizon_Box since D42 sandbox is not giving proper output.
        ## Test in the box and parse hdd_details to get description or it might retrieve from just Devices than hdd_details
        #if dictionary is Empty:
        logger.debug("Appending 'Description' data....")
        descriptions = [[] for i in range(len(dictionary['Devices'][:]))]
        i = 0

        for e in dictionary['Devices'][:]:
            if 'description' in e:
                descriptions[i].append(e['description'])
            elif 'description' not in e:
                descriptions[i].append(None)
            i=i+1
        logger.success("Appending of 'Description' complete.")

        #---------------------------------------------------------------------------------------------

        ## Username [IGNORED, manually entered]
        logger.debug("Ignoring 'Username'...")
        usernames = []
        for e in range(len(dictionary.get('Devices'))):
            usernames.append('')
        logger.success("Ignored 'Username'.")

        #---------------------------------------------------------------------------------------------

        ## Password [IGNORED, manually entered]
        logger.debug("Ignoring 'FS Passwords'...")
        fs_passwords = []
        for e in range(len(dictionary.get('Devices'))):
            fs_passwords.append('')
        logger.success("Ignored 'FS Passwords'.")

        #---------------------------------------------------------------------------------------------

        ## 'Active Contract [Configuration Item]' in ServiceNow is 'in_service' in D42
        ## [WORKING PROPERLY]
        logger.debug("Appending 'Active Contract [Configuration Item]' data...")
        active_contract = [[] for i in range(len(dictionary['Devices'][:]))]
        i = 0

        for e in dictionary['Devices'][:]:
            if 'in_service' in e:
                active_contract[i].append(e['in_service'])
            elif 'in_service' not in e:
                active_contract[i].append(None)
            i=i+1

        logger.success("Appending of 'Active Contract [Configuration Item]' complete.")

        #---------------------------------------------------------------------------------------------

        ## [WORKING] Physical subtype (device_sub_type) in Verizon_Box is ____ in ServiceNow? Idk.
        ##D42 sandbox is called (virtual_subtype)
        #if dictionary is Empty:
        logger.debug("Appending 'Physical Subtype' data...'")
        device_sub_type = [[] for i in range(len(dictionary['Devices'][:]))]
        i = 0

        for e in dictionary['Devices'][:]:
            if 'device_sub_type' in e:
                device_sub_type[i].append(e['device_sub_type'])
            elif 'device_sub_type' not in e:
                device_sub_type[i].append(None)
            i=i+1
        logger.success("Appending of 'Phyiscal Subtype' complete.")

        #---------------------------------------------------------------------------------------------
        # 'rack' is location' but for now default and hardcode to 'Location'
        # which will then be read and replaced by a location that will be
        # posted to ServiceNow/D42
        logger.debug("Appending of 'Location' complete.")
        rack_locations = []
        for e in range(len(dictionary.get('Devices'))):
            rack_locations.append('Location')
        logger.success("Appending of 'Discovery Source' complete.")

        #---------------------------------------------------------------------------------------------
        logger.debug("Appending 'Customer' data...")
        # 'customer'
        customers = [[] for i in range(len(dictionary['Devices'][:]))]
        i = 0

        for e in dictionary['Devices'][:]:
            if 'customer' in e:
                customers[i].append(D42_customer)
            elif 'customer' not in e:
                customers[i].append(D42_customer)
            i=i+1
        logger.success("Appending of 'Customer' complete.")

        #---------------------------------------------------------------------------------------------

        logger.debug("Appending 'Discovery Source' data...")
        discovery_source = []
        for e in range(len(dictionary.get('Devices'))):
            discovery_source.append('Device42')
        logger.success("Appending of 'Discovery Source' complete.")
        #---------------------------------------------------------------------------------------------
  

@logger.catch
def createCSV():
    if file_level == 'QUIET':
        logger.warning("[createCSV] File level set to 'QUIET', can cause errors in other functions. If so, change level to 'DEBUG'.")
    elif file_level != 'QUIET':
        logger.info("--- NOTE: Running 'createCSV()' function ---")
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
                    'Active Contract [Configuration Item]',
                    'Physical Subtype',
                    'Discovery Source'                      #Always 'Device42'
                    ]

        CMDB_Data = list(zip(device_IDs,
                            deviceNames, 
                            customers,
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
                            mac_address, 
                            descriptions,
                            usernames,
                            fs_passwords,
                            active_contract,
                            device_sub_type,
                            discovery_source
                            ))
        logger.debug("Creating CSV file...")
        with open('Verizon_Data.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            try:
                logger.debug("Writing headers to CSV file...")
                # write the headers
                writer.writerow(CMDB_Items)
                logger.success("Successfully written headers to CSV file...")
            except:
                logger.error("Failed to write headers to CSV file.")

            if len(CMDB_Data) != 0:
                logger.debug("Writing rows to CSV file...")
                # write the rows
                for data in CMDB_Data:
                    writer.writerow(data)
                logger.success("Successfully written rows to CSV file...")

                # Removes all unnecessary chars/symbols from csv file
                # reading the CSV file
                text = open("Verizon_Data.csv", "r")

                #join() method combines all contents of 
                # csvfile.csv and formed as a string
                text = ''.join([i for i in text]) 

                logger.debug("Removing special characters and unwanted data from CSV file...")
                # search and replace the contents
                text = text.replace("[None]", "") 
                text = text.replace("[]", "") 
                text = text.replace("[", "") 
                text = text.replace("]", "") 
                text = text.replace(f"[\'", "")
                text = text.replace(f"\']", "")
                text = text.replace(f"\'", "")

                # testD42_Data.csv is the output file opened in write mode
                x = open("Verizon_Data.csv","w")
                
                # all the replaced text is written in the output.csv file
                x.writelines(text)
                x.close()
                logger.success("Successfully re-written data to CSV file to completion.")
            else:
                logger.error("Failed to write rows to CSV file. The data to write does not exist.")


@logger.catch
def postSNOW():
    if file_level == 'QUIET':
        logger.warning("[postSNOW] File level set to 'QUIET', can cause errors in other functions. If so, change level to 'DEBUG'.")
    elif file_level != 'QUIET':
        logger.info("--- NOTE: Running 'postSNOW()' function ---")
        logger.warning("Disabled all unverified HTTPS warnings...")
        ##disables warning for unverified HTTPS (url)
        urllib3.disable_warnings()

        ##Staging table URL 'u_d42_uploads'

        ##Gets CSV file path
        PATH = os.path.dirname(os.path.abspath(__file__))
        os.chdir(PATH)

        logger.debug("Checking files in current directory for a CSV file.")
        for file in glob.glob("*.csv"):
            #tries to get current CSV file to POST in SNOW
            try:
                directPath = PATH.replace("\\", "\\\\")
                PATH = directPath + "\\\\" + file
                ##CSV file to upload
                csv_file = {
                    'import-file': open(f'{PATH}', 'rb')
                }
                logger.debug("[POST] Sending CSV file to SNOW for processing.")
                ##'POST' request to process CSV into the staging table
                r = requests.request("POST", SNOW_url, files=csv_file, auth=(SNOW_username, SNOW_password), verify=False)
                logger.success("[POST] Complete.")
            #exception is raised if there is no CSV file in the directory
            except:
                logger.error("Failed to find a CSV file in the current directory.")
            break
        
# simulation function to test docopt version future addition

if __name__ == "__main__":
    logLevels() #sets logging levels
    config() #config
    pullD42() #Pulls Devices data from D42
    fields() #Populates Devices record fields from lists (all 20 unique fields)
    createCSV() #creates CSV file with Devices record fields data
    #postSNOW() #Posts CSV file to SNOW staging table and processes


    ##To Test, edit 'config.ini' with the following information (ignore SNOW information):
    '''
    [Device42]
    user : guest
    pass : device42_rocks!
    url : https://swaggerdemo.device42.com/api/1.0/devices/all/
    customer : D42 Customer
    location : D42 sandbox, corp.
    content-type : application/json
    '''
