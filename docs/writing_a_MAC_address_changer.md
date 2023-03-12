# Writing a MAC address changer

## MAC Address

* Media Access Control
  * Permanent.
  * Physical.
  * Unique.
* Assigned by manufacturer.

## Why change the MAC Address

1. Increase anonymity.
2. Impersonate other devices.
3. Bypass filters.

Change the MAC address simply with `ifconfig` command: `ifconfig <interface> hw ether <new_mac_address>`

```commandline
ifconfig eth0 down
ifconfig eth0 hw ther 00:11:22:33:44:55
ifconfig eth0 up
```

## Python using a module to execute system command

* The `subprocess` module contains a number of functions.
* These functions allow us to **execute system commands**.
* commands depend on the OS which executes the script.

syntax:

```python
import subprocess
subprocess.call("COMMAND", Shell=True)
```

the `call()` method return status code number of the command.
