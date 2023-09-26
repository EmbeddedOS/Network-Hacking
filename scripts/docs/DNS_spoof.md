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

## Introduction to DNS spoofing

- When we actually try to go to a website, we never use the IP. We are going to the domain name, and here is where DNS server are used.
- When the user sends a request to the DNS sever asking for the domain name, the DNS server will have a big table that contains a number of domains with its IP.
- Therefore it is going to send a DNS response to the user telling the user that Domain actually is located at a computer with its IP address. And the computer will able to use that website.

- Let's say the user wants to go to `domain.com`, the hacker is going to receive this request. And at this stage, the hacker has a number of ways to serve the IP of the hacker's web server. And instead of the IP of `domain.com`, this is very dangerous because we will be able to hack and spoof any DNS request made by the user and serve the user. Fakes websites, fake login pages, fake updates, and so on.

## Filter DNS responses

- If you are `the man in the middle` and you get a DNS request from a user of a domain name, then you can easily spoof this request and serve the user any website you want.

- The easiest is to install a DNS server, so an application similar to the one installed on this web server on your machine and configure that server to return whatever website you want for whatever request that the users enters.

- The next option is to craft a DNS response in the hacker computer, in this computer right here and send it back to the user, given them this IP instead of the actual IP for the domain.

- The third option is to actually forward the request that the user made to the right DNS server. Wait for the response and once we get the response at the hacker machine will modify this response will only modify the IP part and instead of sending the right IP, we will send the IP that we want and this is what we will do.

- We can a DNS request from client with `nslookup` or `ping` commands.
