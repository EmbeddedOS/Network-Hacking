import scapy.all as scapy
import optparse

# python3 network_scanner.py -t 192.168.233.0/24


def ACK_scan(ip, port):
    ans, unans = scapy.sr(scapy.IP(dst=ip)/scapy.TCP(dport=port, flags="A"))
    for s, r in ans:
        if s[scapy.TCP].dport == r[scapy.TCP].sport:
            print("%d is unfiltered" % s[scapy.TCP].dport)


def scan_network_with_ip(ip):
    print("Step 1: Making a arp request to ask who has {} IP address.".format(ip))
    arp_request = scapy.ARP(pdst=ip)

    # Setting destination MAC to broadcast MAC.
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    print("Step 2: Sending the packet.")
    # Making ARP request broadcast, which is the combination of the two.
    arp_request_broadcast = broadcast/arp_request

    # Send and receive packets at layer 2.
    answered_list, unanswered_list = scapy.srp(
        arp_request_broadcast,
        timeout=2,
        verbose=False)

    client_info = []
    print("Step 3: Parsing the answers:")
    for answer in answered_list:
        ip = answer[1].psrc
        mac = answer[1].hwsrc
        client_info.append({"ip": ip, "mac": mac})

    return client_info


def help():
    # Get scapy helper functions.
    scapy.lsc()


def main():
    parser = optparse.OptionParser()

    parser.add_option("-t", "--target", dest="target",
                      help="Target IP to scan.")

    (options, arguments) = parser.parse_args()

    if not options.target:
        parser.error("Please specify an IP.")

    ip = str(options.target)

    result = scan_network_with_ip(ip)
    print(result)


if __name__ == "__main__":
    main()
