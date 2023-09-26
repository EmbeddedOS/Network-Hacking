# Programming a network scanner

- Discover all devices on the network.
- Display their IP address.
- Display their MAC address.

## Introduction to ARP

- Basically, ARP is used so that clients can identify other connected clients on same network. So each computer have an ARP table which links Ip addresses on the same network to their MAC address.
  - Check on Linux:

  ```bash
  arp -a
  ```

- ARP request will ask for who has specified IP. The device that has the IP, will reply its MAC address.

## Network scanner algorithm

- Steps:
  - step 1: Create arp request directed to broadcast MAC asking for IP.
    - Two main parts:
      - Use ARP to ask who has target IP.
      - Set destination MAC to broadcast MAC.

  - Step 2: Send packet and receive response.
  - Step 3: Parse the response.
  - Step 4: Print result.
