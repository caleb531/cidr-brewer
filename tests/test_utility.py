#!/usr/bin/env python3

import unittest

import cidrbrewer.__main__ as cidrbrewer


class TestUtility(unittest.TestCase):
    def test_get_subnet_mask(self):
        """Should compute the subnet mask."""
        self.assertEqual(
            cidrbrewer.get_subnet_mask(28), "11111111111111111111111111110000"
        )

    def test_get_network_id(self):
        """Should compute the network ID of an IP address."""
        self.assertEqual(
            cidrbrewer.get_network_id("11001000000101110001000001011100", 28),
            "11001000000101110001000001010000",
        )

    def test_get_broadcast_id(self):
        """Should compute the broadcast ID of an IP address."""
        self.assertEqual(
            cidrbrewer.get_broadcast_id("11001000000101110001000001011100", 28),
            "11001000000101110001000001011111",
        )

    def test_get_first_available_addr(self):
        """Should compute the first available IP address."""
        self.assertEqual(
            cidrbrewer.get_first_available_addr("11001000000101110001000001011100", 28),
            "11001000000101110001000001010001",
        )

    def test_get_last_available_addr(self):
        """Should compute the last available IP address."""
        self.assertEqual(
            cidrbrewer.get_last_available_addr("11001000000101110001000001011100", 28),
            "11001000000101110001000001011110",
        )

    def test_prettify_bin_addr(self):
        """Should prettify a binary IP address."""
        self.assertEqual(
            cidrbrewer.prettify_bin_addr("11001000000101110001000001011100"),
            "11001000.00010111.00010000.01011100",
        )

    def test_get_prettified_dec_addr(self):
        """Should build a prettified decimal IP address."""
        self.assertEqual(
            cidrbrewer.get_prettified_dec_addr("11001000000101110001000001011100"),
            "200.23.16.92",
        )

    def test_get_subnet_size(self):
        """Should compute the size of the subnet."""
        self.assertEqual(cidrbrewer.get_subnet_size(28), 14)

    def test_is_reserved_addr(self):
        """Should determine that an unreserved IP address is unreserved."""
        self.assertEqual(
            cidrbrewer.is_reserved("11001000000101110001000001011100", 28), False
        )

    def test_is_reserved_network_id(self):
        """Should determine that a network ID is reserved."""
        self.assertEqual(
            cidrbrewer.is_reserved("11001000000101110001000001010000", 28), True
        )

    def test_is_reserved_broadcast_id(self):
        """Should determine that a broadcast ID is reserved."""
        self.assertEqual(
            cidrbrewer.is_reserved("01111101001011110010000000101111", 28), True
        )

    def test_get_largest_subnet_mask(self):
        """Should compute the largest subnet mask for two IP addresses."""
        self.assertEqual(
            cidrbrewer.get_largest_subnet_mask(
                "01111101001011110010000000100001", "01111101001011110010000000101111"
            ),
            "11111111111111111111111111100000",
        )

    def test_get_largest_subnet_mask_same_addr(self):
        """Should compute the largest subnet mask for the same IP address."""
        self.assertEqual(
            cidrbrewer.get_largest_subnet_mask(
                "01111101001011110010000000101010", "01111101001011110010000000101010"
            ),
            "11111111111111111111111111111100",
        )

    def test_indent(self):
        """Should indent the given output by the given indent level."""
        self.assertEqual(
            cidrbrewer.indent("IP Address:", indent_level=2),
            "{}IP Address:".format(" " * 6),
        )

    def test_parse_addr_str(self):
        """Should parse an IP address string not in slash notation."""
        self.assertEqual(
            cidrbrewer.parse_addr_str("192.168.19.100"),
            ("11000000101010000001001101100100", None),
        )

    def test_parse_addr_str_slash_notation(self):
        """Should parse an IP address string in slash notation."""
        self.assertEqual(
            cidrbrewer.parse_addr_str("192.168.19.100/26"),
            ("11000000101010000001001101100100", 26),
        )

    def test_get_block_network_id(self):
        """Should compute the network ID of a block."""
        self.assertEqual(
            cidrbrewer.get_block_network_id(
                "00010000001000111001110110000000", num_subnet_bits=26, block_size=16
            ),
            "00010000001000111001110110010000",
        )

    def test_get_blocks(self):
        """Should compute the list of data for each block."""
        self.assertEqual(
            cidrbrewer.get_blocks(
                "00010000001000111001110110000000",
                num_subnet_bits=26,
                block_sizes=(16, 64, 16, 32),
            ),
            [
                (64, "00010000001000111001110110000000", 26),
                (32, "00010000001000111001110111000000", 27),
                (16, "00010000001000111001110111100000", 28),
                (16, "00010000001000111001110111110000", 28),
            ],
        )
