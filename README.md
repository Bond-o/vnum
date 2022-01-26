# VNUM
![alt text](https://img.shields.io/badge/Python-3_only-blue.svg "Python 3 only") [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

Enumerates Cisco CallManager LDAP Users.

# ABOUT
VNUM is a Python3 script that enumerates Cisco CallManager LDAP users with AXL or UDS API connectivity.

# USAGE
```
usage: vnum.py [-h] -t TARGET [-p PORT] [-a {1,2} API]

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -t TARGET, --target TARGET
                        Target CUCM Host IP Address
  -p PORT, --port PORT  Target CUCM TCP Port
  -a {1,2} API, --api API
                        Choose one of the following:
                        1 = CUCM AXL API
                        2 = CUCM UDS API
```

## Examples
```
./vnum.py -t 192.168.1.10 -p 443 -a 2
```


# Disclaimer
This project is intended for network administrators, security researchers, and penetration testers and should not be used for any illegal activities.

