#!/usr/bin/env python3

import unittest

import cidrbrewer


class TestCIDRBrewer(unittest.TestCase):

    def test_get_subnet_mask(self):
        """Should compute the subnet mask."""
        self.assertEqual(
            cidrbrewer.get_subnet_mask(28),
            '11111111111111111111111111110000')

    def test_get_network_id(self):
        """Should compute the network ID of an IP address."""
        self.assertEqual(cidrbrewer.get_network_id(
            '11001000000101110001000001011100', 28),
            '11001000000101110001000001010000')

    def test_get_broadcast_id(self):
        """Should compute the broadcast ID of an IP address."""
        self.assertEqual(cidrbrewer.get_broadcast_id(
            '11001000000101110001000001011100', 28),
            '11001000000101110001000001011111')

    def test_get_first_available_addr(self):
        """Should compute the first available IP address."""
        self.assertEqual(cidrbrewer.get_first_available_addr(
            '11001000000101110001000001011100', 28),
            '11001000000101110001000001010001')

    def test_get_last_available_addr(self):
        """Should compute the last available IP address."""
        self.assertEqual(cidrbrewer.get_last_available_addr(
            '11001000000101110001000001011100', 28),
            '11001000000101110001000001011110')

    def test_prettify_bin_addr(self):
        """Should prettify a binary IP address."""
        self.assertEqual(cidrbrewer.prettify_bin_addr(
            '11001000000101110001000001011100'),
            '11001000.00010111.00010000.01011100')

    def test_get_prettified_dec_addr(self):
        """Should build a prettified decimal IP address"""
        self.assertEqual(cidrbrewer.get_prettified_dec_addr(
            '11001000000101110001000001011100'), '200.23.16.92')

    def test_get_subnet_size(self):
        """Should compute the size of the subnet."""
        self.assertEqual(cidrbrewer.get_subnet_size(28), 14)

    def test_is_reserved_addr(self):
        """Should determine that an unreserved IP address is unreserved."""
        self.assertEqual(cidrbrewer.is_reserved(
            '11001000000101110001000001011100', 28), False)

    def test_is_reserved_network_id(self):
        """Should determine that a network ID is reserved"""
        self.assertEqual(cidrbrewer.is_reserved(
            '11001000000101110001000001010000', 28), True)

    def test_is_reserved_broadcast_id(self):
        """Should determine that a broadcast ID is reserved"""
        self.assertEqual(cidrbrewer.is_reserved(
            '01111101001011110010000000101111', 28), True)

    def test_get_largest_subnet_mask(self):
        """Should compute the largest subnet mask for two IP addresses."""
        self.assertEqual(cidrbrewer.get_largest_subnet_mask(
            '01111101001011110010000000100001',
            '01111101001011110010000000101111'),
            '11111111111111111111111111100000')

if __name__ == '__main__':
    unittest.main()
