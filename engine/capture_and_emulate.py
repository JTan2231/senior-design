# This script will do the following:
#
# 1. Check if a VPN connection is active and close it.
# 2. Determine device's current location (or provide it).
#     a. Select closest VPN server and connect to it.
#     b. Gather Wi-Fi networks within a 1000ft radius.
# 3. Beigin broadcasting the Wi-Fi networks.
# 4. (optional) show iPhone's connection status to the Pi.

import csv
import select
import sys
import network_scan
import connect as connect
import subprocess
import time
import os

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

# Scan for WiFi networks for 15 seconds or so
# Condense network data into a csv with SSID and MAC pairs
network_scan.capture(network_list_name)

# Spawn a thread for every detected network
# Propagate one network for each thread
# It should use the following commands:
# sudo iw wlan1mon set channel {channel}
# sudo macchanger -m {mac_address} wlan1mon
# sudo mkd3 wlan1mon b -n {ssid} -a -m -s 10
# Propagation function


def propagate(channel, mac_address, ssid):
    # Set the channel
    os.system("sudo iw wlan1mon set channel {}".format(channel))
    # Go down to change the MAC
    os.system("sudo ifconfig wlan1mon down")
    # Set the MAC address
    os.system("sudo macchanger -m {} wlan1mon".format(mac_address))
    # Go back up
    os.system("sudo ifconfig wlan1mon up")
    # Begin propagation
    os.system("sudo mdk3 wlan1mon b -n {} -a -m -s 10".format(ssid))

    #! Issue: the script does not proceed past this point. It is stuck, single threadedly waiting for the previous command to complete
    #! The previous command will not complete unless CTRL + C is forcibly used, or unless a thread is spawned.

    # Propagation using a list and a single script is working. The only thing I changed is maybe -m and increasing the rate to 150pps
    # Also, should refactor how list construction works. When the original list is made, a second list should be made in order of
    # frequency of each SSID. Then, the top x number of SSIDs are kept (5-10).


# Turn off the VPN, if it is on
connect.stop_vpn()

time.sleep(0.5)

# Turn on the VPN
connect.start_vpn()

# Open CSV file
with open("engine/lists/{}.csv".format(network_list_name), 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    # Iterate over each network detected
    while True:
        # check if there is any input available
        if select.select([sys.stdin], [], [], 0)[0]:
            # if there is input available, exit the loop
            break
        for line in csvfile:
            line = line.strip("\n").split(",")
            ssid = line[0]
            mac_address = line[1]
            channel = line[2]

            # Spawn a thread for the given network
            propagate(channel, mac_address, ssid)
            time.sleep(2)
            # Stop propagation
