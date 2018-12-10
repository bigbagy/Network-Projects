#!/usr/bin/python
# CS 6250 Fall 2018 - Project 6 - SDN Firewall

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from pyretic.core import packet 

def make_firewall_policy(config):

    rules = []

    for entry in config:

#    entry={'macaddr_dst': '-', 'protocol': 'T', 'rulenum': '1', 'port_src': '-', 'ipaddr_dst': '10.0.0.6', 'macaddr_src': '-', 'port_dst': '1723','ipaddr_src': '-'}

        entryrule = match(ethtype=packet.IPV4)
        if entry['macaddr_dst'] != '-':
            entryrule = entryrule & match(dstmac=EthAddr(entry['macaddr_dst']))
        if entry['port_src'] != '-':
            entryrule = entryrule & match(srcport=int(entry['port_src']))
        if entry['ipaddr_dst'] != '-':
            entryrule = entryrule & match(dstip=entry['ipaddr_dst'])
        if entry['macaddr_src'] != '-':
            entryrule = entryrule & match(srcmac=EthAddr(entry['macaddr_src']))
        if entry['port_dst'] != '-':
            entryrule = entryrule & match(dstport=int(entry['port_dst']))
        if entry['ipaddr_src'] != '-':
            entryrule = entryrule & match(srcip=entry['ipaddr_src'])

#below parse protocol
        if entry['protocol'] == 'T':
            entryrule = entryrule & match(protocol=6)
        if entry['protocol'] == 'U':
            entryrule = entryrule & match(protocol=17)
        if entry['protocol'] == 'I':
            entryrule = entryrule & match(protocol=1)
        if entry['protocol'] == 'B':
            entryrule = entryrule & match(protocol=6) #tcp=6

        # TODO - This is where you build your firewall rules...
        # Note that you will need to delete the first rule line below when you create your own
        # firewall rules.  Refer to the Pyretic github documentation for instructions on how to
        # format these commands.
        # Example (but incomplete)
        # rule = match(srcport = int(entry['port_src']))
        # The line below is hardcoded to match TCP Port 1080.  You must remove this line
        # in your completed assignments.


        rules.append(entryrule)

     
        if entry['protocol'] == 'B' :
            entryrule = match(ethtype=packet.IPV4)
            if entry['macaddr_dst'] != '-':
                entryrule = entryrule & match(dstmac=EthAddr(entry['macaddr_dst']))
            if entry['port_src'] != '-':
                entryrule = entryrule & match(srcport=int(entry['port_src']))
            if entry['ipaddr_dst'] != '-':
                entryrule = entryrule & match(dstip=entry['ipaddr_dst'])
            if entry['macaddr_src'] != '-':
                entryrule = entryrule & match(srcmac=EthAddr(entry['macaddr_src']))
            if entry['port_dst'] != '-':
                entryrule = entryrule & match(dstport=int(entry['port_dst']))
            if entry['ipaddr_src'] != '-':
                entryrule = entryrule & match(srcip=entry['ipaddr_src'])
            entryrule = entryrule & match(protocol=17) #udp=17
            rules.append(entryrule)

    allowed = ~(union(rules))

    return allowed


#below handler can be deleted

#config={'macaddr_dst': '-', 'protocol': 'T', 'rulenum': '1', 'port_src': '-', 'ipaddr_dst': '10.0.0.6', 'macaddr_src': '-', 'port_dst': '1723','ipaddr_src': '-'}
