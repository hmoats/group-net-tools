#!/usr/bin/python

import sys
import argparse
import ipaddress

parser = argparse.ArgumentParser(description='Describe network utility')
parser.add_argument('net', help='network/bits [10.10.10.0/24]')
parser.add_argument('-list', action='store_true', help='list hosts in network')
parser.add_argument('-subnet', type=int, help='list slices in network')
args = parser.parse_args()


try:
    ipint = ipaddress.ip_interface(args.net.decode("utf-8"))
    ipnet = ipaddress.ip_network(ipint.network)
except (ValueError):
    print "Abort: ", args.net, "does not look like a valid prefix\n"
    parser.print_help()
    exit()

if args.subnet and (args.subnet < ipnet.prefixlen or args.subnet > 32):
    print "Abort: %s new subnet slice has to longer prefix than %s" % (args.subnet, ipnet.prefixlen)
    parser.print_help()
    exit()

if args.net and not args.list and not args.subnet:
        print '#[ Describe Network ]##############################'
        print '#'
        print "# Input:\t\t%s" % ipint
        print '# Network: \t\t', ipnet
        print '# Base: \t\t', ipnet.network_address
        print '# Broadcast:\t\t', ipnet.broadcast_address
        print '# Bits: \t\t', ipnet.prefixlen
        print '# Netmask: \t\t', ipnet.netmask
        print '# Hostmask: \t\t', ipnet.hostmask
        print '# Hosts: \t\t', ipnet.num_addresses
        print '# Reverse Pointer: \t', ipnet.network_address.reverse_pointer
        print '#'

if args.list:
        print '#[ List Hosts in Network ]#########################'
        print '#'
        print "%s, NETWORK" % ipnet.network_address
        for ip in ipnet.hosts():
                print "%s, HOST" % ip
        print "%s, BROADCAST" % ipnet.broadcast_address
        print '#'

if args.subnet:
        print '#[ Subnet Slice of Network ]#######################'
        print '#'
        for n in list(ipnet.subnets(new_prefix=args.subnet)):
            print "%s, NETWORK" % n
