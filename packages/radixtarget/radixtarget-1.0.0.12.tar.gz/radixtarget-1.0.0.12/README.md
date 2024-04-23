# RadixTarget

[![Python Version](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org) [![License](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://github.com/blacklanternsecurity/radixtarget/blob/master/LICENSE) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Tests](https://github.com/blacklanternsecurity/radixtarget/actions/workflows/tests.yml/badge.svg?branch=stable)](https://github.com/blacklanternsecurity/radixtarget/actions?query=workflow%3A"tests") [![Codecov](https://codecov.io/gh/blacklanternsecurity/radixtarget/branch/dev/graph/badge.svg?token=IR5AZBDM5K)](https://codecov.io/gh/blacklanternsecurity/radixtarget)

RadixTarget is a performant radix implementation designed for quick lookups of IP addresses/networks and DNS hostnames. Written in pure python and capable of roughly 100,000 lookups per second regardless of the size of the database.

Used by:
- [BBOT (Bighuge BLS OSINT Tool)](https://github.com/blacklanternsecurity/bbot)
- [cloudcheck](https://github.com/blacklanternsecurity/cloudcheck)

### Installation ([PyPi](https://pypi.org/project/radixtarget/))

```bash
pip install radixtarget
```

### Example Usage

```python
from radixtarget import RadixTarget

rt = RadixTarget()

# IPv4
rt.insert("192.168.1.0/24")
rt.search("192.168.1.10") # ipaddress.ip_network("192.168.1.0/24")
rt.search("192.168.2.10") # None

# ipv6
rt.insert("dead::/64")
rt.search("dead::beef") # ipaddress.ip_network("dead::/64")
rt.search("dead:cafe::beef") # None

# DNS
rt.insert("net")
rt.insert("www.example.com")
rt.insert("test.www.example.com")

rt.search("net") # "net"
rt.search("evilcorp.net") # "net"
rt.search("www.example.com") # "www.example.com"
rt.search("asdf.test.www.example.com") # "test.www.example.com"
rt.search("example.com") # None
```