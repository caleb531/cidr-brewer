#!/usr/bin/env python3

import contextlib
import io
import re
import unittest
from unittest.mock import call, patch

import cidrbrewer.__main__ as main


class TestUtilityDisplay(unittest.TestCase):
    def test_print_addr(self):
        """Should print IP address in decimal and binary formats."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            main.print_addr("11001000000101110001000001011100", indent_level=2)
        self.assertEqual(
            out.getvalue().rstrip(),
            "{}200.23.16.92{}11001000.00010111.00010000.01011100".format(
                " " * 6, " " * 7
            ),
        )

    def test_print_addr_num_subnet_bits(self):
        """Should print IP address in decimal slash and binary formats."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            main.print_addr(
                "11001000000101110001000001011100", num_subnet_bits=26, indent_level=2
            )
        self.assertEqual(
            out.getvalue().rstrip(),
            "{}200.23.16.92/26{}11001000.00010111.00010000.01011100".format(
                " " * 6, " " * 4
            ),
        )

    def test_print_addr_details(self):
        """Should print IP address details (subnet mask, network ID, etc.)"""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            main.print_addr_details(
                "11000000101010000001001101100100", num_subnet_bits=25
            )
        output = out.getvalue()
        self.assertRegex(
            output,
            r"{}\n\s+{}\s+{}".format(
                "Network ID:",
                r"192\.168\.19\.0/25",
                r"11000000\.10101000\.00010011\.00000000",
            ),
            "Network ID not printed",
        )
        self.assertRegex(
            output,
            r"{}\n\s+{}\s+{}".format(
                "Broadcast ID:",
                r"192\.168\.19\.127",
                r"11000000\.10101000\.00010011\.01111111",
            ),
            "Broadcast ID not printed",
        )
        self.assertRegex(
            output,
            r"{}\n\s+{}\s+{}".format(
                "First Available Address:",
                r"192\.168\.19\.1",
                r"11000000\.10101000\.00010011\.00000001",
            ),
            "First available address not printed",
        )
        self.assertRegex(
            output,
            r"{}\n\s+{}\s+{}".format(
                "Last Available Address:",
                r"192\.168\.19\.126",
                r"11000000\.10101000\.00010011\.01111110",
            ),
            "Last available address not printed",
        )

    @patch("cidrbrewer.__main__.print_addr_details")
    def test_handle_two_addrs(self, print_addr_details):
        """Should display information for two IP addresses."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            main.handle_two_addrs("172.16.11.74", "172.16.11.78")
        output = out.getvalue()
        self.assertRegex(
            output,
            r"{}\n\s+{}\s+{}\n\s+{}\s+{}".format(
                "Given IP addresses:",
                r"172\.16\.11\.74",
                r"10101100\.00010000\.00001011\.01001010",
                r"172\.16\.11\.78",
                r"10101100\.00010000\.00001011\.01001110",
            ),
            "Given IP addresses not printed",
        )
        self.assertRegex(
            output,
            r"{}\n\s+{}\n\s+{}\s+{}".format(
                "Largest subnet mask [^:]+:",
                "29 bits",
                r"255\.255\.255\.248",
                r"11111111\.11111111\.11111111\.11111000",
            ),
            "Largest subnet mask not printed",
        )
        print_addr_details.assert_called_once_with(
            "10101100000100000000101101001010", 29
        )

    @patch("cidrbrewer.__main__.print_addr_details")
    def test_handle_two_addrs_slash_notation_communicate_no(self, print_addr_details):
        """Should print info for two IP addresses in slash notation."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            main.handle_two_addrs("125.47.32.170/25", "125.47.32.53/25")
        output = out.getvalue()
        self.assertRegex(
            output,
            r"{}\n\s+{}\s+{}\n\s+{}\s+{}".format(
                "Given IP addresses:",
                r"125\.47\.32\.170/25",
                r"01111101\.00101111\.00100000\.10101010",
                r"125\.47\.32\.53/25",
                r"01111101\.00101111\.00100000\.00110101",
            ),
            "Given IP addresses not printed",
        )
        self.assertRegex(
            output,
            r"{}\n\s+{}".format(r"Can these IP addresses communicate\?", "No"),
            '"Can communicate" message not printed',
        )
        print_addr_details.assert_called_once_with(
            "01111101001011110010000010101010", 24
        )

    @patch("cidrbrewer.__main__.print_addr_details")
    def test_handle_two_addrs_slash_notation_communicate_yes(self, print_addr_details):
        """
        Should print info for two same-subnet IP addresses in slash notation.
        """
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            main.handle_two_addrs("125.47.32.170/24", "125.47.32.53/24")
        output = out.getvalue()
        self.assertRegex(
            output,
            r"{}\n\s+{}\s+{}\n\s+{}\s+{}".format(
                "Given IP addresses:",
                r"125\.47\.32\.170/24",
                r"01111101\.00101111\.00100000\.10101010",
                r"125\.47\.32\.53/24",
                r"01111101\.00101111\.00100000\.00110101",
            ),
            "Given IP addresses not printed",
        )
        self.assertRegex(
            output,
            r"{}\n\s+{}".format(r"Can these IP addresses communicate\?", "Yes"),
            '"Can communicate" message not printed',
        )
        print_addr_details.assert_called_once_with(
            "01111101001011110010000010101010", 24
        )

    @patch("cidrbrewer.__main__.print_addr_details")
    def test_print_blocks(self, print_addr_details):
        """Should print details for IP address blocks."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            main.print_blocks(
                "00101010011100101001100010000000",
                num_subnet_bits=25,
                block_sizes=(16, 64, 16, 32),
            )
        output = out.getvalue()
        block_1_matches = re.search(
            r"{}\n\s+{}".format("Block 1:", r"Block Size: 2\^6 = 64"), output
        )
        block_2_matches = re.search(
            r"{}\n\s+{}".format("Block 2:", r"Block Size: 2\^5 = 32"), output
        )
        block_3_matches = re.search(
            r"{}\n\s+{}".format("Block 3:", r"Block Size: 2\^4 = 16"), output
        )
        block_4_matches = re.search(
            r"{}\n\s+{}".format("Block 4:", r"Block Size: 2\^4 = 16"), output
        )
        self.assertLess(block_1_matches.start(0), block_2_matches.start(0))
        self.assertLess(block_2_matches.start(0), block_3_matches.start(0))
        self.assertLess(block_3_matches.start(0), block_4_matches.start(0))
        self.assertEqual(
            print_addr_details.call_args_list,
            [
                call("00101010011100101001100010000000", 26, indent_level=1),
                call("00101010011100101001100011000000", 27, indent_level=1),
                call("00101010011100101001100011100000", 28, indent_level=1),
                call("00101010011100101001100011110000", 28, indent_level=1),
            ],
        )

    @patch("cidrbrewer.__main__.print_addr_details")
    def test_handle_one_addr(self, print_addr_details):
        """Should display information for one IP address."""
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            main.handle_one_addr("192.168.19.100/25")
        output = out.getvalue()
        self.assertRegex(
            output,
            r"{}\n\s+{}\s+{}".format(
                "Given IP address:",
                r"192\.168\.19\.100/25",
                r"11000000\.10101000\.00010011\.01100100",
            ),
            "Given IP address not printed",
        )
        self.assertRegex(
            output,
            r"{}\n\s+{}\s+{}".format(
                "Subnet mask:",
                r"255\.255\.255\.128",
                r"11111111\.11111111\.11111111\.10000000",
            ),
            "Subnet mask not printed",
        )
        print_addr_details.assert_called_once_with(
            "11000000101010000001001101100100", 25
        )

    @patch("cidrbrewer.__main__.print_blocks")
    def test_handle_one_addr_block_sizes(self, print_blocks):
        """
        Should display information for one IP address and given block sizes.
        """
        with contextlib.redirect_stdout(None):
            main.handle_one_addr("192.168.19.100/25", [16, 64, 16, 32])
        print_blocks.assert_called_once_with(
            "11000000101010000001001101100100", 25, [16, 64, 16, 32]
        )

    @patch("cidrbrewer.__main__.handle_one_addr")
    @patch("sys.argv", [__file__, "192.168.19.100/25"])
    def test_main_one_addr(self, handle_one_addr):
        """Should handle one IP address when running main function."""
        with contextlib.redirect_stdout(None):
            main.main()
        handle_one_addr.assert_called_once_with("192.168.19.100/25", None)

    @patch("cidrbrewer.__main__.handle_two_addrs")
    @patch("sys.argv", [__file__, "125.47.32.170/25", "125.47.32.53/25"])
    def test_main_two_addrs(self, handle_two_addrs):
        """Should handle two IP addresses when running main function."""
        with contextlib.redirect_stdout(None):
            main.main()
        handle_two_addrs.assert_called_once_with("125.47.32.170/25", "125.47.32.53/25")
