# This script will do the following:
#
# 1. Check if a VPN connection is active and close it.
# 2. Determine device's current location (or provide it).
#     a. Select closest VPN server and connect to it.
#     b. Gather Wi-Fi networks within a 1000ft radius.
# 3. Beigin broadcasting the Wi-Fi networks.
# 4. (optional) show iPhone's connection status to the Pi.

import os
import wigle as wigle
import connect as connect
import subprocess
import time

coordinates = input(
    "Please enter a start location (Default: 41.658048, -83.614218): ") or "41.658048, -83.614218"
radius = input(
    "Please enter an acceptable search radius in feet (Default: 1000): ") or 1000
network_list_name = input(
    "Please enter a name for the network list. Do not include a file extension. (Default: ut): ") or "ut"

latitude, longitude = coordinates.split(',')
latitude = float(latitude)
longitude = float(longitude)

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


# Turn off the VPN, if it is on
connect.stop_vpn()

time.sleep(0.5)

# Turn on the VPN
connect.start_vpn()

# Gather Wi-Fi networks
wigle.create_network_list(latitude, longitude, radius, network_list_name)

# Call Wi-Fi propagation script on this list.
# Begin propagation
os.system(
    "sudo mdk3 wlan1mon b -n -f lists/{}.txt -a -m -s 10".format(network_list_name))
