import requests
import time
import coordinate
import os


def create_network_list(x, y, radius, list_name):
    # Check if the list already exists
    if os.path.exists("lists/{}.txt".format(list_name)):
        use_existing = input(
            'List ' + list_name + ' already exists. Use the existing list? (Default: yes): ') or "yes"
        if use_existing == "yes":
            return

    # Establish search area
    search_area = coordinate.SearchArea(x, y, radius)

    # WiGLE API call
    url = 'https://api.wigle.net/api/v2/network/search?'
    headers = {'Authorization': 'Basic QUlENjQ5OThlMjkyMjI5MjBmNDg2MzYzOGEzODc4NTU2M2I6ZmYwMzkxNjMwODEwZTdjMGNkMmMxYWRiNjU4M2RlMmQ='}
    params = {
        "onlymine": "false",
        "latrange1": search_area.lat1,
        "latrange2": search_area.lat2,
        "longrange1": search_area.long1,
        "longrange2": search_area.long2,
        "freenet": "false",
        "paynet": "false",
        "variance": "0.001",
        "resultsPerPage": "1000"
    }

    # Initialize searchAfter parameter
    searchAfter = None

    # Initialize list of SSID names
    ssid_list = []
    queries = 0
    print("Downloading network list...", end="", flush=True),

    while True:
        # Update the params with searchAfter value
        params['searchAfter'] = searchAfter

        # Make request
        response = requests.get(url, headers=headers, params=params)
        if (response.status_code == 429):
            print(response.json())
            break
        elif (response.status_code == 200):
            print(".", end="", flush=True),
        else:
            print(response.status_code)
        data = response.json()

        # Append SSID names to ssid_list
        try:
            ssid_list += [network['ssid'] for network in data['results']]

            # Update searchAfter parameter with the returned value
            searchAfter = data.get('searchAfter', '')

            # Break if searchAfter is null or empty string
            if not searchAfter:
                break
            time.sleep(0.1)
            queries += 1
        except KeyError as error:
            print("Finished")
            print("This location cost {} queries.".format(queries))
            break

    ssid_list = list(dict.fromkeys(ssid_list))
    with open('lists/{}.txt'.format(list_name), 'w') as f:
        ssid_list = list(dict.fromkeys(ssid_list))
        for entry in ssid_list:
            if entry == None:
                continue
            f.write(str(entry) + '\n')
    print("\nNetwork list saved under {}.txt.".format(list_name))
