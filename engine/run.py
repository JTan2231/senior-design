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

# Setup the monitor network interface on wlan1mon
output = subprocess.check_output(["ifconfig"]).decode("utf-8")[0:-1]

if 'wlan1mon' in output:
    print("\nwlan1mon is already configured, skipping configuration.\n")
else:
    print("Configuring wlan1mon...")
    # Check to see if any conflicting processes need to be killed before starting the WiFi Spam Script
    output = subprocess.check_output(["sudo", "airmon-ng", "check", "kill"])
    output = subprocess.check_output(["sudo", "airmon-ng", "start", "wlan1"])

    output = subprocess.check_output(["ifconfig"], shell=True).decode("utf-8")[0:-1]
    if "wlan1mon" in output:
        print("\nwlan1mon successfully configured.\n")
        output = subprocess.check_output(
            ["sudo", "service", "NetworkManager", "start"])


# Turn off the VPN, if it is on
connect.stop_vpn()

time.sleep(0.5)

# Turn on the VPN
connect.start_vpn()

# Call Wi-Fi propagation script on this list.

# Start script
p = subprocess.Popen('sudo ./engine/WiFiSpam.sh', shell=True,
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
p.stdin.write(b'wlan1mon\n')
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
list_path = "engine/lists/ut.txt\n"
p.stdin.write(list_path.encode("utf-8"))
p.stdin.flush()

# Wait for the script to finish
p.wait()
