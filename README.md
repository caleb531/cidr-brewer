# CIDR Brewer

*Copyright 2016 Caleb Evans*  
*Released under the MIT license*

CIDR Brewer is a command-line utility which displays information for classless
IP addresses (such as subnet mask and network ID) so you don't need to perform
the calculations yourself.

## Usage.

To use, run `./cidrbrewer.py` from the command line with one or two IP
addresses. The program will run slightly differently depending on how many IP
addresses you supply:

If you pass a single IP address using slash notation, CIDR Brewer will compute
the subnet mask, network ID, broadcast ID, and the range of valid/available IP
addresses.

```bash
$ ./cidrbrewer.py 192.168.19.100/25
Given IP addresses:
   192.168.19.100   11000000.10101000.00010011.01100100
Subnet mask:
   255.255.255.128  11111111.11111111.11111111.10000000
Network ID:
   192.168.19.0     11000000.10101000.00010011.00000000
Broadcast ID:
   192.168.19.127   11000000.10101000.00010011.01111111
First Available Address:
   192.168.19.1     11000000.10101000.00010011.00000001
Last Available Address:
   192.168.19.126   11000000.10101000.00010011.01111110
Subnet Size: 2^7 - 2 = 126
```

If you pass two IP addresses (without slash notation), CIDR Brewer will compute
the largest subnet mask needed for communication between the two addresses. The
utility will still compute the network ID, broadcast ID, and the range of
valid/available IP addresses.

```bash
$ ./cidrbrewer.py 172.16.11.74 172.16.11.78
Given IP addresses:
   172.16.11.74     10101100.00010000.00001011.01001010
   172.16.11.78     10101100.00010000.00001011.01001110
Largest subnet mask:
   29 bits
   255.255.255.248  11111111.11111111.11111111.11111000
Network ID:
   172.16.11.72     10101100.00010000.00001011.01001000
Broadcast ID:
   172.16.11.79     10101100.00010000.00001011.01001111
First Available Address:
   172.16.11.73     10101100.00010000.00001011.01001001
Last Available Address:
   172.16.11.78     10101100.00010000.00001011.01001110
Subnet Size: 2^3 - 2 = 6
```

## Examples

The `/examples` directory contains example IP addresses for you to test against
the utility.
