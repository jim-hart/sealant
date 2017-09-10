"""unittests for sealant's randstr_terminal classes and functions"""

import os
import sys
import random
import unittest

sys.path.insert(0, os.path.abspath('../sealant/randstr'))  # shhh
import randstr_terminal


class RandstrParserTests(unittest.TestCase):
    """Tests for Randstr's argparse methods"""

    def setUp(self):
        """Sets up parser object to be used for argparse.parse_args calls"""
        self.parser = randstr_terminal.RandstrParser().parser
        self.str_len = str(random.randint(10, 100))
        self.reference_char_set = (
            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVW"
            "XYZ0123456789!\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~ ")

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

    def test_character_set_argument(self):
        """Tests that user-defined character set is correctly saved (i.e.
        identical characters and character index positions)"""

        user_char_set = ''.join(random.sample(
            self.reference_char_set, random.randint(10, 90)))

        args = self.parser.parse_args(
            [self.str_len, '--character-set', user_char_set])

        self.assertEqual(user_char_set, args.characters)

    def test_user_defined_filename(self):
        """Tests that user defined filename overrides default filename for
        --file switch"""

        # valid filename characters
        char_set = [c for c in self.reference_char_set if c not in '\\/:*?"<>|']
        random_name = ''.join(
            random.choice(char_set) for _ in range(0, random.randint(10, 50)))

        user_filename = "{}.txt".format(random_name)

        args = self.parser.parse_args([self.str_len, '--file', user_filename])
        self.assertTrue(user_filename, args.file)

    def test_switch_combinations(self):
        """Verifies all available switches accepted as an argument"""

        switches = ['-p', '--print', '-cp', '--copy', '-f', '--file',
                    ('-cs', 'abc'), ('--character-set', 'abc'), '-s', '--shuffle']

        args = [('1',) + i if isinstance(i, tuple) else ('1', i) for i in switches]

        for arg in args:
            with self.subTest(arg=arg):
                self.assertIsNot(self.parser.parse_args(arg), None)

    def test_boolean_switches(self):
        """Sub-tests for simple switches that store as True when included as an
        argument"""
        switches = {'-p': 'print', '-cp': 'copy', '-s': 'shuffle'}

        for switch, dest in switches.items():
            with self.subTest(switch=switch):
                args = self.parser.parse_args([self.str_len, switch])
                self.assertTrue(getattr(args, dest))


class FileWriteTests(unittest.TestCase):
    """Tests class methods and functions that deal with file writing"""

    def setUp(self):
        """Sets up necessary attributes for file write tests"""
        self.parser = randstr_terminal.RandstrParser().parser
        self.str_len = str(random.randint(10, 100))

        self.test_directory = os.path.abspath('test_write_files\\')

        os.mkdir(self.test_directory)

    def tearDown(self):
        """ Removes any files/directories created during file write test
        procedures"""
        temp_files = os.listdir(self.test_directory)

        if temp_files:
            for file in temp_files:
                os.remove(os.path.abspath(file))

        os.rmdir(self.test_directory)


if __name__ == '__main__':
    print("Testing randstr_terminal Methods and Functions\n")
    unittest.main(buffer=True)
