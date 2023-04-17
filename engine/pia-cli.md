# Overview

This document details how to interface with the PIA VPN over the command line.

Mac and Linux
On Mac and Linux, piactl is symlinked into /usr/local/bin at installation time if possible, so normally piactl is sufficient from a command line. For example:

piactl --help
piactl connect
This requires that:

There isn't already a file called piactl in /usr/local/bin
/usr/local/bin is already in your PATH (PIA does not alter PATH)
On Linux, the directory /usr/local/bin must already exist.
Otherwise, the full path to piactl can be used - on Mac: /Applications/Private Internet Access.app/Contents/MacOS/piactl; on Linux: /opt/piavpn/bin/piactl.

Help
piactl --help displays usage information.

Usage:piactl [options] command [parameters...]
Command-line interface to the PIA client. Some commands, such as connect, require that the graphical client is also running.

Options:
--timeout, -t <seconds> Sets timeout for one-shot commands.
--debug, -d Prints debug logs to stderr.
--help, -h Displays this help.
-v, --version Displays version information.

Arguments:
command Command to execute
parameters Parameters for the command

Commands
background
usage: background <enable|disable>
Allow the killswitch and/or VPN connection to remain active in the background when the GUI client is not running.
When enabled, the PIA daemon will stay active even if the GUI client is closed or has not been started.
This allows `piactl connect` to be used even if the GUI client is not running.
Disabling background activation will disconnect the VPN and deactivate killswitch if the GUI client is not running.
Disabling background activation will disconnect the VPN and deactivate killswitch if the GUI client is not running.

connect
Connects to the VPN, or reconnects to apply new settings.
The PIA client must be running to use this command.
(The PIA daemon is inactive when the client is not running.)

dedicatedip
usage (add): dedicatedip add <token_file>
usage (remove): dedicatedip remove <region_id>
Add or remove a Dedicated IP.
To add, put the dedicated IP token in a text file (by itself), and specify that file on the command line:
DIP20000000000000000000000000000
(This ensures the token is not visible in the process command line or environment.)
To remove, specify the dedicated IP region ID, as shown by `piactl get regions`, such as
`dedicated-sweden-000.000.000.000`.

disconnect
Disconnects from the VPN.

get
usage: get <type>
Get information from the PIA daemon.
Available types:

- connectionstate - VPN connection state
  values: Disconnected, Connecting, StillConnecting, Connected, Interrupted, Reconnecting, StillReconnecting, DisconnectingToReconnect, Disconnecting
- debuglogging - State of debug logging setting
- portforward - Forwarded port number if available, or the status of the request to forward a port
  values: [forwarded port], Inactive, Attempting, Failed, Unavailable
- region - Currently selected region (or "auto")
- regions - List all available regions
- vpnip - Current VPN IP address

login
usage: login
Log in to your PIA account.
Put your username and password on separate lines in a text file,
and specify that file on the command line:
p0000000
(yourpassword)

logout
Log out your PIA account on this computer.

monitor
usage: monitor <type>
Monitors the PIA daemon for changes in a specific setting or state value.
When a connection is established, the current value is printed.
When a change is received, the new value is printed.
Available types:

- connectionstate - VPN connection state
  values: Disconnected, Connecting, Still Connecting, Connected, Interrupted, Reconnecting, Still Reconnecting, Disconnecting To Reconnect, Disconnecting
- debuglogging - State of debug logging setting
- portforward - Forwarded port number if available, or the status of the request to forward a port
  values: [forwarded port], Inactive, Attempting, Failed, Unavailable
- region - Currently selected region (or "auto")
- vpnip - Current VPN IP address

resetsettings
Resets daemon settings to the defaults (ports/protocols/etc.)
Client settings (themes/icons/layouts) can't be set with the CLI.

set
usage: set <type> <value>
Change settings in the PIA daemon.
Available types:

- region - Select a region (or "auto")
  Commands

Option Description
--timeout <sec> / -t <sec> Specifies the timeout used for one-shot commands (default is 5 seconds). If the PIA daemon doesn't respond before this timeout, piactl exits unsuccessfully.
--debug / -d Displays debug output while executing piactl.
--help / -h Displays the help text.
--version / -v Displays the version of piactl.

piactl supports several commands:

Command Description
background Allow the killswitch and/or VPN connection to remain active in the background when the GUI client is not running.
connect Causes PIA to connect to the VPN, if it isn't already connected.
disconnect Causes PIA to disconnect from the VPN, if it is connected.
get <type> Gets information about PIA settings or state.
login <login_file>
Logs in to a PIA account.
logout
Logs out of a PIA account.
resetsettings Resets settings to the defaults. This only resets daemon settings (those that control the VPN connection), like protocols, ports, exclusions, etc. Graphical client settings (like the window type and icon theme) are not affected.
set <type> <value> Sets some of the values obtainable with get.
monitor <type> Monitors the PIA daemon for changes in a specific setting or state value.

The PIA client must be running to use the connect command. Otherwise, piactl will print a message and exit. This is currently required because the daemon is inactive when the graphical client is not running, and so the daemon can disconnect if the user logs out.
get/set types

Type

Can set?

Description

Values

`connectionstate`

No

VPN connection state

Disconnected, Connecting, Still Connecting, Connected, Interrupted, Reconnecting, Still Reconnecting, Disconnecting To Reconnect, Disconnecting

`debuglogging`

Yes

Whether debug logging is enabled

`true` or `false`

`portforward`

No

When connected, the forwarded port, or the status of the request to forward a port

Forwarded port value, or state indicator: `Inactive`, `Attempting`, `Failed`, `Unavailable`

`region`

Yes

The current selected region

Region identifier (see `get regions`) or `auto` for automatic region

`requestportforward`
Yes Enabling port forwarding Whether to request port forwarding after connecting
`protocol`
Yes Selects the VPN connection protocol VPN connection protocol - openvpn or wireguard
`regions`

No

Lists all available regions

Lists `auto` and all region identifiers

`vpnip`

No

The current VPN IP address, if connected and the address is known

IP address, or `Unknown`

`monitor` Types
Type

Description

Values

`connectionstate`

VPN connection state

Disconnected, Connecting, StillConnecting, Connected, Interrupted, Reconnecting, StillReconnecting, DisconnectingToReconnect, Disconnecting

`debuglogging`

State of debug logging setting

True or False

`portforward`

When connected, the forwarded port, or the status of the request to forward a port

[forwarded port], Inactive, Attempting, Failed, Unavailable

`region`

The current selected region

Currently selected region (or "auto")

`requestportforward`
Enabling port forwarding
Whether to request port forwarding after connecting
`protocol`
Selects the VPN connection protocol
VPN connection protocol - openvpn or wireguard
`vpnip`

The current VPN IP address, if connected and the address is known

Current VPN IP address

_Note_ The current monitor command will continue running until it is manually stopped by pressing Ctrl+C _Note_
