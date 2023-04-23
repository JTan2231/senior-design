import subprocess
import servers
import time

# https://helpdesk.privateinternetaccess.com/kb/articles/pia-desktop-command-line-interface-2


def get_connection_state():
    output = subprocess.check_output(["piactl", "get", "connectionstate"])
    return output.decode("utf-8")[0:-1]


def get_server_location():
    output = subprocess.check_output(["piactl", "get", "region"])
    return output.decode("utf-8")[0:-1]


def get_vpn_ip():
    output = subprocess.check_output(["piactl", "get", "vpnip"])
    return output.decode("utf-8")[0:-1]


def stop_vpn():
    print("Disconnecting from VPN...", end="", flush=True)
    state = get_connection_state()
    output = subprocess.check_output(["piactl", "disconnect"])
    while state != "Disconnected":
        try:
            output = subprocess.check_output(["piactl", "disconnect"])

            while state != "Disconnected":
                if state == "Connected" or state == "Disconnecting":
                    print(".", end="", flush=True)
                else:
                    print(state)
                time.sleep(0.5)
                state = get_connection_state()

        except Exception as e:
            print("Error disconnecting from VPN. Trying again.")
    print("Done.\n")
    return output.decode("utf-8")[0:-1]


def start_vpn():
    # Show IP details before connecting
    print("Pre-VPN Connection Details:")
    servers.show_ip_info()

    # Connect to the closest VPN server
    closest_server = servers.get_closest_server()

    commands = [
        ["piactl", "set", "region", closest_server],    # Change server location
        ["piactl", "connect"]
    ]


    # Check connection state
    isConnected = False
    while (isConnected == False):
        try:
            for command in commands:
                output = subprocess.check_output(command)
                output = output.decode("utf-8")[0:-1]
                if output != "":
                    print(output)

            state = get_connection_state()
            print("Connecting to VPN...", end="", flush=True)
            while state != "Connected" and state != "Connected\n":
                if state == "Disconnected" or state == "Connecting":
                    print(".", end="", flush=True)
                else:
                    print(state)
                time.sleep(0.5)
                state = get_connection_state()
            isConnected = True
        except Exception as e:
            print("Error connecting to VPN. Trying again.")

    print("Done.")

    # get server location
    connected_server = get_server_location()

    # get IP
    connected_ip = get_vpn_ip()

    print("\nVPN is connected to {} with VPN IP {}".format(
        connected_server, connected_ip))

    # Show IP info AFTER connecting:
    print("Post-VPN Connection Details:")
    servers.show_ip_info()
