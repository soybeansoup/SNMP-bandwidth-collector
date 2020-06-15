#!/usr/bin/python

from pysnmp.hlapi import *
import argparse
import threading

# Handles arguments for input.
parser = argparse.ArgumentParser()
parser.add_argument('path_to_domain_list', help='domain list to read from')
args = parser.parse_args()

with open(args.path_to_domain_list) as file: domain_list = [line.strip() for line in file]

# Output handling happens here.
file_name = 'threaded_data_log.txt'
log_data = open(file_name, 'a+')


def get_info(domain_list, write_file):
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
            print(domain_data)
            write_file.write(str(domain_data) + '\n')



# Splitting domain list for threading
first = domain_list[:round(len(domain_list)/5)]
second = domain_list[round(len(domain_list)/5):round(len(domain_list)/5*2)]
third = domain_list[round(len(domain_list)/5*2):round(len(domain_list)/5*3)]
fourth = domain_list[round(len(domain_list)/5*3):round(len(domain_list)/5*4)]
fifth = domain_list[round(len(domain_list)/5*4):]

t1 = threading.Thread(target=get_info, args=(first, log_data))
t2 = threading.Thread(target=get_info, args=(second, log_data))
t3 = threading.Thread(target=get_info, args=(third, log_data))
t4 = threading.Thread(target=get_info, args=(fourth, log_data))
t5 = threading.Thread(target=get_info, args=(fifth, log_data))


t1.start()
t2.start()
t3.start()
t4.start()
t5.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()

log_data.close()
