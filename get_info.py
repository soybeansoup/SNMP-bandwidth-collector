#!/usr/bin/python

from pysnmp.hlapi import *
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('path_to_domain_list', help='domain list to read from')
args = parser.parse_args()

with open(args.path_to_domain_list) as file: domain_list = [line.strip() for line in file]

def get_info(domain_list):
    for domain in domain_list:
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   CommunityData('Public', mpModel=1),
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
                print(' = '.join([x.prettyPrint() for x in varBind]))

get_info(domain_list)
