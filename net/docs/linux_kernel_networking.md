# Linux Kernel Networking

- This document deals with the implementation of the Linux Kernel Networking stack and theory behind it.
- Linux Began as an Intel x86-based OS but has been ported to a very wide range of processors, including ARM, PowerPC, MIPS, SPARC, and more. The Android OS, based upon the Linux kernel, is common today in tablets and smartphones, and seems likely to gain popularity in the future in smart TVs.
- The Linux kernel networking stack is a very important subsystem of the Linux kernel. it is quite difficult to find a Linux-based system, whether it is a desktop, a server, a mobile device or any other embedded device, that does not use any kind of networking.

- The Linux Network Stack:
  - There are seven logical networking layers according to the Open System Interconnection OSI model. The lowest is the physical layer, the lowest layer is the physical layer, which is the hardware, and the highest layer is the application layer, where user space software processes are running. Let's describe these seven layers:
    - 1. *The physical layer*: Handles electrical signals and the low level details.
    - 2. *The data link layer*: Handles data transfer between endpoints. The most common data link layer is ethernet. The Linux Ethernet network device drivers reside in this layer.
    - 3. *The network layer*: Handles packet forwarding and host addressing. The most common network layers of the Linux Kernel Networking subsystem: IPv4 or IPv6.
    - 4. *The protocol layer/transport layer*: layer handles data sending between nodes. The TCP and UDP protocols are the best-known protocols.
    - 5. *The session layer*: Handles sessions between endpoints.
    - 6. *The presentation layer*: Handles delivery and formatting.
    - 7. *The application layer*: Provides network services to end-user applications.
  - Three layers that the Linux Kernel Networking stack handles.
    - 1. L2.
    - 2. L3 (IPv4, IPv6)
    - 3. L4 (TCP/UDP, ...)
  - The L2, L3, and L4 layers in this figure correspond to the data link layer, the network layer, and the transport layer in the seven-layer model, respectively. The essence of the Linux Kernel stack is **passing incoming packets from Layer 2 (network device driver) to Layer 3 (Network layer) and then to Layer 4 if they are for local delivery or back to Layer 2 for transmission when the packets should be forwarded**. Outgoing packets that were locally generated are passed from Layer 4 to Layer 3 and then to Layer 2 for actually transmission by the network device driver. Along this way there are many stages, and many things can happen. For example:
    - The packet can be changed due to protocol rules (for example, due to an IPsec rule or to a NAT rule).
    - The packet can be discarded.
    - The packet can cause an error message to be sent.
    - The packet can be fragmented.
    - The packet can be de-fragmented.
    - A checksum should be calculated for the packet.
  - The kernel does not handle any layer above layer 4; those layers (the session, presentation, and application layers) are handled solely by user space application.

- The Network Device
