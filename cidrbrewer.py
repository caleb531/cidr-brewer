#!/usr/bin/env python3

import argparse
import functools
import math


# The number of spaces used per indentation level when displaying output
SPACES_PER_INDENT = 3


# Converts the given decimal number to a binary octet
def dec_to_bin_octet(dec_octet):
    # The bin() function returns a string prefixed with '0b'; strip it
    return bin(int(dec_octet))[2:].zfill(8)


# Adds a decimal number to a binary number
def add_dec_to_bin(bin_num, dec_num):
    return bin(int(bin_num, 2) + dec_num)[2:].zfill(len(bin_num))


# Splits a binary address into octets
def get_addr_octets(bin_addr):
    octets = []
    for i in range(0, len(bin_addr), 8):
        octets.append(bin_addr[i:i+8])
    return tuple(octets)


# Computes the subnet mask given the number of bits used for the subnet
def get_subnet_mask(num_subnet_bits):
    return ('1' * num_subnet_bits) + ('0' * (32 - num_subnet_bits))


# Computes the network ID given the binary address and the number of bits used
# for the subnet
def get_network_id(bin_addr, num_subnet_bits):
    return bin_addr[:num_subnet_bits].ljust(32, '0')


# Computes the broadcast ID given the binary address and the number of bits
# used for the subnet
def get_broadcast_id(bin_addr, num_subnet_bits):
    return bin_addr[:num_subnet_bits].ljust(32, '1')


# Computes the first available IP address in the defined subnet
def get_first_available_addr(bin_addr, num_subnet_bits):
    return get_network_id(bin_addr, num_subnet_bits)[:31] + '1'


# Computes the last available IP address in the defined subnet
def get_last_available_addr(bin_addr, num_subnet_bits):
    return get_broadcast_id(bin_addr, num_subnet_bits)[:31] + '0'


# Prettifies the given binary address by adding separating octets with dots
def prettify_bin_addr(bin_addr):
    return '.'.join(get_addr_octets(bin_addr))


# Converts a binary address to a prettified decimal address
def get_prettified_dec_addr(bin_addr):
    octets = get_addr_octets(bin_addr)
    return '.'.join(map(str, map(functools.partial(int, base=2), octets)))


# Computes the subnet size given the number of bits used for the subnet ID
def get_subnet_size(num_subnet_bits):
    return 2**(32 - num_subnet_bits) - 2


# Returns True if the given IP address is reserved; otherwise, returns False
def is_reserved(bin_addr, num_subnet_bits):
    host_part = bin_addr[num_subnet_bits:]
    return (host_part.count('1') == len(host_part) or
            host_part.count('0') == len(host_part))


# Computes the largest subnet mask that allows two IP addresses to communicate
def get_largest_subnet_mask(bin_addr_1, bin_addr_2):
    for i in reversed(range(31)):  # pragma: no branch
        bin_addr_1_left = bin_addr_1[:i]
        bin_addr_2_left = bin_addr_2[:i]
        if (bin_addr_1_left == bin_addr_2_left and
                not is_reserved(bin_addr_1, i) and
                not is_reserved(bin_addr_2, i)):
            break
    return get_subnet_mask(i)


# Indents the given output string
def indent(output, indent_level=1):
    return (' ' * indent_level * SPACES_PER_INDENT) + output


# Prints address for display in terminal
def print_addr(bin_addr, num_subnet_bits=None, indent_level=1):
    if num_subnet_bits is not None:
        prettified_dec_addr = '{}/{}'.format(
            get_prettified_dec_addr(bin_addr), num_subnet_bits)
    else:
        prettified_dec_addr = get_prettified_dec_addr(bin_addr)
    prettified_bin_addr = prettify_bin_addr(bin_addr)
    print(indent(
        '{:<18} {:<35}'.format(prettified_dec_addr, prettified_bin_addr),
        indent_level=indent_level))


# Parses the full address string by separating the address from the number of
# subnet bits
def parse_addr_str(addr_str):
    addr_str_parts = addr_str.split('/')
    bin_addr = ''.join(map(dec_to_bin_octet, addr_str_parts[0].split('.')))
    if len(addr_str_parts) == 2:
        num_subnet_bits = int(addr_str_parts[1])
    else:
        num_subnet_bits = None
    return bin_addr, num_subnet_bits


# Parses command-line arguments passed to the utility
def parse_cli_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('addr_str_1', metavar='ip_addr')
    parser.add_argument('addr_str_2', metavar='ip_addr', nargs='?')
    parser.add_argument('--block-sizes', type=int, nargs='*')
    parser.add_argument('--num-subnets', type=int)
    return parser.parse_args()


# Prints details (like network ID and broadcast ID) for the given IP address
def print_addr_details(bin_addr, num_subnet_bits, indent_level=0):

    print(indent('Network ID:', indent_level=indent_level))
    print_addr(
        get_network_id(bin_addr, num_subnet_bits),
        num_subnet_bits=num_subnet_bits,
        indent_level=indent_level + 1)

    print(indent('Broadcast ID:', indent_level=indent_level))
    print_addr(
        get_broadcast_id(bin_addr, num_subnet_bits),
        indent_level=indent_level + 1)

    print(indent('First Available Address:', indent_level=indent_level))
    print_addr(
        get_first_available_addr(bin_addr, num_subnet_bits),
        indent_level=indent_level + 1)

    print(indent('Last Available Address:', indent_level=indent_level))
    print_addr(
        get_last_available_addr(bin_addr, num_subnet_bits),
        indent_level=indent_level + 1)

    print(indent('Subnet Size: 2^{} - 2 = {}'.format(
        32 - num_subnet_bits, get_subnet_size(num_subnet_bits)),
        indent_level=indent_level))


# Prints 'Yes' or 'No' depending on whether or not two IP addresses can
# communicate on their respective subnets
def print_addrs_can_communicate(bin_addr_1, num_subnet_bits_1,
                                bin_addr_2, num_subnet_bits_2):

    if num_subnet_bits_1 is not None and num_subnet_bits_2 is not None:
        print('Can these IP addresses communicate?')
        network_id_1 = get_network_id(bin_addr_1, num_subnet_bits_1)
        network_id_2 = get_network_id(bin_addr_2, num_subnet_bits_2)
        if network_id_1 == network_id_2:
            print(indent('Yes'))
        else:
            print(indent('No'))


# Takes the appropriate action when two IP addresses are passed to the utility
def handle_two_addrs(addr_str_1, addr_str_2):

    bin_addr_1, num_subnet_bits_1 = parse_addr_str(addr_str_1)
    bin_addr_2, num_subnet_bits_2 = parse_addr_str(addr_str_2)

    print('Given IP addresses:')
    print_addr(bin_addr_1, num_subnet_bits_1)
    print_addr(bin_addr_2, num_subnet_bits_2)

    print_addrs_can_communicate(
        bin_addr_1, num_subnet_bits_1,
        bin_addr_2, num_subnet_bits_2)

    print('Largest subnet mask allowing communication:')
    largest_subnet_mask = get_largest_subnet_mask(bin_addr_1, bin_addr_2)
    num_subnet_bits = largest_subnet_mask.count('1')
    print(indent('{} bits'.format(num_subnet_bits), indent_level=1))
    print_addr(largest_subnet_mask)

    print_addr_details(bin_addr_1, num_subnet_bits)


def get_block_network_id(bin_addr, num_subnet_bits, block_size):
    subnet_part = bin_addr[:num_subnet_bits - 1]
    host_part = add_dec_to_bin(bin_addr[num_subnet_bits - 1:], block_size)
    return subnet_part + host_part


# Returns a list of blocks, where each block is a tuple containing its size,
# network ID, and number of subnet bits
def get_blocks(bin_addr, num_subnet_bits, block_sizes):

    prev_block_size = 0
    block_network_id = bin_addr
    blocks = []
    for block_size in reversed(sorted(block_sizes)):

        num_block_subnet_bits = 32 - int(math.log2(block_size))
        block_network_id = get_block_network_id(
            block_network_id, num_subnet_bits, prev_block_size)
        blocks.append(
            (block_size, block_network_id, num_block_subnet_bits))
        prev_block_size = block_size

    return blocks


# Prints details for every sub-block created from an IP address and a sequence
# of block sizes
def print_blocks(bin_addr, num_subnet_bits, block_sizes):

    blocks = get_blocks(bin_addr, num_subnet_bits, block_sizes)
    for block_num, (block_size, block_network_id, num_block_subnet_bits) in \
            enumerate(blocks, 1):
        print('Block {}:'.format(block_num))
        print(indent('Block Size: 2^{} = {}'.format(
            int(math.log2(block_size)), block_size)))
        print_addr_details(
            block_network_id, num_block_subnet_bits, indent_level=1)


# Takes the appropriate action when one IP address is passed to the utility
def handle_one_addr(addr_str, block_sizes=None):

    bin_addr, num_subnet_bits = parse_addr_str(addr_str)

    print('Given IP address:')
    print_addr(bin_addr, num_subnet_bits)

    if block_sizes:
        print_blocks(bin_addr, num_subnet_bits, block_sizes)
    else:
        print('Subnet mask:')
        print_addr(get_subnet_mask(num_subnet_bits))
        print_addr_details(bin_addr, num_subnet_bits)


def main():

    cli_args = parse_cli_args()
    if cli_args.addr_str_2:
        handle_two_addrs(cli_args.addr_str_1, cli_args.addr_str_2)
    else:
        handle_one_addr(cli_args.addr_str_1, cli_args.block_sizes)


if __name__ == '__main__':
    main()
