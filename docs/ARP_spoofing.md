# ARP Spoofing

## What is ARP spoofing?

- ARP spoofing allows us to redirect the flow packets.
  - Normally:
    Hacker<-------->|Access point <-----> Resources
    User<---------->|

  - Become:
    Hacker <------->|Access point <----> Resources
     /\
     ||
     \/
    User

- So any requests sent and any responses received by the target computer will have to flow through the hacker computer.
- This allows we to read this information, modify it, or drop it.

- Basically, ARP is used so that clients can identify other connected clients on same network. So each computer have an ARP table which links Ip addresses on the same network to their MAC address.
  - Check on Linux or Windows:

  ```bash
  arp -a
  ```

- We can exploit the ARP protocol and send two ARP responses one to the gateway.

    Hacker--I am at 10.0.2.7----->|Access point <----> Resources
     ||
    I am at 10.0.2.1
     ||
     \/
    User (IP: 10.0.2.7)

- Result of this, the user is going to think that i am the router and the router is going to think that I am the User.

- So any time the User wants to send any requests, the requests will have to flow though my computer and I am going to forward them to router after.

## Why ARP Spoofing is possible?

- CLient is accept responses even if they did not send a request.
- Client trust response without any form of verification.

## arpspoof tool

- `arpspoof` - Intercept packets on a switched LAN.
- For example: `arpspoof -i eth0 -t 10.0.2.7 10.0.2.1`
  - This will spoof the target `10.0.2.7`, telling him that I am the router `10.0.2.1`.
  - Now, we tell with router that we are the User: `arpspoof -i eth0 -t 10.0.2.1 10.0.2.7`
  - NOTE: Keep in mind, this attack will work against both Ethernet and wifi or wireless networks.

- After that, we can then test this working by checking ARP table at User machine and Router (check MAC address): `arp -a`

- NOTE: Enable port forwarding on Linux: `echo 1 > /proc/sys/net/ipv4/ip_forward`

## Restore normally traffic

- We will send an ARP response to the User telling it that the router is at this MAC address. And also so the same with the router, so we will send it an ARP response saying this IP should be associated with the MAC address. So we can restore the ARP table in the router and the target so that the traffic will go back to flowing normally.
