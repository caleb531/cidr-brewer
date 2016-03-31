# CIDR Brewer

*Copyright 2016 Caleb Evans*  
*Released under the MIT license*

CIDR Brewer is a command-line utility which displays information for classless
IP addresses (such as subnet mask and network ID) so you don't need to perform
the calculations yourself.

## Usage

To use, run `./cidrbrewer.py` from the command line with one or two IP
addresses.

### One IP address

If you pass a single IP address using slash notation, CIDR Brewer will compute
the subnet mask, network ID, broadcast ID, and the range of valid/available IP
addresses.

```
$ ./cidrbrewer.py 192.168.19.100/25
Given IP address:
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

If you also pass a list of block sizes, CIDR Brewer will compute the network ID
of each sub-block.

```
cidr-brewer : master : $ ./cidrbrewer.py 42.114.152.128/25 --block-sizes 16 64 16 32
Given IP address:
   42.114.152.128/25  00101010.01110010.10011000.10000000
Block 1:
   Block Size: 64
   Network ID:
      42.114.152.128/26  00101010.01110010.10011000.10000000
Block 2:
   Block Size: 32
   Network ID:
      42.114.152.192/27  00101010.01110010.10011000.11000000
Block 3:
   Block Size: 16
   Network ID:
      42.114.152.224/28  00101010.01110010.10011000.11100000
Block 4:
   Block Size: 16
   Network ID:
      42.114.152.240/28  00101010.01110010.10011000.11110000
```

### Two IP addresses

If you pass two IP addresses (without slash notation), CIDR Brewer will also
compute the largest subnet mask needed for communication between the two
addresses.

```
$ ./cidrbrewer.py 172.16.11.74 172.16.11.78
Given IP addresses:
   172.16.11.74     10101100.00010000.00001011.01001010
   172.16.11.78     10101100.00010000.00001011.01001110
Largest subnet mask allowing communication
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

If you pass two IP addresses (with slash notation), CIDR Brewer will also
indicate if the IP addresses can already communicate on their respective
subnets.

```
$ ./cidrbrewer.py 125.47.32.170/25 125.47.32.53/25
Given IP addresses:
   125.47.32.170    01111101.00101111.00100000.10101010
   125.47.32.53     01111101.00101111.00100000.00110101
Can these IP addresses communicate?
   No
Largest subnet mask allowing communication
   24 bits
   255.255.255.0    11111111.11111111.11111111.00000000
Network ID:
   125.47.32.0      01111101.00101111.00100000.00000000
Broadcast ID:
   125.47.32.255    01111101.00101111.00100000.11111111
First Available Address:
   125.47.32.1      01111101.00101111.00100000.00000001
Last Available Address:
   125.47.32.254    01111101.00101111.00100000.11111110
Subnet Size: 2^8 - 2 = 254
```

## Examples

The `/examples` directory contains example IP addresses for you to test against
the utility.
