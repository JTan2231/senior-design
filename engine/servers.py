from geopy.distance import distance
import requests

SERVER_LOCATIONS = {
    'us-alabama': (32.318230, -86.902298),
    'us-south-carolina': (33.836081, -81.163725),
    'us-kentucky': (37.839333, -84.270018),
    'us-indiana': (39.7662, -86.4412),
    'us-wisconsin': (43.784440, -88.787868),
    'us-nebraska': (41.492537, -99.901813),
    'us-ohio': (40.417287, -82.907123),
    'us-connecticut': (41.603221, -73.087749),
    'us-new-mexico': (34.168219, -106.026039),
    'us-vermont': (43.871571, -72.447783),
    'us-maine': (45.253783, -69.445469),
    'us-kansas': (38.498771, -98.320035),
    'us-rhode-island': (41.580103, -71.477429),
    'us-east': (39.833333, -98.583333),
    'us-virginia': (37.431573, -78.656894),
    'us-alaska': (64.200841, -149.493673),
    'us-oregon': (43.804133, -120.554201),
    'us-south-dakota': (44.212655, -100.247164),
    'us-north-dakota': (47.551493, -101.002012),
    'us-north-carolina': (35.759573, -79.019300),
    'us-tennessee': (35.747845, -86.692345),
    'us-west-virginia': (38.597626, -80.454903),
    'us-minnesota': (46.729553, -94.685900),
    'us-iowa': (42.011539, -93.210526),
    'us-idaho': (44.068202, -114.742041),
    'us-massachusetts': (42.407211, -71.382437),
    'us-new-hampshire': (43.193852, -71.572395),
    'us-west-streaming-optimized': (34.052235, -118.243683),
    'us-mississippi': (32.354668, -89.398528),
    'us-oklahoma': (35.007752, -97.092877),
    'us-louisiana': (30.984298, -91.962333),
    'us-missouri': (37.964253, -91.831833),
    'us-michigan': (44.314844, -85.602364),
    'us-arkansas': (34.969704, -92.373123),
    'us-texas': (31.968594, -99.901813),
    'us-east-streaming-optimized': (40.705630, -73.978004),
    'us-pennsylvania': (40.5773, -77.264),
    'us-west': (39.833333, -98.583333),
    'us-salt-lake-city': (40.760779, -111.891046),
    'us-wyoming': (43.000325, -107.554567),
    'us-montana': (46.879682, -110.362566),
    'us-california': (36.778259, -119.417931),
    'us-seattle': (47.606209, -122.332071),
    'us-florida': (27.664827, -81.515754)
}


def get_closest_server():
    url = f'https://ipinfo.io/json'
    response = requests.get(url)
    location = response.json().get('loc')
    user_lat, user_lon = location.split(',')
    user_lat = float(user_lat)
    user_lon = float(user_lon)

    # Calculate distances between user and each server location
    closest_server = None
    closest_distance = float('inf')
    for server, coords in SERVER_LOCATIONS.items():
        server_lat, server_lon = coords
        server_distance = distance(
            (user_lat, user_lon), (server_lat, server_lon)).miles
        if server_distance < closest_distance:
            closest_distance = server_distance
            closest_server = server

    return closest_server


def show_ip_info():
    url = f'https://ipinfo.io/json'
    response = requests.get(url).json()

    # Info
    ip = response.get('ip')
    coords = response.get('loc')
    city = response.get('city')
    state = response.get('region')
    country = response.get('country')

    # Print formatted connection details
    print("IP | Coords | City | State | Country")
    print("{} | {} | {} | {} | {}\n".format(
        ip, coords, city, state, country))
