# This script will do the following:
#
# 1. Check if a VPN connection is active and close it.
# 2. Determine device's current location (or provide it).
#     a. Select closest VPN server and connect to it.
#     b. Gather Wi-Fi networks within a 1000ft radius.
# 3. Beigin broadcasting the Wi-Fi networks.
# 4. (optional) show iPhone's connection status to the Pi.

import network_scan
import connect as connect
import subprocess
import time
import os
from threading import Thread

network_list_name = input(
    "Please enter a name for the network list. Do not include a file extension. (Default: ut): ") or "ut"

# Setup the monitor network interface on wlan1mon
output = subprocess.check_output(["ifconfig"]).decode("utf-8")[0:-1]
if 'wlan1mon' in output:
    print("\nwlan1mon is already configured, skipping configuration.\n")
else:
    print("Configuring wlan1mon...")
    # Check to see if any conflicting processes need to be killed before starting the WiFi Spam Script
    output = subprocess.check_output(["sudo", "airmon-ng", "check", "kill"])
    output = subprocess.check_output(["sudo", "airmon-ng", "start", "wlan1"])

    output = subprocess.check_output(["ifconfig"]).decode("utf-8")[0:-1]
    if "wlan1mon" in output:
        print("\nwlan1mon successfully configured.\n")
        output = subprocess.check_output(
            ["sudo", "service", "NetworkManager", "start"])

# Scan for WiFi networks for 15 seconds
# Condense network data into a csv with SSID and MAC pairs
network_scan.capture(network_list_name)

# Spawn a thread for every detected network
# Propagate one network for each thread
# It should use the following commands:
# sudo iw wlan1mon set channel {channel}
# sudo macchanger -m {mac_address} wlan1mon
# sudo mkd3 wlan1mon b -n {ssid} -a -m -s 10
# Propagation function


def propagation(channel, mac_address, ssid):
    # Set the channel
    os.system("sudo iw wlan1mon set channel {}".format(channel))
    # Set the MAC address
    os.system("sudo macchanger -m {} wlan1mon".format(mac_address))
    # Begin propagation
    os.system("sudo mkd3 wlan1mon b -n {} -a -m -s 10".format(ssid))


# Iterate over each network detected
for item in network_list_name:
    channel = item['channel']
    mac_address = item['mac_address']
    ssid = item['ssid']

    # Spawn a thread for the given network
    t = Thread(target=propagation, args=(channel, mac_address, ssid))
    t.start()


# Turn off the VPN, if it is on
connect.stop_vpn()

time.sleep(0.5)

# Turn on the VPN
connect.start_vpn()
