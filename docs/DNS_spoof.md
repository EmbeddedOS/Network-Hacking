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
  - `J` we want to put this in an net filter queue `NFQUEUE`, which is a short net filter. and we are just going to use number `0` to identify our queue.
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

- After finish, one more thing u can do are flushing iptables: `iptables --flush`

## Converting packet to Scapy packets

- If you want to be able to test on your local computer, we are going to have to change this rule and say that the chain that you want to trap its packets is the `OUTPUT` chain: `iptables -I OUTPUT -j NFQUEUE --queue-num 0`
  - This is the chain where packets leaving your computer go through.

  - Next, we need to run `iptables -I INPUT -j NFQUEUE --queue-num 0` so these are the packets coming to your computer.

  - By using these two commands by redirecting the output and the input chain to your QUEUE and here all requests and responses sent to my computer will be trapped into this queue and then we will be able to use our program exactly the same way.
