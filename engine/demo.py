# This script will do the following:
#
# 1. Check if a VPN connection is active and close it.
# 2. Determine device's current location (or provide it).
#     a. Select closest VPN server and connect to it.
#     b. Gather Wi-Fi networks within a 1000ft radius.
# 3. Beigin broadcasting the Wi-Fi networks.
# 4. (optional) show iPhone's connection status to the Pi.

import wigle as wigle
import connect as connect
import subprocess
import time
import sys

print("CHECK")

coordinates = f"{sys.argv[1]}, {sys.argv[2]}"
print("COORDINATES:", coordinates)
radius = 1000
network_list_name = "ut"

latitude, longitude = coordinates.split(',')
latitude = float(latitude)
longitude = float(longitude)

# Gather Wi-Fi networks
wigle.create_network_list(latitude, longitude, radius, network_list_name)

exit(0)
