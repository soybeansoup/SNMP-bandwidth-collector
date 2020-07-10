#!/usr/bin/python
from pysnmp.hlapi import *
import argparse
import threading

parser = argparse.ArgumentParser()
parser.add_argument('path_to_domain_list', help='domain list to read from')
args = parser.parse_args()
with open(args.path_to_domain_list) as file: domain_list = [line.strip() for line in file]
log_data = []


def get_info(domain_list, log_data):
    for domain in domain_list:
        domain_data=[] # Initializes list to later write data from (single line per domain).
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData('public', mpModel=1), # Assigns community string to SNMP request and sets V.
                   UdpTransportTarget((domain, 161)),
                   ContextData(),
                   ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0)),
                   ObjectType(ObjectIdentity('IF-MIB', 'ifDescr', 1)),
                   ObjectType(ObjectIdentity('IF-MIB', 'ifName', 1)),
                   ObjectType(ObjectIdentity('IF-MIB', 'ifHCInOctets', 1)),
                   ObjectType(ObjectIdentity('IF-MIB', 'ifHCInUcastPkts', 1)),
                   ObjectType(ObjectIdentity('IF-MIB', 'ifHCOutUcastPkts', 1)),
                   ObjectType(ObjectIdentity('IF-MIB', 'ifCounterDiscontinuityTime', 1)))
        )

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                domain_data.append(str(varBind[1])) # Index of 1 grabs only data with no MIB info/context data.
            log_data.append(" ".join(domain_data)) # merges data objects into single line and appends to log list


# Splitting domain list for threading
first = domain_list[:round(len(domain_list)/5)]
second = domain_list[round(len(domain_list)/5):round(len(domain_list)/5*2)]
third = domain_list[round(len(domain_list)/5*2):round(len(domain_list)/5*3)]
fourth = domain_list[round(len(domain_list)/5*3):round(len(domain_list)/5*4)]
fifth = domain_list[round(len(domain_list)/5*4):]

to_thread = [ t1 = threading.Thread(target=get_info, args=(first, log_data)),
              t2 = threading.Thread(target=get_info, args=(second, log_data)),
              t3 = threading.Thread(target=get_info, args=(third, log_data)),
              t4 = threading.Thread(target=get_info, args=(fourth, log_data)),
              t5 = threading.Thread(target=get_info, args=(fifth, log_data)),
            ]

for thread in to_thread:
    thread.start()
for thread in to_thread:
    thread.join()

# Writes compiled data to log file
file_name = 'threaded_data_log.txt'
write_file = open(file_name, 'a+')
for data in log_data:
    write_file.write(str(data) + '\n')
write_file.close()
