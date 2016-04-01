#!/usr/bin/env python3

import contextlib
import io
import re
from unittest.mock import call, patch

import nose.tools as nose

import cidrbrewer


def test_get_subnet_mask():
    """Should compute the subnet mask."""
    nose.assert_equal(
        cidrbrewer.get_subnet_mask(28),
        '11111111111111111111111111110000')


def test_get_network_id():
    """Should compute the network ID of an IP address."""
    nose.assert_equal(cidrbrewer.get_network_id(
        '11001000000101110001000001011100', 28),
        '11001000000101110001000001010000')


def test_get_broadcast_id():
    """Should compute the broadcast ID of an IP address."""
    nose.assert_equal(cidrbrewer.get_broadcast_id(
        '11001000000101110001000001011100', 28),
        '11001000000101110001000001011111')


def test_get_first_available_addr():
    """Should compute the first available IP address."""
    nose.assert_equal(cidrbrewer.get_first_available_addr(
        '11001000000101110001000001011100', 28),
        '11001000000101110001000001010001')


def test_get_last_available_addr():
    """Should compute the last available IP address."""
    nose.assert_equal(cidrbrewer.get_last_available_addr(
        '11001000000101110001000001011100', 28),
        '11001000000101110001000001011110')


def test_prettify_bin_addr():
    """Should prettify a binary IP address."""
    nose.assert_equal(cidrbrewer.prettify_bin_addr(
        '11001000000101110001000001011100'),
        '11001000.00010111.00010000.01011100')


def test_get_prettified_dec_addr():
    """Should build a prettified decimal IP address."""
    nose.assert_equal(cidrbrewer.get_prettified_dec_addr(
        '11001000000101110001000001011100'), '200.23.16.92')


def test_get_subnet_size():
    """Should compute the size of the subnet."""
    nose.assert_equal(cidrbrewer.get_subnet_size(28), 14)


def test_is_reserved_addr():
    """Should determine that an unreserved IP address is unreserved."""
    nose.assert_equal(cidrbrewer.is_reserved(
        '11001000000101110001000001011100', 28), False)


def test_is_reserved_network_id():
    """Should determine that a network ID is reserved."""
    nose.assert_equal(cidrbrewer.is_reserved(
        '11001000000101110001000001010000', 28), True)


def test_is_reserved_broadcast_id():
    """Should determine that a broadcast ID is reserved."""
    nose.assert_equal(cidrbrewer.is_reserved(
        '01111101001011110010000000101111', 28), True)


def test_get_largest_subnet_mask():
    """Should compute the largest subnet mask for two IP addresses."""
    nose.assert_equal(cidrbrewer.get_largest_subnet_mask(
        '01111101001011110010000000100001',
        '01111101001011110010000000101111'),
        '11111111111111111111111111100000')


def test_get_largest_subnet_mask_same_addr():
    """Should compute the largest subnet mask for the same IP address."""
    nose.assert_equal(cidrbrewer.get_largest_subnet_mask(
        '01111101001011110010000000101010',
        '01111101001011110010000000101010'),
        '11111111111111111111111111111100')


def test_indent():
    """Should indent the given output by the given indent level."""
    nose.assert_equal(
        cidrbrewer.indent('IP Address:', indent_level=2),
        '{}IP Address:'.format(' ' * 6))


def test_print_addr():
    """Should print IP address in decimal and binary formats."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        cidrbrewer.print_addr(
            '11001000000101110001000001011100',
            indent_level=2)
    nose.assert_equal(
        out.getvalue().rstrip(),
        '{}200.23.16.92{}11001000.00010111.00010000.01011100'.format(
            ' ' * 6, ' ' * 7))


def test_print_addr_num_subnet_bits():
    """Should print IP address in decimal slash and binary formats."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        cidrbrewer.print_addr(
            '11001000000101110001000001011100',
            num_subnet_bits=26,
            indent_level=2)
    nose.assert_equal(
        out.getvalue().rstrip(),
        '{}200.23.16.92/26{}11001000.00010111.00010000.01011100'.format(
            ' ' * 6, ' ' * 4))


def test_parse_addr_str():
    """Should parse an IP address string not in slash notation."""
    nose.assert_equal(
        cidrbrewer.parse_addr_str('192.168.19.100'),
        ('11000000101010000001001101100100', None))


def test_parse_addr_str_slash_notation():
    """Should parse an IP address string in slash notation."""
    nose.assert_equal(
        cidrbrewer.parse_addr_str('192.168.19.100/26'),
        ('11000000101010000001001101100100', 26))


def test_print_addr_details():
    """Should print IP address details (subnet mask, network ID, etc.)"""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        cidrbrewer.print_addr_details(
            '11000000101010000001001101100100',
            num_subnet_bits=25)
    output = out.getvalue()
    nose.assert_regexp_matches(output, r'{}\n\s+{}\s+{}'.format(
        'Network ID:', r'192\.168\.19\.0/25',
        '11000000.10101000.00010011.00000000'),
        'Network ID not printed')
    nose.assert_regexp_matches(output, r'{}\n\s+{}\s+{}'.format(
        'Broadcast ID:', r'192\.168\.19\.127',
        '11000000.10101000.00010011.01111111'),
        'Broadcast ID not printed')
    nose.assert_regexp_matches(output, r'{}\n\s+{}\s+{}'.format(
        'First Available Address:', r'192\.168\.19\.1',
        '11000000.10101000.00010011.00000001'),
        'First available address not printed')
    nose.assert_regexp_matches(output, r'{}\n\s+{}\s+{}'.format(
        'Last Available Address:', r'192\.168\.19\.126',
        '11000000.10101000.00010011.01111110'),
        'Last available address not printed')


@patch('cidrbrewer.print_addr_details')
def test_handle_two_addrs(print_addr_details):
    """Should display information for two IP addresses."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        cidrbrewer.handle_two_addrs('172.16.11.74', '172.16.11.78')
    output = out.getvalue()
    nose.assert_regexp_matches(output, r'{}\n\s+{}\s+{}\n\s+{}\s+{}'.format(
        'Given IP addresses:', r'172\.16\.11\.74',
        '10101100.00010000.00001011.01001010',
        r'172\.16\.11\.78', '10101100.00010000.00001011.01001110'),
        'Given IP addresses not printed')
    nose.assert_regexp_matches(output, r'{}\n\s+{}\n\s+{}\s+{}'.format(
        'Largest subnet mask [^:]+:', '29 bits',
        r'255\.255\.255\.248', '11111111.11111111.11111111.11111000'),
        'Largest subnet mask not printed')
    print_addr_details.assert_called_once_with(
        '10101100000100000000101101001010', 29)


@patch('cidrbrewer.print_addr_details')
def test_handle_two_addrs_slash_notation_communicate_no(print_addr_details):
    """Should print info for two IP addresses in slash notation."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        cidrbrewer.handle_two_addrs('125.47.32.170/25', '125.47.32.53/25')
    output = out.getvalue()
    nose.assert_regexp_matches(output, r'{}\n\s+{}\s+{}\n\s+{}\s+{}'.format(
        'Given IP addresses:', r'125\.47\.32\.170/25',
        '01111101.00101111.00100000.10101010',
        r'125\.47\.32\.53/25', '01111101.00101111.00100000.00110101'),
        'Given IP addresses not printed')
    nose.assert_regexp_matches(output, r'{}\n\s+{}'.format(
        r'Can these IP addresses communicate\?', 'No'),
        '"Can communicate" message not printed')
    print_addr_details.assert_called_once_with(
        '01111101001011110010000010101010', 24)


@patch('cidrbrewer.print_addr_details')
def test_handle_two_addrs_slash_notation_communicate_yes(print_addr_details):
    """Should print info for two same-subnet IP addresses in slash notation."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        cidrbrewer.handle_two_addrs('125.47.32.170/24', '125.47.32.53/24')
    output = out.getvalue()
    nose.assert_regexp_matches(output, r'{}\n\s+{}\s+{}\n\s+{}\s+{}'.format(
        'Given IP addresses:', r'125\.47\.32\.170/24',
        '01111101.00101111.00100000.10101010',
        r'125\.47\.32\.53/24', '01111101.00101111.00100000.00110101'),
        'Given IP addresses not printed')
    nose.assert_regexp_matches(output, r'{}\n\s+{}'.format(
        r'Can these IP addresses communicate\?', 'Yes'),
        '"Can communicate" message not printed')
    print_addr_details.assert_called_once_with(
        '01111101001011110010000010101010', 24)


def test_get_block_network_id():
    """Should compute the network ID of a block."""
    nose.assert_equal(cidrbrewer.get_block_network_id(
        '00010000001000111001110110000000',
        num_subnet_bits=26,
        block_size=16),
        '00010000001000111001110110010000')


def test_get_blocks():
    """Should compute the list of data for each block."""
    nose.assert_equal(cidrbrewer.get_blocks(
        '00010000001000111001110110000000',
        num_subnet_bits=26,
        block_sizes=(16, 64, 16, 32)),
        [
            (64, '00010000001000111001110110000000', 26),
            (32, '00010000001000111001110111000000', 27),
            (16, '00010000001000111001110111100000', 28),
            (16, '00010000001000111001110111110000', 28)
        ])


@patch('cidrbrewer.print_addr_details')
def test_print_blocks(print_addr_details):
    """Should print details for IP address blocks."""
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        cidrbrewer.print_blocks(
            '00101010011100101001100010000000',
            num_subnet_bits=25,
            block_sizes=(16, 64, 16, 32))
    output = out.getvalue()
    block_1_matches = re.search(r'{}\n\s+{}'.format(
        'Block 1:', r'Block Size: 2\^6 = 64'), output)
    block_2_matches = re.search(r'{}\n\s+{}'.format(
        'Block 2:', r'Block Size: 2\^5 = 32'), output)
    block_3_matches = re.search(r'{}\n\s+{}'.format(
        'Block 3:', r'Block Size: 2\^4 = 16'), output)
    block_4_matches = re.search(r'{}\n\s+{}'.format(
        'Block 4:', r'Block Size: 2\^4 = 16'), output)
    nose.assert_less(block_1_matches.start(0), block_2_matches.start(0))
    nose.assert_less(block_2_matches.start(0), block_3_matches.start(0))
    nose.assert_less(block_3_matches.start(0), block_4_matches.start(0))
    nose.assert_equal(print_addr_details.call_args_list, [
        call('00101010011100101001100010000000', 26, indent_level=1),
        call('00101010011100101001100011000000', 27, indent_level=1),
        call('00101010011100101001100011100000', 28, indent_level=1),
        call('00101010011100101001100011110000', 28, indent_level=1)
    ])
