# DNS Spoof

## Intercepting & Modifying Packets

- `Scapy` can be used to:
  - Create a packets.
  - Analyse packets.
  - Send/receive packets.

- But it can't be used to **intercept** packets/flows.

## Classic MITM scenario

- User <-----> (queue) Hacker (queue) <----> Access point
- A better implementation is to create a queue in our hacker machine and trap packets inside that queue. So whenever we get a request, we will put it in that queue and never send it to its target. Then we will access this queue from our Python program and modify the packets as we want.
- We can use the same way to modify responses, so whenever we get a response we will trap it in a queue. We access the queue from a python program and only then, only after modifying the packet will actually be forwarded to its destination.

- Fist thing we want to redirect any packets that we receive on this computer to this queue: `iptables -I FORWARD -j NFQUEUE --queue-num 0`
  - `I` arguments to specify a chain that we want to modify, and the chain we want to modify is `FORWARD` chain, because this is the chain or the place where packets that come to our computer are placed in by default.
  - `J` we want to put this in an `NFQUEUE`, which is a short net filter. and we are just going to use number `0` to identify our queue.
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

- After finish, one more thing u can do are flushing iptables: `iptables flush`
