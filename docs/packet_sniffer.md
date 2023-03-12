# Packet sniffer

- Capture data flowing through an interface.
- Filter this data.
- Display interesting information.
  - Login info (usernames & passwords).
  - Visited websites.
  - Images.
  - ...etc.

## Capture and filter data

- `scapy` has a sniffer function.
- Can capture data sent to/from interface.
- Can call a function specified in prn on each packet.
- Syntax:
  - `scapy.sniff(iface=[interface], prn=[call_back])`

## ARP Spoof + packet sniffer

- Target a computer on the same network.
- Arp_spoof to redirect flow of packets (become MITM).
- Packet_sniffer to see URLs, usernames and password sent by target.

## Some website available for testing

- [link](http://testhtml5.vulnweb.com)
