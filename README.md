# CIDR Brewer

*Copyright 2016 Caleb Evans*  
*Released under the MIT license*

[![Build Status](https://travis-ci.org/caleb531/cidr-brewer.svg?branch=master)](https://travis-ci.org/caleb531/cidr-brewer)
[![Coverage Status](https://coveralls.io/repos/caleb531/cidr-brewer/badge.svg?branch=master)](https://coveralls.io/r/caleb531/cidr-brewer?branch=master)

CIDR Brewer is a command-line utility which displays information for classless
IP addresses (such as subnet mask and network ID) so you don't need to perform
the calculations yourself.

## Installing

You can install CIDR Brewer via pip (ideally globally):

```
pip install cidr-brewer
```

## Usage

To use, run `cidr-brewer` from the command line with one or two IP addresses.

### One IP address

If you pass a single IP address using slash notation, CIDR Brewer will compute
the subnet mask, network ID, broadcast ID, and the range of valid/available IP
addresses.

```
$ cidr-brewer 192.168.19.100/25
Given IP address:
   192.168.19.100/25  11000000.10101000.00010011.01100100
Subnet mask:
   255.255.255.128    11111111.11111111.11111111.10000000
Network ID:
   192.168.19.0/25    11000000.10101000.00010011.00000000
Broadcast ID:
   192.168.19.127     11000000.10101000.00010011.01111111
First Available Address:
   192.168.19.1       11000000.10101000.00010011.00000001
Last Available Address:
   192.168.19.126     11000000.10101000.00010011.01111110
Subnet Size: 2^7 - 2 = 126
```

Additionally, if you supply a list of block sizes, CIDR Brewer will compute the
same information for each sub-block.

```
$ cidr-brewer 42.114.152.128/25 --block-sizes 16 64 16 32
Given IP address:
   42.114.152.128/25  00101010.01110010.10011000.10000000
Block 1:
   Block Size: 2^6 = 64
   Network ID:
      42.114.152.128/26  00101010.01110010.10011000.10000000
   Broadcast ID:
      42.114.152.191     00101010.01110010.10011000.10111111
   First Available Address:
      42.114.152.129     00101010.01110010.10011000.10000001
   Last Available Address:
      42.114.152.190     00101010.01110010.10011000.10111110
   Subnet Size: 2^6 - 2 = 62
Block 2:
   Block Size: 2^5 = 32
   Network ID:
      42.114.152.192/27  00101010.01110010.10011000.11000000
   Broadcast ID:
      42.114.152.223     00101010.01110010.10011000.11011111
   First Available Address:
      42.114.152.193     00101010.01110010.10011000.11000001
   Last Available Address:
      42.114.152.222     00101010.01110010.10011000.11011110
   Subnet Size: 2^5 - 2 = 30
Block 3:
   Block Size: 2^4 = 16
   Network ID:
      42.114.152.224/28  00101010.01110010.10011000.11100000
   Broadcast ID:
      42.114.152.239     00101010.01110010.10011000.11101111
   First Available Address:
      42.114.152.225     00101010.01110010.10011000.11100001
   Last Available Address:
      42.114.152.238     00101010.01110010.10011000.11101110
   Subnet Size: 2^4 - 2 = 14
Block 4:
   Block Size: 2^4 = 16
   Network ID:
      42.114.152.240/28  00101010.01110010.10011000.11110000
   Broadcast ID:
      42.114.152.255     00101010.01110010.10011000.11111111
   First Available Address:
      42.114.152.241     00101010.01110010.10011000.11110001
   Last Available Address:
      42.114.152.254     00101010.01110010.10011000.11111110
   Subnet Size: 2^4 - 2 = 14
```

### Two IP addresses

If you pass two IP addresses (without slash notation), CIDR Brewer will also
compute the largest subnet mask needed for communication between the two
addresses.

```
$ cidr-brewer 172.16.11.74 172.16.11.78
Given IP addresses:
   172.16.11.74       10101100.00010000.00001011.01001010
   172.16.11.78       10101100.00010000.00001011.01001110
Largest subnet mask allowing communication:
   29 bits
   255.255.255.248    11111111.11111111.11111111.11111000
Network ID:
   172.16.11.72/29    10101100.00010000.00001011.01001000
Broadcast ID:
   172.16.11.79       10101100.00010000.00001011.01001111
First Available Address:
   172.16.11.73       10101100.00010000.00001011.01001001
Last Available Address:
   172.16.11.78       10101100.00010000.00001011.01001110
Subnet Size: 2^3 - 2 = 6
```

If you pass two IP addresses (with slash notation), CIDR Brewer will also
indicate if the IP addresses can already communicate on their respective
subnets.

```
$ cidr-brewer 125.47.32.170/25 125.47.32.53/25
Given IP addresses:
   125.47.32.170/25   01111101.00101111.00100000.10101010
   125.47.32.53/25    01111101.00101111.00100000.00110101
Can these IP addresses communicate?
   No
Largest subnet mask allowing communication:
   24 bits
   255.255.255.0      11111111.11111111.11111111.00000000
Network ID:
   125.47.32.0/24     01111101.00101111.00100000.00000000
Broadcast ID:
   125.47.32.255      01111101.00101111.00100000.11111111
First Available Address:
   125.47.32.1        01111101.00101111.00100000.00000001
Last Available Address:
   125.47.32.254      01111101.00101111.00100000.11111110
Subnet Size: 2^8 - 2 = 254
```

## Examples

The `/examples` directory contains example IP addresses for you to test against
the utility.
