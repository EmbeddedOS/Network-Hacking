#!/usr/bin/python3

import subprocess
import optparse
import re


def get_current_mac_address(_interface):
    result = subprocess.check_output(
        ["ifconfig", str(_interface)]).decode("utf-8")
    current_mac_address = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", result)
    if current_mac_address:
        print("Current MAC address is {}".format(
            str(current_mac_address.group(0))))

        return str(current_mac_address.group(0))
    else:
        print("Can not get MAC address.")
        return -1


def main():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface",
                      help="Interface to change its MAC address.")

    parser.add_option("-m", "--mac", dest="mac", help="MAC address.")

    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("Please specify an interface.")
    elif not options.mac:
        parser.error("Please specify an MAC address.")

    interface = str(options.interface)
    mac = str(options.mac)

    if mac == get_current_mac_address(interface):
        print("MAC address didn't get changed.")
        return 0

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig", interface, "up"])

if __name__ == "__main__":
    main()
