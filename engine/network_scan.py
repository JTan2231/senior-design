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
    channel_list = []

    # For each element in the list, find SSID and MAC address and add to appropriate list
    for line in data_list:
        if 'ESSID:' in line:
            ssid_list.append(line.split(':')[1].strip('"'))
        elif 'Address:' in line:
            mac_list.append(line.split()[4])
        elif 'Channel:' in line:
            channel_list.append(line.split(':')[1].strip('"'))

  # Open CSV file and save results
    with open('engine/lists/{}.csv'.format(filename), 'w') as outfile:
        writer = csv.writer(outfile)
        for i in range(len(ssid_list)):
            if int(channel_list[i]) > 11:
                continue
            writer.writerow([ssid_list[i], mac_list[i], channel_list[i]])
