import netfilterqueue
import scapy.all as scapy

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    
    print(scapy_packet.show())
    packet.accept()



def main():
    queue = netfilterqueue.NetfilterQueue()
    
    # Bind to queue number 0.
    queue.bind(0, process_packet)
    queue.run()

if __name__ == "__main__":
    main()