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

coordinates = input(
    "Please enter a start location (Ex: 41.658048, -83.614218): ")
radius = input(
    "Please enter an acceptable search radius in feet (default is 1000): ")
network_list_name = input(
    "Please enter a name for the network list. Do not include a file extension. (Ex: Toledo): ")

latitude, longitude = coordinates.split(',')
latitude = float(latitude)
longitude = float(longitude)

# Turn off the VPN, if it is on
connect.stop_vpn()

# Turn on the VPN
connect.start_vpn()

# Gather Wi-Fi networks
wigle.create_network_list(latitude, longitude, radius, network_list_name)

# Call Wi-Fi propagation script on this list.

# Start script
p = subprocess.Popen('sudo ./WiFiSpam.sh', shell=True,
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE)
# output = subprocess.run(["sh", "WiFiSpam.sh"])
# print(output.decode("utf-8")[0:-1])

# Wait for the script to print out a prompt
print("Waiting for first prompt...")
# output = p.stdout.readline().decode('utf-8')
# while 'Type your wireless interface >' not in output:
#    output = p.stdout.readline().decode('utf-8')

time.sleep(1)

# Send the parameter to the script
print("Sent response to first prompt...")
p.stdin.write(b'wlan1\n')
p.stdin.flush()

# Wait for the script to print out a prompt
print("Waiting for second prompt...")
output = p.stdout.readline().decode('utf-8')
while 'Choose an option:' not in output:
    output = p.stdout.readline().decode('utf-8')

# Send the parameter to the script
print("Sent response to second prompt...")
p.stdin.write(b'3\n')
p.stdin.flush()

# Wait for the script to print out a prompt
print("Waiting for third prompt...")
# output = p.stdout.readline().decode('utf-8')
# while 'Type the name of your own word list >' not in output:
#    output = p.stdout.readline().decode('utf-8')

# Send the parameter to the script
print("Sent response to third prompt...")
list_path = "lists/{}.txt\n".format(network_list_name)
p.stdin.write(list_path.encode("utf-8"))
p.stdin.flush()

# Wait for the script to finish
p.wait()
