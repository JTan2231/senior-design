import subprocess
import csv


def scan(filename):
    # Scan for WiFi networks
    proc = subprocess.Popen('sudo iwlist wlan0 scan',
                            stdout=subprocess.PIPE, shell=True)
    data_str = proc.communicate()[0].decode('utf-8')

    # Parse data from string to list
    data_list = data_str.split('\n')

    # Establish lists
    ssid_list = []
    # channel_list = []
    # mac_list = []

    # For each element in the list, find SSID and MAC address and add to appropriate list
    for line in data_list:
        if 'ESSID:' in line:
            curr_ssid = line.split(':')[1].strip('"').strip(",")
            if curr_ssid not in ssid_list and '""' not in curr_ssid and "\\" not in curr_ssid:
                ssid_list.append(curr_ssid)
        # elif 'Address:' in line:
        #     mac_list.append(line.split()[4])
        # elif 'Channel:' in line:
        #     channel_list.append(line.split(':')[1].strip('"').strip(","))

    # Open CSV file and save results
    with open('lists/{}.txt'.format(filename), 'w') as outfile:
        writer = csv.writer(outfile)
        for ssid in ssid_list:
            writer.writerow([ssid])
