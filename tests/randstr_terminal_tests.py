"""unittests for sealant's randstr_terminal classes and functions"""

import os
import sys
import unittest
import pyperclip

sys.path.insert(0, os.path.abspath('../sealant/randstr'))  # shhh
import randstr_terminal


class RandstrParserTests(unittest.TestCase):
    """Tests for Randstr's argparser methods"""

    def setUp(self):
        """Sets up parser object to be used for argparse.parse_args calls"""
        self.parser = randstr_terminal.RandstrParser().parser
        self.length = 10

    def test_undefined_length(self):
        """Verify passing empty arguments causes system exit"""

        with self.assertRaises(SystemExit) as cm:
            self.parser.parse_args()

        sys_exit = cm.exception
        self.assertEqual(sys_exit.code, 2)

    def test_print_switch(self):
        """Test use of print switch"""

        args = self.parser.parse_args(['10', '-p'])
        self.assertTrue(args.print)


if __name__ == '__main__':
    unittest.main(buffer=True)
