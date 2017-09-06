"""unittests for sealant's randstr_terminal classes and functions"""

import os
import sys
import random
import unittest
import pyperclip
import freezegun
import datetime

sys.path.insert(0, os.path.abspath('../sealant/randstr'))  # shhh
import randstr_terminal


class RandstrParserTests(unittest.TestCase):
    """Tests for Randstr's argparser methods"""

    def setUp(self):
        """Sets up parser object to be used for argparse.parse_args calls"""
        self.parser = randstr_terminal.RandstrParser().parser
        self.str_len = str(random.randint(10, 100))

    def test_undefined_length(self):
        """Verify passing empty arguments causes system exit"""

        with self.assertRaises(SystemExit) as cm:
            self.parser.parse_args()

        sys_exit = cm.exception
        self.assertEqual(sys_exit.code, 2)

    def test_length_argument(self):
        """tests length value and type correctly set"""
        args = self.parser.parse_args([self.str_len])
        self.assertEqual(int(self.str_len), args.len)


    def test_boolean_switches(self):
        """Subtests for simple switches that store as True when included as an
        argument"""

        switches = {'-p': 'print', '-cp': 'copy', '-s': 'shuffle'}

        for switch, dest in switches.items():
            with self.subTest(switch=switch):
                args = self.parser.parse_args([self.str_len, switch])
                self.assertTrue(getattr(args, dest))


@freezegun.freeze_time('2017-01-01 12:00:00')
class FileWriteTests(unittest.TestCase):
    """Tests class methods and functions that deal with file writing"""


    def setUp(self):
        """Sets up necessary attributes for file write tests"""
        self.parser = randstr_terminal.RandstrParser().parser
        self.str_len = str(random.randint(10, 100))

        self._strftime = datetime.datetime.now().strftime('%a%d-%H%M%S')
        self.default_file = "randstr_{}.txt".format(self._strftime)
        self.test_directory = os.path.abspath('test_write_files\\')

        os.mkdir(self.test_directory)


    def tearDown(self):
        """ Removes any files/directories created during file write tests"""

        temp_files = os.listdir(self.test_directory)
        if temp_files:
            for file in temp_files:
                os.remove(os.path.abspath(file))

        os.rmdir(self.test_directory)


if __name__ == '__main__':
    unittest.main(buffer=True)
