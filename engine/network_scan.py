import subprocess
import csv


def capture(filename):
    # Scan for WiFi networks
    proc = subprocess.Popen('sudo iwlist wlan0 scan',
                            stdout=subprocess.PIPE, shell=True)
    data_str = proc.communicate()[0].decode('utf-8')

    # Parse data from string to list
    data_list = data_str.split('\n')

    # Establish lists
    ssid_list = []
    mac_list = []

    # For each element in the list, find SSID and MAC address and add to appropriate list
    for line in data_list:
        if 'ESSID:' in line:
            ssid_list.append(line.split(':')[1].strip('"'))
        elif 'Address:' in line:
            mac_list.append(line.split(':')[1])

    # Open CSV file and save results
    with open('{}.csv'.format(filename), 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(zip(ssid_list, mac_list))
