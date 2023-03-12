# DNS Spoof

## Intercepting & Modifying Packets

- `Scapy` can be used to:
  - Create a packets.
  - Analyse packets.
  - Send/receive packets.

- But it can't be used to **intercept** packets/flows.

## Classic MITM scenario

- User <-----> (queue) Hacker (queue) <----> Access point

- Push packets to specified queue with: `iptables`
  - For example: `iptables -I FORWARD -j NFQUEUE --queue-num 0`
    - Insert FORWARD rule, action is add to queue with number 0 when packet matches it.
    - In python code, we filter queue `0`:

    ```python
    import netfilterqueue

    def process_packet(packet):
        print(packet)
        packet.drop()

    queue = netfilterqueue.NetFilterQueue()
    queue.bind(0, process_packet)
    queue.run()
    ```
