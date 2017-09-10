"""unittests for sealant's randstr_terminal classes and functions"""

import os
import sys
import shutil
import random
import unittest
import tempfile
import pyperclip

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

        switches = ['-p', '--print', '-cp', '--copy', '-f', '--file', '-ro',
                    '--raw-output', ('-cs', 'abc'), ('--character-set', 'abc'),
                    '-s', '--shuffle']

        args = [('1',) + i if isinstance(i, tuple) else ('1', i) for i in switches]

        for arg in args:
            with self.subTest(arg=arg):
                self.assertIsNot(self.parser.parse_args(arg), None)

    def test_boolean_switches(self):
        """Sub-tests for simple switches that store as True when included as an
        argument"""
        switches = {'print': ['-p', '--print'],
                    'copy': ['-cp', '--copy'],
                    'shuffle': ['-s', '--shuffle'],
                    'raw_output': ['-ro', '--raw-output']}

        for dest, switches in switches.items():
            for switch in switches:
                with self.subTest(switch=switch):
                    args = self.parser.parse_args([self.str_len, switch])
                    self.assertTrue(getattr(args, dest))


class RandstrOutputTests(unittest.TestCase):
    """Test cases for randstr_terminal.randstr_output()"""

    def setUp(self):
        """Sets up default parser and test directories used during tests"""
        self.parser = randstr_terminal.RandstrParser().parser
        self.str_len = str(random.randint(10, 100))

        self.randstr_output = randstr_terminal.randstr_output

        self.test_dir = tempfile.mkdtemp()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Removes any files/directories created during file write test
        procedures."""

        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        shutil.rmtree(self.test_dir)

    def test_raw_output(self):
        """Tests use of --raw-output switch"""

        args = self.parser.parse_args([self.str_len, '--raw-output'])
        self.randstr_output(args)

        output = sys.stdout.getvalue()
        self.assertEqual(int(self.str_len), len(output))

    def test_copy_results(self):
        """Test that use of '--copy' switch copies string to clipboard"""

        args = self.parser.parse_args([self.str_len, '--copy', '--print'])
        self.randstr_output(args)

        output = sys.stdout.getvalue()
        clipboard_contents = pyperclip.paste()

        self.assertIn(clipboard_contents, output)

    def test_file_write(self):
        """Test that randomized correctly writes to file"""

        args = self.parser.parse_args([self.str_len, '--file', '--print'])

        self.randstr_output(args)
        output = sys.stdout.getvalue()

        filename = os.path.join(self.test_dir, args.file)
        with open(filename, 'r') as f:
            random_string = f.read()

        self.assertIn(random_string, output)


if __name__ == '__main__':
    print("Testing randstr_terminal Methods and Functions\n")
    unittest.main(buffer=True)
