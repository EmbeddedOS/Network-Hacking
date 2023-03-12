import scapy.all as scapy


def scan_network_with_ip(ip):
    arp_request = scapy.ARP(pdst=ip)
    print(arp_request.summary())


scan_network_with_ip("ip")
