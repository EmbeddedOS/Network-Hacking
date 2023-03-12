# Programming a network scanner

* Discover all devices on the network.
* Display their IP address.
* Display their MAC address.

## Introduction to ARP

ARP request will ask for who has specified IP. The device that has the IP, will reply its MAC address.

## Network scanner algorithm

Steps:

1. Create arp request directed to broadcast MAC asking for IP.
   1. Two main parts:
      * Use ARP to ask who has target IP.
      * Set destination MAC to broadcast MAC.

2. Send packet and receive response.
3. Parse the response.
4. Print result.
