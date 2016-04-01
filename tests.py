#!/usr/bin/env python3

import contextlib
import io

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
            num_subnet_bits=25,
            indent_level=2)
        nose.assert_regexp_matches(out.getvalue(), r'{}\n\s+{}\s+{}'.format(
            'Network ID:', '192.168.19.0/25',
            '11000000.10101000.00010011.00000000'),
            'Network ID not printed')
        nose.assert_regexp_matches(out.getvalue(), r'{}\n\s+{}\s+{}'.format(
            'Broadcast ID:', '192.168.19.127',
            '11000000.10101000.00010011.01111111'),
            'Broadcast ID not printed')
        nose.assert_regexp_matches(out.getvalue(), r'{}\n\s+{}\s+{}'.format(
            'First Available Address:', '192.168.19.1',
            '11000000.10101000.00010011.00000001'),
            'First available address not printed')
        nose.assert_regexp_matches(out.getvalue(), r'{}\n\s+{}\s+{}'.format(
            'Last Available Address:', '192.168.19.126',
            '11000000.10101000.00010011.01111110'),
            'Last available address not printed')


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
